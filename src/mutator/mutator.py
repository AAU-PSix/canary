
from random import choice
from .obom_strategy import MutationStrategy
from ts import (
    Parser,
    Tree,
    Node,
)
from ts.c_syntax import CSyntax

class Mutator:
    def __init__(self, parser: Parser) -> None:
        self._parser = parser
        self._language = parser.language
        self._syntax = CSyntax()

    def mutate(
        self,
        tree: Tree,
        node: Node,
        strategy: MutationStrategy,
        encoding: str = "utf8"
    ) -> Tree:
        if tree is None:
            raise Exception('Could not find tree')
        
        candidates = strategy.capture(node)
        mutated_tree = strategy.mutate(tree, choice(candidates), encoding)
        return mutated_tree