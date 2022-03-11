import random
from ts import *

class MutationAnalyser:
    def __init__(self, parser: Parser) -> None:
        self._parser = parser

    def mutate(self, tree: Tree, unit: Node, query: Query, encoding: str = "utf8") -> Tree:

        if query is None:
            raise Exception(f'{query} is an invalid query')
        if tree is None:
            raise Exception('Could not find tree')
        if unit is None:
            raise Exception(f'{unit} is an invalid unit')

        captures: List[Tuple[Node, str]] = query.captures(unit)
        return self.mutate_binary_operator(tree, captures[0][0].next_sibling, encoding)

    def mutate_binary_operator(self, tree: Tree, node: Node, encoding: str = "utf8") -> Tree:

        if node.type is None:
            raise Exception(f'{Node.type} is null')
        if tree is None:
            raise Exception('Could not find tree')

        return tree.replace(self._parser, node, self.random_binary_operator(node), encoding)

    def random_binary_operator(self, node: Node) -> str:

        binary_operators = ["+", "-", "*", "/", "%", "||", "&&", "|", "^",
                            "&", "==", "!=", ">", ">=", "<=", "<", "<<", ">>"]

        if node.type is None:
            raise Exception(f'{node.type} is null')
       
        if node.type not in binary_operators:
            raise Exception(f'{node.type}is not in the set of binary operators')

        binary_operators.remove(node.type)

        return random.choice(binary_operators)

