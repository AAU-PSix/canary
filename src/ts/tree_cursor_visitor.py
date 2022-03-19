from typing import Callable, Dict

from .node import Node
from src.cfa import CFA, CFANode

class TreeCFAVisitor():
    _cfa: CFA
    _current: CFANode

    def __init__(self) -> None:
        # We dont have the "translation_unit" because it will always be the root
        self._visits: Dict[str, Callable[[Node], CFANode]] = {
            "expression_statement": self.visit_expression_statement,
            "if_statement": self.visit_if_statement,
            "while_statement": self.visit_while_statement,
            "translation_unit": self.visit_translation_unit,
            "compound_statement": self.visit_compound_statement,
            "do_statement": self.visit_do_statement,
            "for_statement": self.visit_for_statement,
            "switch_statement": self.visit_switch_statement,
        }
        self._current = None

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

    def create(self, root: Node) -> CFA:
        self._order = [ ]

        cfa_root: CFANode = CFANode(root)
        self._current = cfa_root
        self._cfa = CFA(cfa_root)

        self.accept(root)

        if self._current.node is None:
            self._cfa.remove(self._current)

        return self._cfa

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

    def visit_expression_statement(self, d: Node) -> CFANode:
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
        # TODO: Implement fallthrough
        #   p
        #  /|\
        # c-c-c
        #  \|/
        #   s
        p: CFANode = CFANode(node.child_by_field_name("condition"))
        self.next(p)
        s: CFANode = CFANode(None)

        body: Node = node.child_by_field_name("body")
        # A child will always be a "case_statement"
        for child in body.named_children:
            c: CFANode = CFANode(None)
            value: Node = child.child_by_field_name("value")
            # Case 1: No body "case 1:"
            if child.named_child_count == 1 and value is not None:
                pass
            # Case 2: Has body "case 1: a=1;"
            elif child.named_child_count == 2:
                # The next named sibling could eg. be 
                #   "expression_statement" and "compound_statement"
                c = self.accept(
                    value.next_named_sibling
                )
            # Case 3: Default "default: a=3;"
            elif child.named_child_count == 1 and value is None:
                c = self.accept(
                    child.named_children[0]
                )

            self.branch(c, s)
            self.set_active(p)
        self.set_active(s)
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

        j: CFANode = CFANode(None)
        self.branch(p, j, "T")
        b: Node = node.child_by_field_name("body")
        self.accept(b)
        self.next(p)

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
        # | j |
        # | | |
        # | b |
        # | | |
        # --u f
        i: CFANode = CFANode(node.child_by_field_name("initializer"))
        self.next(i)
        c: CFANode = CFANode(node.child_by_field_name("condition"))
        self.next(c)
        j: CFANode = CFANode(None)
        self.branch(c, j, "T")
        self.accept(node.named_children[-1])
        u: CFANode = CFANode(node.child_by_field_name("update"))
        self.next(u)
        self.branch(u, c)
        f: CFANode = CFANode(None)
        self.branch(c, f, "F")
        return f

    def visit_goto_label(self, node: Node) -> CFANode:
        pass

    def visit_continue_statement(self, node: Node) -> CFANode:
        pass

    def visit_return_statement(self, node: Node) -> CFANode:
        pass