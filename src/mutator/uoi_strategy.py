from random import choice
from typing import List
from ts import Tree, Node, CNodeType, NodeType, CSyntax, Parser
from .mutation_strategy import MutationStrategy
from .mutation import Mutation, ReplacementMutation, WrappedMutation

class UoiStrategy(MutationStrategy):
    def __init__(self, parser: Parser) -> None:
        self._parser = parser
        self._language = parser.language
        self._syntax = CSyntax()

    def capture(self, node: Node) -> List[Node]:
        query_capture = self._language.query(
            self._syntax.update_expression_query + \
            self._syntax.unary_expression_query
        ).captures(node)
        
        nodes: List[Node] = query_capture.nodes()
        result: List[Node] = list()
        for node in nodes:
            if node.is_type(CNodeType.UNARY_EXPRESSION) and \
                node.children[0].is_either_type(self._syntax.arithmetic_unary_operators) or \
                node.children[0].is_either_type(self._syntax.logical_unary_operators):
                if node not in result: result.append(node.children[0])
            if node.is_type(CNodeType.UPDATE_EXPRESSION):
                if node not in result: result.append(node.children[0])
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
            replacement_types: List[NodeType] = list()
            if candidate.is_either_type(self._syntax.arithmetic_unary_operators):
                for type in self._syntax.arithmetic_unary_operators:
                    if not candidate.is_type(type): replacement_types.append(type)
            elif candidate.is_either_type(self._syntax.logical_unary_operators):
                for type in self._syntax.logical_unary_operators:
                    if type not in replacement_types: replacement_types.append(type)
            elif candidate.is_either_type(self._syntax.update_expression_operators):
                for type in self._syntax.update_expression_operators:
                    if not candidate.is_type(type): replacement_types.append(type)
            for replacement in replacement_types:
                if replacement.value == CNodeType.Logical_NOT.value:
                    mutations.append(
                        ReplacementMutation(
                            parser, tree, candidate, ""
                        )
                    )
                else:
                    mutations.append(
                        ReplacementMutation(
                            parser, tree, candidate, replacement.value
                        )
                    )
        return mutations