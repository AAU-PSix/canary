from ts import *

class MutationAnalyser:
    def __init__(self, parser: Parser) -> None:
        self._parser = parser

    def mutate(self, tree: Tree, unit: Node, encoding: str = "utf8") -> Tree:
        query: Query = LanguageLibrary.js().query("(binary_expression (number) @left (number))")
        captures: List[Tuple[Node, str]] = query.captures(unit)
        print(captures)
        return self.mutate_operator(tree, captures[0][0].next_sibling, encoding)

    def mutate_operator(self, tree: Tree, node: Node, encoding: str = "utf8") -> Tree:
        if node.type == "+":
            return tree.replace(self._parser, node, "-", encoding)