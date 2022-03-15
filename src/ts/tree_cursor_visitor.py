from typing import Callable, Dict, Iterable, List, Tuple

from .node import Node
from .tree_cursor import TreeCursor
from src.cfa import CFA, CFANode

class TreeCFAVisitor():
    _cfa: CFA
    _current: CFANode
    _visits: Dict[str, Callable[[TreeCursor], None]]
    _order: List[Node]
    _merges: List[Tuple[Node, Node]]

    def __init__(self) -> None:
        # We dont have the "translation_unit" because it will always be the root
        self._visits: Dict[str, Callable[[TreeCursor], None]] = {
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
        self._current = d
        self._cfa.branch(s, d)
        return d

    def next_empty(self) -> CFANode:
        return self.next(CFANode(None))

    def branch(self, s: CFANode, d: CFANode) -> CFANode:
        # s
        # |
        # d
        self._cfa.branch(s, d)
        self._current = d
        return d

    def accept(self, root: Node) -> CFA:
        self._order = [ root ]

        cfa_root: CFANode = CFANode(root)
        self._current = cfa_root
        self._cfa = CFA(cfa_root)

        self._previous_collection = list()
        self._previous_collection.append(cfa_root)

        self.visit_children(root)

        return self._cfa

    def visit(self, node: Node) -> CFANode:
        if node.type in self._visits:
            return self._visits[node.type](node)

    def visit_children(self, node: Node) -> CFANode:
        last: CFANode = None
        for child in node.children:
            if not child.is_named: continue
            last = self.visit(child)
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
            self.branch(p, j)

            self.visit(consequence)
            c: CFANode = self.visit_children(consequence)
            self.branch(c, s)

        alternative: Node = node.child_by_field_name("alternative")
        if alternative is not None and alternative.child_count > 0:
            i: CFANode = CFANode(None)
            self.branch(p, i)

            self.visit(alternative)
            a: CFANode = self.visit_children(alternative)
            self.branch(a, s)
        else: self.branch(p, s)
