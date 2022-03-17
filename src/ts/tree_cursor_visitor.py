from typing import Callable, Dict, List, Tuple

from .node import Node
from src.cfa import CFA, CFANode

class TreeCFAVisitor():
    _cfa: CFA
    _current: CFANode
    _visits: Dict[str, Callable[[Node], CFANode]]
    _order: List[Node]
    _merges: List[Tuple[Node, Node]]

    def __init__(self) -> None:
        # We dont have the "translation_unit" because it will always be the root
        self._visits: Dict[str, Callable[[Node], CFANode]] = {
            "expression_statement": self.visit_expression_statement,
            "if_statement": self.visit_if_statement,
        }
        self._do_merge = False
        self._current = None

    def current(self) -> CFANode:
        return self._current

    def next(self, d: CFANode) -> CFANode:
        # s
        # |
        # d
        s: CFANode = self.current()
        if s.node is None:
            s.node = d.node
            return s
        return self.branch(s, d)

    def branch(self, s: CFANode, d: CFANode) -> CFANode:
        # s
        # |
        # d
        self._cfa.branch(s, d)
        self._current = d
        return d

    def create(self, root: Node) -> CFA:
        self._order = [ root ]

        cfa_root: CFANode = CFANode(root)
        self._current = cfa_root
        self._cfa = CFA(cfa_root)

        self._previous_collection = list()
        self._previous_collection.append(cfa_root)

        self.visit_children(root)

        return self._cfa

    def accept(self, node: Node) -> CFANode:
        if node.type in self._visits:
            return self._visits[node.type](node)

    def visit(self, node: Node) -> CFANode:
        last: CFANode = self.accept(node)
        return last

    def visit_children(self, node: Node) -> CFANode:
        last: CFANode = None
        for child in node.children:
            if not child.is_named: continue
            last = self.accept(child)
        return last

    def visit_expression_statement(self, d: Node) -> CFANode:
        # p
        # |
        # d

        self._order.append(d)
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
        self._order.append(node)

        consequence: Node = node.child_by_field_name("consequence")
        if consequence is not None and consequence.child_count > 0:
            j: CFANode = CFANode(None)
            c: CFANode = None
            # By doing this branch the next to be replaced will be "j"
            self.branch(p, j)
            self.visit(consequence)
            c = self.visit_children(consequence)
            # By doing this branch the next to be replaced will be "s"
            #   This is useful in the cases where there are no "alternative"
            #   s.t. we will just continue from "s" which is essentially 
            #   then the outgoing endpoint from "p"
            self.branch(c, s)
            if c is not None and c.node is None: self._cfa.remove(c)

        alternative: Node = node.child_by_field_name("alternative")
        if alternative is not None and alternative.child_count > 0:
            i: CFANode = CFANode(None)
            a: CFANode = None
            # By doing this branch the next to be replaced will be "i"
            self.branch(p, i)

            # Check if it is an else-if chain, if so then dont check the children
            #   but allow the accept call to accept the if-stmt visit.
            if alternative.type == "if_statement":
                a = self.visit(alternative)
            else: a = self.visit_children(alternative)
            self.branch(a, s)
            if a is not None and a.node is None: self._cfa.remove(a)
        else: self.branch(p, s)

        return s

    def visit_switch_statement(self, node: Node) -> CFANode:
        pass

    def visit_while_statement(self, node: Node) -> CFANode:
        pass

    def visit_do_statement(self, node: Node) -> CFANode:
        pass

    def visit_for_statement(self, node: Node) -> CFANode:
        pass

    def visit_goto_label(self, node: Node) -> CFANode:
        pass

    def visit_continue_statement(self, node: Node) -> CFANode:
        pass

    def visit_return_statement(self, node: Node) -> CFANode:
        pass