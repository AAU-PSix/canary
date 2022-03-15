from typing import Callable, Dict, Iterable, List

from .node import Node
from .tree_cursor import TreeCursor
from src.cfa import CFA, CFANode

class TreeCursorVisitor():
    _cfa: CFA
    _previous_collection: List[CFANode]
    _visits: Dict[str, Callable[[TreeCursor], None]]

    @property
    def _previous(self) -> CFANode:
        previous: CFANode = self._previous_collection[-1]
        if previous is None: previous = self._previous_collection[-2]
        return previous
    
    def _set_previous(self, node: CFANode) -> None:
        self._previous_collection[-1] = node

    def _add_depth(self, node: CFANode = None) -> None:
        self._previous_collection.append(node)

    def _remove_depth(self) -> None:
        self._previous_collection.pop()

    def _branch(self, destination: CFANode) -> None:
        self._cfa.branch(self._previous, destination)

    def accept(self, node: Node) -> CFA:
        # We dont have the "translation_unit" because it will always be the root
        self._visits: Dict[str, Callable[[TreeCursor], None]] = {
            "expression_statement": self.visit_expression_statement,
            "if_statement": self.visit_if_statement,
        }

        root_node: CFANode = CFANode(node)
        self._previous_collection = list()
        self._previous_collection.append(root_node)
        self._cfa = CFA(root_node)

        self.visit(root_node.node)
        return self._cfa

    def visit(self, node: Node) -> None:
        if node is None: return

        iterable: Iterable[Node] = node.pre_order_traverse(True)
        while True:
            # We have reached the end and the node has the default value
            if node is None: break

            # If we have a visit function then visit it and break
            # Otherwise, let the pre-order traversal handle what it does
            # This allows us to break early and re-visit from the one we want
            if node.type in self._visits:
                self._visits[node.type](node)
                break
            else: node = next(iterable, None)

    def visit_expression_statement(self, node: Node) -> None:
        cfa_node: CFANode = CFANode(node)
        self._branch(cfa_node)
        self._set_previous(cfa_node)
        self.visit(node.next_sibling)

    def visit_if_statement(self, node: Node) -> None:
        # Goto: "condition" (parenthesized_expression)
        # type: if
        condition: Node = node.first_child
        # type: parenthesized_expression
        condition = condition.next_sibling
        cfa_condition: CFANode = CFANode(condition)
        self._branch(cfa_condition)
        self._set_previous(cfa_condition)

        # Goto: "consequence" (compound_statement)
        # type: consequence
        consequence: Node = condition.next_sibling.next_sibling
        self._add_depth()
        self.visit(consequence)
        self._remove_depth()
