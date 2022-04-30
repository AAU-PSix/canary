from random import choice
from typing import List
from ts import Tree, Node, NodeType, CSyntax, Parser
from .mutation_strategy import MutationStrategy
from .mutation import Mutation, ReplacementMutation, WrappedMutation

class RorStrategy(MutationStrategy):
    def __init__(self, parser: Parser) -> None:
        self._parser = parser
        self._language = parser.language
        self._syntax = CSyntax()

    def capture(self, node: Node) -> List[Node]:
        binary_expression_capture = self._language.query(
            self._syntax.binary_expression_query
        ).captures(node)
        binary_expression_nodes: List[Node] = binary_expression_capture.nodes(
            self._syntax.get_binary_expression_operator
        )
        return list(
            filter(
                lambda x: x.is_either_type(self._syntax.relational_operators),
                binary_expression_nodes
            )
        )

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
            for type in self._syntax.relational_operators:
                if type.value != candidate.type: replacement_types.append(type)
            for replacement in replacement_types:
                mutations.append(ReplacementMutation(
                    parser, tree, candidate, replacement.value
                ))
        return mutations