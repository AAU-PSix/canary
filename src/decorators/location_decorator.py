from abc import ABC, abstractmethod
from dataclasses import dataclass
from cfa import CFANode, CFAEdge, CFAGeneric, CFA, CFAFactory
from cfa.c_cfa_factory import CCFAFactory
from ts.c_syntax import *
from typing import List, Dict



class LocalisedNode(CFANode):
    def __init__(self, node: Node) -> None:
        self.location = -99
        super().__init__(node)

class LocalisedCFA(CFAGeneric[LocalisedNode, CFAEdge]):
    pass

class LocalisedCFACFactory(CCFAFactory):
    pass


class ScopeContent:
    def __init__(self) -> None:
        self.statements: List[LocalisedNode] = []

    def add_to_scope(self, node : LocalisedNode):
        self.statements.append(node)

def peek(stack: Dict[int, ScopeContent]) -> ScopeContent:
    if stack == {}:
        return None
    else:
        top = len(stack)-1
        return stack[top]



@dataclass
class DecorationResult():
    cfa: LocalisedCFA = None

@dataclass
class LocalisationResult(DecorationResult):
    Scopes: Dict[int, ScopeContent] = None

class CFADecorator(ABC):

    @abstractmethod
    def decorate(self) -> DecorationResult:
        pass



class LocationDecorator(CFADecorator):

    def __init__(self, CFA: LocalisedCFA) -> None:
        self.cfa = CFA
        self.location_value = 0
        self.scopes: Dict[int, ScopeContent] = {self.location_value:ScopeContent()}
        self.result: Dict[int, ScopeContent] = {}

    def _add_to_current_scope(self, node: LocalisedNode):
        node.location = self.location_value
        dict = peek(self.scopes)
        if dict is not None:
            dict.add_to_scope(node)

    def decorate(self) -> LocalisationResult:
        syntax = CSyntax()
        searched_nodes = []
        for cfa_node in self.cfa.breadth_first_traverse():
            if cfa_node in searched_nodes:
                continue
    
            searched_nodes.append(cfa_node)
            
            if syntax.is_condition_of_if(cfa_node.node):
                self._enter_scope(cfa_node)
                continue
            elif syntax.is_else_if(cfa_node.node):
                self._enter_scope(cfa_node)
                continue
            # Switch
            elif syntax.is_condition_of_switch(cfa_node.node):
                self._enter_scope(cfa_node)
                continue
            elif syntax.is_empty_switch_case(cfa_node.node):
                self._enter_scope(cfa_node)
                continue
            elif syntax.is_default_switch_case(cfa_node.node):
                self._enter_scope(cfa_node)
                continue
            # While and for
            elif syntax.is_condition_of_while(cfa_node.node):
                self._enter_scope(cfa_node)
                continue
            elif syntax.is_condition_of_do_while(cfa_node.node):
                self._enter_scope(cfa_node)
                continue
            elif syntax.is_body_of_for_loop(cfa_node.node):
                self._enter_scope(cfa_node)
                continue
            else:
                self._add_to_current_scope(cfa_node)
                continue
                
        # Exit global scope to say that we are done
        self._exit_scope()

        return DecorationResult(Scopes=self.result, cfa=self.cfa)
                

    def _exit_scope(self):
        location = self.location_value
        content = self.scopes.pop(location)
        self.result[location] = content
        self.location_value -= 1

    def _enter_scope(self, node: LocalisedNode):
        scope = ScopeContent()
        self._add_to_current_scope(node)
        self.scopes[self.location_value] = scope
        self.location_value += 1
    

    

from typing import (
    Callable,
    Dict,
    Tuple,
    List
)
from collections import deque
from ts import (
    Node,
    Tree,
    CNodeType,
    CField,
    CSyntax
)
from cfa.cfa_factory import CFAFactory
from cfa import CFA


class CCFADecoratorFactory(CFAFactory):
    _cfa: CFA
    _tree: Tree
    _continue_break_stack: "deque[Tuple[LocalisedNode, LocalisedNode]]"
    _current: LocalisedNode
    _labels: List[Tuple[LocalisedNode, str]]
    _gotos: List[Tuple[LocalisedNode, str]]

    def __init__(self, tree: Tree) -> None:
        # We dont have the "translation_unit" because it will always be the root
        self._visits: Dict[str, Callable[[Node], LocalisedNode]] = {
            CNodeType.EXPRESSION_STATEMENT.value: self._visit_node,
            CNodeType.DECLARATION.value: self._visit_node,
            CNodeType.IF_STATEMENT.value: self._visit_if_statement,
            CNodeType.WHILE_STATEMENT.value: self._visit_while_statement,
            CNodeType.TRANSLATION_UNIT.value: self._visit_translation_unit,
            CNodeType.COMPOUND_STATEMENT.value: self._visit_compound_statement,
            CNodeType.DO_STATEMENT.value: self._visit_do_statement,
            CNodeType.FOR_STATEMENT.value: self._visit_for_statement,
            CNodeType.SWITCH_STATEMENT.value: self._visit_switch_statement,
            CNodeType.BREAK_STATEMENT.value: self._visit_break_statement,
            CNodeType.CONTINUE_STATEMENT.value: self._visit_continue_statement,
            CNodeType.RETURN_STATEMENT.value: self._visit_return_statement,
            CNodeType.LABELED_STATEMENT.value: self._visit_labeled_statement,
            CNodeType.GOTO_STATEMENT.value: self._visit_goto_statement,
        }
        self._current = None
        self._tree = tree
        self._syntax = CSyntax()

    def create(self, root: Node) -> LocalisedCFA:
        self._continue_break_stack = deque()
        self._labels = list()
        self._gotos = list()
        cfa_root: LocalisedNode = LocalisedNode(None)
        self._cfa = CFA(cfa_root)
        self._next(cfa_root)

        self._accept(root)

        if self._current is not None and self._current.node is None:
            self._cfa.remove(self._current)

        return self._cfa

    def _add_continue(self, source: LocalisedNode) -> LocalisedNode:
        continue_break: Tuple[LocalisedNode, LocalisedNode] = self._continue_break_stack.pop()
        self._continue_break_stack.append(continue_break)
        return self._branch(source, continue_break[0], "C")

    def _add_break(self, source: LocalisedNode) -> LocalisedNode:
        continue_break: Tuple[LocalisedNode, LocalisedNode] = self._continue_break_stack.pop()
        self._continue_break_stack.append(continue_break)
        return self._branch(source, continue_break[1], "B")

    def _add_label(self, label: Node, label_stmt: LocalisedNode) -> None:
        label_str: str = self._tree.contents_of(label)
        self._labels.append((label_stmt, label_str))
        current: LocalisedNode = self._current
        for goto in self._gotos:
            goto_stmt: LocalisedNode = goto[0]
            goto_label_str: str = goto[1]
            if goto_label_str == label_str:
                self._branch(goto_stmt, label_stmt, "G")
        self._set_active(current)

    def _add_goto(self, label: Node, goto_stmt: LocalisedNode) -> None:
        goto_label_str: str = self._tree.contents_of(label)
        self._gotos.append((goto_stmt, goto_label_str))
        current: LocalisedNode = self._current
        for label in self._labels:
            label_stmt: LocalisedNode = label[0]
            label_str: str = label[1]
            if label_str == goto_label_str:
                self._branch(goto_stmt, label_stmt, "G")
        self._set_active(current)

    def _next(self, d: LocalisedNode) -> LocalisedNode:
        # s
        # |
        # d
        s: LocalisedNode = self._current
        if s is None:
            self._current = d
            return d
        # if is possible for the TSNode to be None when we
        #   want to start a branch from another LocalisedNode.
        elif s.node is None:
            s.node = d.node
            return s
        return self._branch(s, d)

    def _branch(self, s: LocalisedNode, d: LocalisedNode, label: str = None) -> LocalisedNode:
        # s
        # |
        # d
        self._cfa.branch(s, d, label)
        self._current = d
        return d

    def _set_active(self, node: LocalisedNode) -> None:
        self._current = node

    def _accept(self, node: Node) -> LocalisedNode:
        if node.type in self._visits:
            return self._visits[node.type](node)

    def _accept_siblings(self, node: Node) -> LocalisedNode:
        last: LocalisedNode = None
        sibling: Node = node.next_named_sibling
        while sibling is not None:
            last = self._accept(sibling)
            sibling = sibling.next_named_sibling
        return last
    
    def _accept_children(self, node: Node) -> LocalisedNode:
        last: LocalisedNode = None
        for child in node.named_children:
            last = self._accept(child)
        return last

    def _visit_translation_unit(self, node: Node) -> LocalisedNode:
        return self._accept_children(node)

    def _visit_compound_statement(self, node: Node) -> LocalisedNode:
        # If the compound statement is empty, then we create a node for it.
        #   The reason for this is that the CFA loses too much detail if
        #   they are excluded completely.
        if node.named_child_count == 0:
            return self._next(LocalisedNode(node))
        return self._accept_children(node)

    def _visit_node(self, d: Node) -> LocalisedNode:
        # p
        # |
        # d
        return self._next(LocalisedNode(d))

    def _visit_if_statement(self, node: Node) -> LocalisedNode:
        # if with alternative
        # "j", "i" and "s" are None because we dont know whether they
        #   are required in the flow, it could be that there are
        #   no LocalisedNode(s) in the "alternative"/"consequence" and after the
        #   "if"-statement for these reasons they exists.
        #   p
        #  / \
        # j   i
        # |   |
        # c   a
        #  \ /
        #   s

        condition: Node = node.child_by_field(CField.CONDITION)
        p: LocalisedNode = self._next(LocalisedNode(condition))
        s: LocalisedNode = LocalisedNode(None)

        consequence: Node = node.child_by_field(CField.CONSEQUENCE)
        if consequence is not None:
            j: LocalisedNode = LocalisedNode(None)
            # By doing this branch the next to be replaced will be "j"
            j = self._branch(p, j, "T")
            c: LocalisedNode = self._accept(consequence)
            if j.node is not None:
                self._branch(c, s)
            else:
                self._cfa.remove(j)
                self._branch(p, s, "T")
            if c is not None and c.node is None:
                self._cfa.remove(c)

        alternative: Node = node.child_by_field(CField.ALTERNATIVE)
        if alternative is not None:
            i: LocalisedNode = LocalisedNode(None)
            # By doing this branch the next to be replaced will be "i"
            i = self._branch(p, i, "F")
            a: LocalisedNode = self._accept(alternative)
            if i.node is not None:
                self._branch(a, s)
            else:
                self._cfa.remove(i)
                self._branch(p, s, "F")
            if a is not None and a.node is None:
                self._cfa.remove(a)
        else:
            self._branch(p, s, "F")
        return s

    def _visit_switch_statement(self, node: Node) -> LocalisedNode:
        # Because of fallthrough for now we assume that the end of
        #   the first case is connected with the start of the next.
        #   p
        #  /|\
        # v v v
        # |/|/|
        # c c c
        #  \|/
        #   s

        p: LocalisedNode = LocalisedNode(node.child_by_field(CField.CONDITION))
        p = self._next(p)
        s: LocalisedNode = LocalisedNode(None)

        cases: List[Tuple[LocalisedNode, LocalisedNode]] = list()

        body: Node = node.child_by_field(CField.BODY)
        # A child will always be a "case_statement"
        for case_stmt in body.named_children:
            is_default_case = self._syntax.is_default_switch_case(case_stmt)
            is_empty_case = self._syntax.is_empty_switch_case(case_stmt)
            value: Node = case_stmt.child_by_field(CField.VALUE)

            v: LocalisedNode = LocalisedNode(value)
            c: LocalisedNode = LocalisedNode(None)

            # Case 1: No body "case 1:"
            if is_empty_case and not is_default_case:
                c = self._branch(p, v, "C")
            # Case 2: Has body "case 1: a=1;" or "case 1: a=1; a=2" or "case 1: { a=1; }"
            elif not is_empty_case and not is_default_case:
                c = self._branch(p, v, "C")
                # We have to visit all siblings because it might not be a "compound_statement"
                #   and just a sequence of expression statements.
                c = self._accept_siblings(v.node)
            # Case 3: Default which has no value, but has a body "default: a=1;"
            elif not is_empty_case and is_default_case:
                c = self._branch(p, v, "D")
                c = self._accept_children(case_stmt)
            # Case 4: Default but without a body "default:"
            elif is_empty_case and is_default_case:
                v = LocalisedNode(case_stmt)
                c = self._branch(p, v, "D")

            # We always add the current case, this helps discover bugs
            cases.append((v, c))

        # Connect fall throughs
        for idx in range(0, len(cases) - 1):
            prev_end: LocalisedNode = cases[idx][1]
            next_start: LocalisedNode = cases[idx + 1][0]
            self._branch(prev_end, next_start)

        # Connect breaks
        for case in cases:
            prev_end: LocalisedNode = case[1]
            self._branch(prev_end, s)
        return s

    def _visit_while_statement(self, node: Node) -> LocalisedNode:
        # While-loop with "p" condition, and "b" body which when "c"
        #   is true is then executed. Otherwise, we exit and advance to "s"
        # --p--
        # | | |
        # | j s
        # | |
        # --b

        condition: Node = node.child_by_field(CField.CONDITION)
        p: LocalisedNode = self._next(LocalisedNode(condition))
        s: LocalisedNode = LocalisedNode(None)

        self._continue_break_stack.append((p, s))

        j: LocalisedNode = LocalisedNode(None)
        self._branch(p, j, "T")
        b: Node = node.child_by_field(CField.BODY)
        self._accept(b)
        self._next(p)

        self._continue_break_stack.pop()

        return self._branch(p, s, "F")

    def _visit_do_statement(self, node: Node) -> LocalisedNode:
        #   i
        #   |
        # --b
        # | |
        # --c-s
        i: LocalisedNode = LocalisedNode(None)
        i = self._next(i)
        b: LocalisedNode = self._accept(node.child_by_field(CField.BODY))
        c: LocalisedNode = LocalisedNode(node.child_by_field(CField.CONDITION))
        self._next(c)
        s: LocalisedNode = LocalisedNode(None)
        self._branch(c, i, "T")
        return self._branch(c, s, "F")

    def _visit_for_statement(self, node: Node) -> LocalisedNode:
        #   i
        #   |
        # --c--
        # | | |
        # | j n
        # | | |
        # | b f
        # | |
        # --u
        f: LocalisedNode = LocalisedNode(None)
        i: LocalisedNode = LocalisedNode(node.child_by_field(CField.INITIALIZER))
        c: LocalisedNode = LocalisedNode(node.child_by_field(CField.CONDITION))
        u: LocalisedNode = LocalisedNode(node.child_by_field(CField.UPDATE))

        has_init: bool = i.node is not None
        has_cond: bool = c.node is not None
        has_update: bool = u.node is not None

        body: Node = self._syntax.get_for_loop_body(node)

        self._continue_break_stack.append((u, f))

        if has_init: self._next(i)
        if has_cond: self._next(c)

        # The following are the various configurations which can be made
        #   with the "condition", "update", and "body". However, the
        #   biggest problems lies when there are no "condition" beucase
        #   implicitly it means that there is a "condition" which cant
        #   be found in the tree and evaluated to TRUE constantly.
        if has_cond and has_update:
            j: LocalisedNode = LocalisedNode(None)
            j = self._branch(self._current, j, "T")
            self._accept(body)
            self._next(u)
            self._next(c)
        elif has_cond and not has_update:
            j: LocalisedNode = LocalisedNode(None)
            j = self._branch(self._current, j, "T")
            self._accept(body)
            self._next(c)
        elif not has_cond and not has_update:
            j: LocalisedNode = LocalisedNode(None)
            j = self._next(j)
            c = self._accept(body)
            self._branch(c, j)

        self._continue_break_stack.pop()

        # If we dont have a conditional, then we should not
        #   denote the transition with "F" marking the "false"
        #   branch, ebcause there are no predicate to be "false"
        return self._branch(c, f, "F" if has_cond else "")

    def _visit_labeled_statement(self, node: Node) -> LocalisedNode:
        label: Node = node.child_by_field(CField.LABEL)
        stmt: LocalisedNode = self._next(LocalisedNode(node))
        self._add_label(label, stmt)
        return stmt

    def _visit_goto_statement(self, node: Node) -> LocalisedNode:
        label: Node = node.child_by_field(CField.LABEL)
        stmt: LocalisedNode = LocalisedNode(node)
        self._add_goto(label, stmt)
        return self._next(stmt)

    def _visit_break_statement(self, node: Node) -> LocalisedNode:
        break_node: LocalisedNode = LocalisedNode(node)
        current: LocalisedNode = self._current
        self._add_break(break_node)
        self._set_active(current)
        return self._next(break_node)

    def _visit_continue_statement(self, node: Node) -> LocalisedNode:
        continue_node: LocalisedNode = LocalisedNode(node)
        current: LocalisedNode = self._current
        self._add_continue(continue_node)
        self._set_active(current)
        return self._next(continue_node)

    def _visit_return_statement(self, node: Node) -> LocalisedNode:
        return_node = self._next(LocalisedNode(node))
        self._cfa.add_final(return_node)
        return return_node