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
from .cfa_factory import CFAFactory
from .cfa import CFA
from .cfa_node import CFANode

class CCFAFactory(CFAFactory):
    _cfa: CFA[CFANode]
    _tree: Tree
    _continue_break_stack: "deque[Tuple[CFANode, CFANode]]"
    _current: CFANode
    _labels: List[Tuple[CFANode, str]]
    _gotos: List[Tuple[CFANode, str]]

    def __init__(self, tree: Tree) -> None:
        # We dont have the "translation_unit" because it will always be the root
        self._visits: Dict[str, Callable[[Node], CFANode]] = {
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
            CNodeType.FUNCTION_DEFINITION.value: self._visit_function_definition,
        }
        self._current = None
        self._tree = tree
        self._syntax = CSyntax()

    def _create_cfa_node(self, node: Node, description: str = None):
        cfa_node = CFANode(node)
        if description is not None: cfa_node.secret = description
        return cfa_node

    def create(self, root: Node) -> CFA[CFANode]:
        self._continue_break_stack = deque()
        self._labels = list()
        self._gotos = list()
        cfa_root: CFANode = CFANode(None)
        self._cfa = CFA[CFANode](cfa_root)
        self._next(cfa_root)

        self._accept(root)

        if self._current is not None and self._current.node is None:
            ingoing_edges = self._cfa.ingoing_edges(self._current)
            for edge in ingoing_edges: self._cfa.add_final(edge.source, edge.label)
            self._cfa.remove(self._current)

        return self._cfa

    def _add_continue(self, source: CFANode) -> CFANode:
        continue_break: Tuple[CFANode, CFANode] = self._continue_break_stack.pop()
        self._continue_break_stack.append(continue_break)
        return self._branch(source, continue_break[0], "C")

    def _add_break(self, source: CFANode) -> CFANode:
        continue_break: Tuple[CFANode, CFANode] = self._continue_break_stack.pop()
        self._continue_break_stack.append(continue_break)
        return self._branch(source, continue_break[1], "B")

    def _add_label(self, label: Node, label_stmt: CFANode) -> None:
        label_str: str = self._tree.contents_of(label)
        self._labels.append((label_stmt, label_str))
        current: CFANode = self._current
        for goto in self._gotos:
            goto_stmt: CFANode = goto[0]
            goto_label_str: str = goto[1]
            if goto_label_str == label_str:
                self._branch(goto_stmt, label_stmt, "G")
        self._set_active(current)

    def _add_goto(self, label: Node, goto_stmt: CFANode) -> None:
        goto_label_str: str = self._tree.contents_of(label)
        self._gotos.append((goto_stmt, goto_label_str))
        current: CFANode = self._current
        for label in self._labels:
            label_stmt: CFANode = label[0]
            label_str: str = label[1]
            if label_str == goto_label_str:
                self._branch(goto_stmt, label_stmt, "G")
        self._set_active(current)

    def _next(self, d: CFANode) -> CFANode:
        # s
        # |
        # d
        s: CFANode = self._current
        if s is None:
            self._current = d
            return d
        # if is possible for the TSNode to be None when we
        #   want to start a branch from another CFANode.
        elif s.node is None:
            s.node = d.node
            return s
        return self._branch(s, d)

    def _branch(self, s: CFANode, d: CFANode, label: str = None) -> CFANode:
        # s
        # |
        # d
        self._cfa.branch(s, d, label)
        self._current = d
        return d

    def _set_active(self, node: CFANode) -> None:
        self._current = node

    def _accept(self, node: Node) -> CFANode:
        if node.type in self._visits:
            return self._visits[node.type](node)

    def _accept_siblings(self, node: Node) -> CFANode:
        last: CFANode = None
        sibling: Node = node.next_named_sibling
        while sibling is not None:
            last = self._accept(sibling)
            sibling = sibling.next_named_sibling
        return last
    
    def _accept_children(self, node: Node) -> CFANode:
        last: CFANode = None
        for child in node.named_children:
            last = self._accept(child)
        return last

    def _visit_translation_unit(self, node: Node) -> CFANode:
        return self._accept_children(node)

    def _visit_function_definition(self, node: Node) -> CFANode:
        body = node.child_by_field(CField.BODY)
        return self._accept(body)

    def _visit_compound_statement(self, node: Node) -> CFANode:
        # If the compound statement is empty, then we create a node for it.
        #   The reason for this is that the CFA loses too much detail if
        #   they are excluded completely.
        if node.named_child_count == 0:
            return self._next(CFANode(node))
        return self._accept_children(node)

    def _visit_node(self, d: Node) -> CFANode:
        # p
        # |
        # d
        return self._next(CFANode(d))

    def _visit_if_statement(self, node: Node) -> CFANode:
        # if with alternative
        # "j", "i" and "s" are None because we dont know whether they
        #   are required in the flow, it could be that there are
        #   no CFANode(s) in the "alternative"/"consequence" and after the
        #   "if"-statement for these reasons they exists.
        #   p
        #  / \
        # j   i
        # |   |
        # c   a
        #  \ /
        #   s

        condition: Node = node.child_by_field(CField.CONDITION)
        p: CFANode = self._next(CFANode(condition))
        s: CFANode = CFANode(None)

        consequence: Node = node.child_by_field(CField.CONSEQUENCE)
        if consequence is not None:
            j: CFANode = CFANode(None)
            # By doing this branch the next to be replaced will be "j"
            j = self._branch(p, j, "T")
            c: CFANode = self._accept(consequence)
            if j.node is not None:
                self._branch(c, s)
            else:
                self._cfa.remove(j)
                self._branch(p, s, "T")
            if c is not None and c.node is None:
                self._cfa.remove(c)

        alternative: Node = node.child_by_field(CField.ALTERNATIVE)
        if alternative is not None:
            i: CFANode = CFANode(None)
            # By doing this branch the next to be replaced will be "i"
            i = self._branch(p, i, "F")
            a: CFANode = self._accept(alternative)
            if i.node is not None:
                self._branch(a, s)
            else:
                self._cfa.remove(i)
                self._branch(p, s, "F")
            if a is not None and a.node is None:
                self._cfa.remove(a)
        else:
            self._branch(p, s, "F")
        return self._next(s)

    def _visit_switch_statement(self, node: Node) -> CFANode:
        # Because of fallthrough for now we assume that the end of
        #   the first case is connected with the start of the next.
        # +---p
        # |  /|\
        # | v v v
        # | |/|/|
        # | c c c
        # |  \|/
        # +---s

        p: CFANode = CFANode(node.child_by_field(CField.CONDITION))
        p = self._next(p)
        s: CFANode = CFANode(None)
        self._continue_break_stack.append((None, s))

        cases: List[Tuple[CFANode, CFANode]] = list()

        body: Node = node.child_by_field(CField.BODY)
        # A child will always be a "case_statement"
        for case_stmt in body.named_children:
            is_default_case = self._syntax.is_default_switch_case(case_stmt)
            is_empty_case = self._syntax.is_empty_switch_case(case_stmt)
            value: Node = case_stmt.child_by_field(CField.VALUE)

            v: CFANode = CFANode(value)
            c: CFANode = CFANode(None)

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
                v = CFANode(case_stmt)
                c = self._branch(p, v, "D")

            # We always add the current case, this helps discover bugs
            cases.append((v, c))

        # Connect fall throughs
        for idx in range(0, len(cases) - 1):
            prev_end: CFANode = cases[idx][1]
            next_start: CFANode = cases[idx + 1][0]
            self._branch(prev_end, next_start)

        # Connect breaks
        for case in cases:
            prev_end: CFANode = case[1]
            self._branch(prev_end, s)

        self._continue_break_stack.pop()
        return s

    def _visit_while_statement(self, node: Node) -> CFANode:
        # While-loop with "p" condition, and "b" body which when "c"
        #   is true is then executed. Otherwise, we exit and advance to "s"
        # --p--
        # | | |
        # | j s
        # | |
        # --b

        condition: Node = node.child_by_field(CField.CONDITION)
        p: CFANode = self._next(CFANode(condition))
        s: CFANode = CFANode(None)

        self._continue_break_stack.append((p, s))

        j: CFANode = CFANode(None)
        self._branch(p, j, "T")
        b: Node = node.child_by_field(CField.BODY)
        self._accept(b)
        self._next(p)

        self._continue_break_stack.pop()

        return self._branch(p, s, "F")

    def _visit_do_statement(self, node: Node) -> CFANode:
        #   i
        #   |
        # --b
        # | |
        # --c-s
        i: CFANode = CFANode(None)
        i = self._next(i)
        b: CFANode = self._accept(node.child_by_field(CField.BODY))
        c: CFANode = CFANode(node.child_by_field(CField.CONDITION))
        self._next(c)
        s: CFANode = CFANode(None)
        self._branch(c, i, "T")
        return self._branch(c, s, "F")

    def _visit_for_statement(self, node: Node) -> CFANode:
        #   i
        #   |
        # --c--
        # | | |
        # | j f
        # | |
        # --u
        f: CFANode = CFANode(None)
        i: CFANode = CFANode(node.child_by_field(CField.INITIALIZER))
        c: CFANode = CFANode(node.child_by_field(CField.CONDITION))
        u: CFANode = CFANode(node.child_by_field(CField.UPDATE))

        has_init: bool = i.node is not None
        has_cond: bool = c.node is not None
        has_update: bool = u.node is not None

        body: Node = self._syntax.get_for_loop_body(node)

        if has_init: self._next(i)
        if has_cond: self._next(c)

        # The following are the various configurations which can be made
        #   with the "condition", "update", and "body". However, the
        #   biggest problems lies when there are no "condition" beucase
        #   implicitly it means that there is a "condition" which cant
        #   be found in the tree and evaluated to TRUE constantly.
        if has_cond and has_update:
            j: CFANode = CFANode(None)
            j = self._branch(self._current, j, "T")

            self._continue_break_stack.append((u, f))
            self._accept(body)
            self._continue_break_stack.pop()
            self._next(u)

            self._branch(self._current, c)
            return self._branch(c, f, "F")
        elif has_cond and not has_update:
            j: CFANode = CFANode(None)
            j = self._branch(self._current, j, "T")

            self._continue_break_stack.append((j, f))
            l: CFANode = self._accept(body)
            self._continue_break_stack.pop()

            q: CFANode = self._branch(l, j)
            if l.node is None: self._cfa.remove(l)

            return self._branch(c, f, "F")
        elif not has_cond and not has_update:
            j: CFANode = self._next(CFANode(None))

            self._continue_break_stack.append((j, f))
            l: CFANode = self._accept(body)
            self._continue_break_stack.pop()

            q: CFANode = self._branch(l, j)
            if l.node is None: self._cfa.remove(l)

            return self._branch(q, f)
        elif not has_cond and has_update:
            j: CFANode = self._next(CFANode(None))

            self._continue_break_stack.append((j, f))
            self._accept(body)
            self._continue_break_stack.pop()
            self._next(u)
            
            return self._branch(self._current, j)

    def _visit_labeled_statement(self, node: Node) -> CFANode:
        label: Node = node.child_by_field(CField.LABEL)
        stmt: CFANode = self._next(CFANode(node))
        self._add_label(label, stmt)
        return stmt

    def _visit_goto_statement(self, node: Node) -> CFANode:
        label: Node = node.child_by_field(CField.LABEL)
        stmt: CFANode = CFANode(node)
        self._add_goto(label, stmt)
        return self._next(stmt)

    def _visit_break_statement(self, node: Node) -> CFANode:
        break_node: CFANode = CFANode(node)
        current: CFANode = self._current
        self._add_break(break_node)
        self._set_active(current)
        return self._next(break_node)

    def _visit_continue_statement(self, node: Node) -> CFANode:
        continue_node: CFANode = CFANode(node)
        current: CFANode = self._current
        self._add_continue(continue_node)
        self._set_active(current)
        return self._next(continue_node)

    def _visit_return_statement(self, node: Node) -> CFANode:
        return_node = self._next(CFANode(node))
        self._cfa.add_final(return_node)
        return return_node