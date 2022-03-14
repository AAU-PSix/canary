import random
from ts import (
    Parser,
    Tree,
    Capture,
    Node,
)
from typing import List


class Mutator:
    def __init__(self, parser: Parser) -> None:
        self._parser = parser
        self._language = parser.language

    def mutate(
        self,
        tree: Tree,
        choose_randomly: bool = True,
        encoding: str = "utf8"
    ) -> Tree:
        if tree is None:
            raise Exception('Could not find tree')

        binary_expression_capture: Capture = self._language.query(
            self._language.syntax.query_binary_expression
        ).captures(tree.root_node)
        binary_expression_nodes: List[Node] = binary_expression_capture.nodes(
            self._language.syntax.get_binary_expression_operator
        )

        mutated_tree: Tree = tree

        node: Node = None
        if (choose_randomly): node = random.choice(binary_expression_nodes)
        else: node = binary_expression_nodes[0]
        mutated_tree = self.mutate_binary_operator(
            mutated_tree, node, encoding
        )
        binary_expression_nodes.remove(node)

        return mutated_tree

    def mutate_binary_operator(self, tree: Tree, node: Node, encoding: str = "utf8") -> Tree:
        if node.type is None:
            raise Exception(f'{Node.type} is null')
        if tree is None:
            raise Exception('Could not find tree')

        return tree.replace(self._parser, node, self.obom(node), encoding)

    def choose(self, collection: list, rnd: float = None) -> any:
        if rnd is None: rnd = random.random()
        else: rnd = max(min(rnd, 1), 0)
        index: int = int(rnd * len(collection))
        return collection[index]

    def random_operator_range(
        self,
        range: List[List[str]],
        rnd_range: float = None,
        rnd_operator: float = None
    ) -> str:
        range: List[str] = self.choose(range, rnd_range)
        return self.choose(range, rnd_operator)

    def obom(
        self,
        node: Node,
        rnd_range: float = None,
        rnd_operator: float = None
    ) -> str:
        """Obom is a mutant operator category

        Args:
            node (Node): the operator node
            rnd_range (float, optional): A [0,1) value denoting the desired range category. Defaults to None, then random.
            rnd_operator (float, optional): A [0,1) value denoting the desired operator in the range category. Defaults to None, then random.

        Returns:
            str: the replacement of the operator node
        """
        
        # Domain: Arithmetic assignment
        if node.type in self._language.syntax.arithmetic_compound_assignment:
            return self.random_operator_range(
                [
                    # OABA: a {+,-,*,/,%}= b -> a {|,&,^}= b
                    self._language.syntax.bitwise_compound_assignment,
                    # OAEA: a {+,-,*,/,%}= b -> a = b
                    self._language.syntax.plain_assignment,
                    # OASA: a {+,-,*,/,%}= b -> a {<<,>>}= b
                    self._language.syntax.shift_compound_assignment,
                ],
                rnd_range, rnd_operator
            )

        # Domain: Aritmetic operator
        if node.type in self._language.syntax.arithmetic_operators:
            return self.random_operator_range(
                [
                    # OABN: a {+,-,*,/,%} b -> a {|,&,^} b
                    self._language.syntax.bitwise_operators,
                    # OALN: a {+,-,*,/,%} b -> a {&&,||} b
                    self._language.syntax.logical_operators,
                    # OARN: a {+,-,*,/,%} b -> a {>,>=,<,<=,==,!=} b
                    self._language.syntax.relational_opearators,
                    # OASN: a {+,-,*,/,%} b -> a {<<,>>} b
                    self._language.syntax.shift_operators,
                ],
                rnd_range, rnd_operator
            )

        # Domain: Bitwise operator
        if node.type in self._language.syntax.bitwise_operators:
            return self.random_operator_range(
                [
                    # OBAN: a {|,&,^} b -> a {+,-,*,/,%} b
                    self._language.syntax.arithmetic_operators,
                    # OBLN: a {|,&,^} b -> a {&&,||} b
                    self._language.syntax.logical_operators,
                    # OBRN: a {|,&,^} b -> a {>,>=,<,<=,==,!=} b
                    self._language.syntax.relational_opearators,
                    # OBSN: a {|,&,^} b -> a {<<,>>} b
                    self._language.syntax.shift_operators,
                ],
                rnd_range, rnd_operator
            )

        # Domain: Bitwise assignment
        if node.type in self._language.syntax.bitwise_compound_assignment:
            return self.random_operator_range(
                [
                    # OBAA: a {|,&,^}= b -> a {+,-,*,/,%}= b
                    self._language.syntax.arithmetic_compound_assignment,
                    # OBEA: a {|,&,^}= b -> a = b
                    self._language.syntax.plain_assignment,
                    # OBSA: a {|,&,^}= b -> a {<<,>>}= b
                    self._language.syntax.shift_compound_assignment,
                ],
                rnd_range, rnd_operator
            )

        # Domain: Plain assignment
        if node.type in self._language.syntax.plain_assignment:
            return self.random_operator_range(
                [
                    # OEAA: a = b -> a {+,-,*,/,%}= b
                    self._language.syntax.arithmetic_compound_assignment,
                    # OEBA: a = b -> a {|,&,^}= b
                    self._language.syntax.bitwise_compound_assignment,
                    # OESA: a = b -> a {<<,>>}= b
                    self._language.syntax.shift_compound_assignment,
                ],
                rnd_range, rnd_operator
            )

        # Domain: Logical operator
        if node.type in self._language.syntax.logical_operators:
            return self.random_operator_range(
                [
                    # OLAN: a {&&,||} b -> a {+,-,*,/,%} b
                    self._language.syntax.arithmetic_operators,
                    # OLBN: a {&&,||} b -> a {|,&,^} b
                    self._language.syntax.bitwise_operators,
                    # OLRN: a {&&,||} b -> a {>,>=,<,<=,==,!=} b
                    self._language.syntax.relational_opearators,
                    # OLSN: a {&&,||} b -> a {<<,>>} b
                    self._language.syntax.shift_operators,
                    # OSLN: a {<<,>>}= b -> a {&&,||} b
                    self._language.syntax.logical_operators,
                ],
                rnd_range, rnd_operator
            )

        # Domain: Relational operator
        if node.type in self._language.syntax.relational_opearators:
            return self.random_operator_range(
                [
                    # ORAN: a {>,>=,<,<=,==,!=} b -> a {+,-,*,/,%} b
                    self._language.syntax.arithmetic_operators,
                    # ORBN: a {>,>=,<,<=,==,!=} b -> a {|,&,^} b
                    self._language.syntax.bitwise_operators,
                    # ORLN: a {>,>=,<,<=,==,!=} b -> a {&&,||} b
                    self._language.syntax.logical_operators,
                    # ORSN: a {>,>=,<,<=,==,!=} b -> a {<<,>>} b
                    self._language.syntax.shift_operators,
                ],
                rnd_range, rnd_operator
            )

        # Domain: Shift assignment
        if node.type in self._language.syntax.shift_compound_assignment:
            return self.random_operator_range(
                [
                    # OSAA: a {<<,>>}= b -> a {+,-,*,/,%}= b
                    self._language.syntax.arithmetic_compound_assignment,
                    # OSBA: a {<<,>>}= b -> a {|,&,^}= b
                    self._language.syntax.bitwise_compound_assignment,
                    # OSEA: a {<<,>>}= b -> a = b
                    self._language.syntax.plain_assignment,
                ],
                rnd_range, rnd_operator
            )

        # Domain: Shift operator
        if node.type in self._language.syntax.shift_operators:
            return self.random_operator_range(
                [
                    # OSAN: a {<<,>>} b -> a {+,-,*,/,%} b
                    self._language.syntax.arithmetic_operators,
                    # OSBN: a {<<,>>} b -> a {|,&,^} b
                    self._language.syntax.bitwise_operators,
                    # OSRN: a {<<,>>} b -> a {>,>=,<,<=,==,!=} b
                    self._language.syntax.relational_opearators,
                ],
                rnd_range, rnd_operator
            )