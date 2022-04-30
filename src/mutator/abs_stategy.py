from random import choice
from typing import List
from ts import Tree, Node, CField, CNodeType, CSyntax, Parser
from .mutation_strategy import MutationStrategy
from .mutation import Mutation, ReplacementMutation, WrappedMutation

class AbsStrategy(MutationStrategy):
    def __init__(self, parser: Parser) -> None:
        self._parser = parser
        self._language = parser.language
        self._syntax = CSyntax()

    def capture(self, node: Node) -> List[Node]:
        query_capture = self._language.query(
            self._syntax.binary_expression_query + \
            self._syntax.unary_expression_query + \
            self._syntax.number_literal_query + \
            self._syntax.declaration_query
        ).captures(node)
        
        nodes: List[Node] = query_capture.nodes()
        result: List[Node] = list()
        for node in nodes:
            if node.is_type(CNodeType.BINARY_EXPRESSION) and ( \
                node.children[1].is_either_type(self._syntax.arithmetic_operators or \
                node.children[1].is_either_type(self._syntax.arithmetic_compound_assignment))):
                if node not in result: result.append(node)
            elif node.is_type(CNodeType.UNARY_EXPRESSION) and \
                node.children[0].is_either_type(self._syntax.arithmetic_operators):
                if node not in result: result.append(node)
            elif node.is_type(CNodeType.NUMBER_LITERAL):
                if node not in result: result.append(node)
            # elif node.is_type(CNodeType.DECLARATION) and \
            #     node.child_by_field(CField.DECLARATOR).is_type(CNodeType.INIT_DECLARATOR):
            #     type_node = node.child_by_field(CField.TYPE)
            #     primitive: str = None
            #     if type_node is not None and type_node.is_type(CNodeType.PRIMITIVE_TYPE):
            #         pass
            #     elif type_node.is_type(CNodeType.SIZED_TYPE_SPECIFIER):
            #         type_type_node = type_node.child_by_field(CField.TYPE)
            #         if type_type_node is not None:
            #             type_type_node.is_type(CNodeType.PRIMITIVE_TYPE)
            #         pass
        return result

    def mutate(
        self,
        tree: Tree,
        node: Node,
        encoding: str = "utf8"
    ) -> Tree:
        mutations = self.mutations(
            self._parser,
            tree,
            node,
        )
        mutation: Mutation = choice(mutations)
        return mutation.apply(encoding)

    def mutations(
        self,
        parser: Parser,
        tree: Tree,
        node: Node
    ) -> List[Mutation]:
        mutations: List[Mutation] = list()
        candidates = self.capture(node)
        for candidate in candidates:
            mutation = WrappedMutation(
                parser, tree, candidate,
                "-(", ")"
            )
            mutations.append(mutation)
        return mutations