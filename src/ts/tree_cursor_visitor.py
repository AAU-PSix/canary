from typing import Callable, Dict, Tuple, List
from queue import LifoQueue


from .node import Node
from src.ts.tree import Tree
from src.cfa import CFA, CFANode

class TreeCFAVisitor():
    _cfa: CFA
    _continue_break_stack: LifoQueue[Tuple[CFANode, CFANode]]
    _current: CFANode
    _tree: Tree
    _labels: List[Tuple[CFANode, str]]
    _gotos: List[Tuple[CFANode, str]]

    def __init__(self, tree: Tree) -> None:
        # We dont have the "translation_unit" because it will always be the root
        self._visits: Dict[str, Callable[[Node], CFANode]] = {
            "expression_statement": self.visit_node,
            "declaration": self.visit_node,
            "if_statement": self.visit_if_statement,
            "while_statement": self.visit_while_statement,
            "translation_unit": self.visit_translation_unit,
            "compound_statement": self.visit_compound_statement,
            "do_statement": self.visit_do_statement,
            "for_statement": self.visit_for_statement,
            "switch_statement": self.visit_switch_statement,
            "break_statement": self.visit_break_statement,
            "continue_statement": self.visit_continue_statement,
            "return_statement": self.visit_return_statement,
            "labeled_statement": self.visit_labeled_statement,
            "goto_statement": self.visit_goto_statement,
        }
        self._current = None
        self._tree = tree

    def create(self, root: Node, include_root: bool = True) -> CFA:
        self._continue_break_stack = LifoQueue()
        self._labels = list()
        self._gotos = list()
        cfa_root: CFANode = CFANode(root if include_root else None)
        self._cfa = CFA(cfa_root)
        self.next(cfa_root)

        self.accept(root)

        return self._cfa

    def _continue(self, source: CFANode) -> CFANode:
        continue_break: Tuple[CFANode, CFANode] = self._continue_break_stack.get()
        self._continue_break_stack.put(continue_break)
        return self.branch(source, continue_break[0], "C")

    def _break(self, source: CFANode) -> CFANode:
        continue_break: Tuple[CFANode, CFANode] = self._continue_break_stack.get()
        self._continue_break_stack.put(continue_break)
        return self.branch(source, continue_break[1], "B")

    def _add_label(self, label: Node, label_stmt: CFANode) -> None:
        label_str: str = self._tree.contents_of(label)
        self._labels.append((label_stmt, label_str))
        current: CFANode = self._current
        for goto in self._gotos:
            goto_stmt: CFANode = goto[0]
            goto_label_str: str = goto[1]
            if goto_label_str == label_str:
                self.branch(goto_stmt, label_stmt, "G")
                break
        self.set_active(current)

    def _add_goto(self, label: Node, goto_stmt: CFANode) -> None:
        goto_label_str: str = self._tree.contents_of(label)
        self._gotos.append((goto_stmt, goto_label_str))
        current: CFANode = self._current
        for label in self._labels:
            label_stmt: CFANode = label[0]
            label_str: str = label[1]
            if label_str == goto_label_str:
                self.branch(goto_stmt, label_stmt, "G")
                break
        self.set_active(current)

    def current(self) -> CFANode:
        return self._current

    def next(self, d: CFANode) -> CFANode:
        # s
        # |
        # d
        s: CFANode = self.current()
        if s is None:
            self._current = d
            return d
        elif s.node is None:
            s.node = d.node
            return s
        return self.branch(s, d)

    def branch(self, s: CFANode, d: CFANode, label: str = None) -> CFANode:
        # s
        # |
        # d
        self._cfa.branch(s, d, label)
        self._current = d
        return d

    def set_active(self, node: CFANode) -> None:
        self._current = node

    def accept(self, node: Node) -> CFANode:
        if node.type in self._visits:
            return self._visits[node.type](node)

    def visit_translation_unit(self, node: Node) -> CFANode:
        last: CFANode = None
        for child in node.named_children:
            last = self.accept(child)
        return last

    def visit_compound_statement(self, node: Node) -> CFANode:
        last: CFANode = None
        for child in node.named_children:
            last = self.accept(child)
        return last

    def visit_node(self, d: Node) -> CFANode:
        # p
        # |
        # d
        return self.next(CFANode(d))

    def visit_if_statement(self, node: Node) -> CFANode:
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

        condition: Node = node.child_by_field_name("condition")
        p: CFANode = self.next(CFANode(condition))
        s: CFANode = CFANode(None)

        consequence: Node = node.child_by_field_name("consequence")
        if consequence is not None and consequence.child_count > 0:
            j: CFANode = CFANode(None)
            # By doing this branch the next to be replaced will be "j"
            self.branch(p, j, "T")
            c: CFANode = self.accept(consequence)
            self.branch(c, s)
            if c is not None and c.node is None:
                self._cfa.remove(c)

        alternative: Node = node.child_by_field_name("alternative")
        if alternative is not None and alternative.child_count > 0:
            i: CFANode = CFANode(None)
            # By doing this branch the next to be replaced will be "i"
            self.branch(p, i, "F")
            a: CFANode = self.accept(alternative)
            self.branch(a, s)
            if a is not None and a.node is None:
                self._cfa.remove(a)
        else:
            self.branch(p, s, "F")
            if p is not None and p.node is None:
                self._cfa.remove(p)
        return s

    def visit_switch_statement(self, node: Node) -> CFANode:
        # Because of fallthrough for now we assume that the end of
        #   the first case is connected with the start of the next.
        #   p
        #  /|\
        # v v v
        # |/|/|
        # c c c
        #  \|/
        #   s

        p: CFANode = CFANode(node.child_by_field_name("condition"))
        p = self.next(p)
        s: CFANode = CFANode(None)

        cases: List[Tuple[CFANode, CFANode]] = list()

        body: Node = node.child_by_field_name("body")
        # A child will always be a "case_statement"
        for child in body.named_children:
            value: Node = child.child_by_field_name("value")
            v: CFANode = CFANode(value)

            # Case 1: No body "case 1:"
            if child.named_child_count == 1 and value is not None:
                self.branch(p, v, "C")
            # Case 2: Has body "case 1: a=1;"
            elif child.named_child_count == 2:
                self.branch(p, v, "C")
                # The next named sibling could eg. be 
                #   "expression_statement" and "compound_statement"
                self.accept(
                    value.next_named_sibling
                )
            # Case 3: Default "default: a=3;"
            elif child.named_child_count == 1 and value is None:
                self.branch(p, v, "D")
                self.accept(
                    child.named_children[0]
                )
            cases.append((v, self._current))

        # Connect fall throughs
        for idx in range(0, len(cases) - 1):
            prev_end: CFANode = cases[idx][1]
            next_start: CFANode = cases[idx + 1][0]
            self.branch(prev_end, next_start)

        # Connect breaks
        for idx in range(0, len(cases)):
            prev_end: CFANode = cases[idx][1]
            self.branch(prev_end, s)

        return s

    def visit_while_statement(self, node: Node) -> CFANode:
        # While-loop with "p" condition, and "b" body which when "c"
        #   is true is then executed. Otherwise, we exit and advance to "s"
        # --p--
        # | | |
        # | j s
        # | |
        # --b

        condition: Node = node.child_by_field_name("condition")
        p: CFANode = self.next(CFANode(condition))
        s: CFANode = CFANode(None)

        self._continue_break_stack.put((p, s))

        j: CFANode = CFANode(None)
        self.branch(p, j, "T")
        b: Node = node.child_by_field_name("body")
        self.accept(b)
        self.next(p)

        self._continue_break_stack.get()

        return self.branch(p, s, "F")

    def visit_do_statement(self, node: Node) -> CFANode:
        #   i
        #   |
        # --b
        # | |
        # --c-s
        i: CFANode = CFANode(None)
        i = self.next(i)
        b: CFANode = self.accept(node.child_by_field_name("body"))
        c: CFANode = CFANode(node.child_by_field_name("condition"))
        self.next(c)
        s: CFANode = CFANode(None)
        self.branch(c, i, "T")
        return self.branch(c, s, "F")

    def visit_for_statement(self, node: Node) -> CFANode:
        #   i
        #   |
        # --c--
        # | | |
        # | j n
        # | | |
        # | b f
        # | |
        # --u
        f: CFANode = CFANode(None)
        i: CFANode = CFANode(node.child_by_field_name("initializer"))
        c: CFANode = CFANode(node.child_by_field_name("condition"))
        u: CFANode = CFANode(node.child_by_field_name("update"))

        has_init: bool = i.node is not None
        has_cond: bool = c.node is not None
        has_update: bool = u.node is not None

        last_child: Node = node.named_children[-1]
        l: CFANode = CFANode(last_child)
        is_expression: bool = last_child.type == "expression_statement"
        is_compound: bool = last_child.type == "compound_statement"
        is_empty: bool = is_expression or is_compound and last_child.named_child_count is 0

        self._continue_break_stack.put((u, f))

        if has_init:
            self.next(i)
        if has_cond:
            self.next(c)

        # The following are the various configurations which can be made
        #   with the "condition", "update", and "body". However, the
        #   biggest problems lies when there are no "condition" beucase
        #   implicitly it means that there is a "condition" which cant
        #   be found in the tree and evaluated to TRUE constantly.
        if has_cond and not has_update and is_empty:
            self.branch(c, c, "T")
        elif not has_cond and not has_update and is_empty:
            c = self.next(l)
            self.branch(c, c, "T")
        elif has_cond and has_update and is_empty:
            self.next(u)
            self.branch(self.current(), c, "T")
        elif has_cond and has_update and not is_empty:
            j: CFANode = CFANode(None)
            self.branch(self.current(), j, "T")
            self.accept(last_child)
            self.next(u)
            self.next(c)
        elif has_cond and not has_update and not is_empty:
            j: CFANode = CFANode(None)
            self.branch(self.current(), j, "T")
            self.accept(last_child)
            self.next(c)
        elif not has_cond and not has_update and not is_empty:
            c = self.accept(last_child)
            self.branch(c, c, "T")

        self._continue_break_stack.get()

        return self.branch(c, f, "F")

    def visit_labeled_statement(self, node: Node) -> CFANode:
        label: Node = node.child_by_field_name("label")
        stmt: CFANode = self.next(CFANode(node))
        self._add_label(label, stmt)
        return stmt

    def visit_goto_statement(self, node: Node) -> CFANode:
        label: Node = node.child_by_field_name("label")
        stmt: CFANode = CFANode(node)
        self._add_goto(label, stmt)
        return self.next(stmt)

    def visit_break_statement(self, node: Node) -> CFANode:
        break_node: CFANode = CFANode(node)
        current: CFANode = self.current()
        self._break(break_node)
        self.set_active(current)
        return self.next(break_node)

    def visit_continue_statement(self, node: Node) -> CFANode:
        continue_node: CFANode = CFANode(node)
        current: CFANode = self.current()
        self._continue(continue_node)
        self.set_active(current)
        return self.next(continue_node)

    def visit_return_statement(self, node: Node) -> CFANode:
        return_node = self.next(CFANode(node))
        self._cfa.add_final(return_node)
        return return_node