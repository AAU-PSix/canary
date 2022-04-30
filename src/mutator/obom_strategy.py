from typing import List
from ts import Tree, Node, NodeType, CSyntax, Parser
from .mutation_strategy import MutationStrategy
from .mutation import Mutation, ReplacementMutation

class ObomStrategy(MutationStrategy):
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
        return binary_expression_nodes

    def mutate(
        self,
        tree: Tree,
        node: Node,
        encoding: str = "utf8"
    ) -> Tree:
        if node.type is None:
            raise Exception(f'{Node.type} is null')
        if tree is None:
            raise Exception('Could not find tree')

        return self._parser.replace(
            tree, node, self.obom(node).value, encoding
        )

    def mutations(
        self,
        parser: Parser,
        tree: Tree,
        node: Node
    ) -> List[Mutation]:
        replacement_types: List[NodeType] = list()

        # Domain: Arithmetic assignment
        if self._syntax.in_types(node.type, self._syntax.arithmetic_compound_assignment):
            replacement_types.extend(self._syntax.bitwise_compound_assignment)
            replacement_types.extend(self._syntax.plain_assignment)
            replacement_types.extend(self._syntax.shift_compound_assignment)

        # Domain: Aritmetic operator
        if self._syntax.in_types(node.type, self._syntax.arithmetic_operators):
            replacement_types.extend(self._syntax.bitwise_operators)
            replacement_types.extend(self._syntax.logical_operators)
            replacement_types.extend(self._syntax.relational_operators)
            replacement_types.extend(self._syntax.shift_operators)

        # Domain: Bitwise operator
        if self._syntax.in_types(node.type, self._syntax.bitwise_operators):
            replacement_types.extend(self._syntax.arithmetic_operators)
            replacement_types.extend(self._syntax.logical_operators)
            replacement_types.extend(self._syntax.relational_operators)
            replacement_types.extend(self._syntax.shift_operators)

        # Domain: Bitwise assignment
        if self._syntax.in_types(node.type, self._syntax.bitwise_compound_assignment):
            replacement_types.extend(self._syntax.arithmetic_compound_assignment)
            replacement_types.extend(self._syntax.plain_assignment)
            replacement_types.extend(self._syntax.shift_compound_assignment)

        # Domain: Plain assignment
        if self._syntax.in_types(node.type, self._syntax.plain_assignment):
            replacement_types.extend(self._syntax.arithmetic_compound_assignment)
            replacement_types.extend(self._syntax.bitwise_compound_assignment)
            replacement_types.extend(self._syntax.shift_compound_assignment)

        # Domain: Logical operator
        if self._syntax.in_types(node.type, self._syntax.logical_operators):
            replacement_types.extend(self._syntax.arithmetic_operators)
            replacement_types.extend(self._syntax.bitwise_operators)
            replacement_types.extend(self._syntax.relational_operators)
            replacement_types.extend(self._syntax.shift_operators)
            replacement_types.extend(self._syntax.logical_operators)

        # Domain: Relational operator
        if self._syntax.in_types(node.type, self._syntax.relational_operators):
            replacement_types.extend(self._syntax.arithmetic_operators)
            replacement_types.extend(self._syntax.bitwise_operators)
            replacement_types.extend(self._syntax.logical_operators)
            replacement_types.extend(self._syntax.shift_operators)

        # Domain: Shift assignment
        if self._syntax.in_types(node.type, self._syntax.shift_compound_assignment):
            replacement_types.extend(self._syntax.arithmetic_compound_assignment)
            replacement_types.extend(self._syntax.bitwise_compound_assignment)
            replacement_types.extend(self._syntax.plain_assignment)

        # Domain: Shift operator
        if self._syntax.in_types(node.type, self._syntax.shift_operators):
            replacement_types.extend(self._syntax.arithmetic_operators)
            replacement_types.extend(self._syntax.bitwise_operators)
            replacement_types.extend(self._syntax.relational_operators)

        mutations: List[Mutation] = list()
        for type in replacement_types:
            mutations.append(
                ReplacementMutation(
                    parser,
                    tree,
                    node,
                    type.value
                )
            )
        return mutations

    def obom(
            self,
            node: Node,
            rnd_range: float = None,
            rnd_operator: float = None
        ) -> NodeType:
            """Obom is a mutant operator category

            Args:
                node (Node): the operator node
                rnd_range (float, optional): A [0,1) value denoting the desired range category. Defaults to None, then random.
                rnd_operator (float, optional): A [0,1) value denoting the desired operator in the range category. Defaults to None, then random.

            Returns:
                NodeType: the replacement of the operator node
            """

            # Domain: Arithmetic assignment
            if self._syntax.in_types(node.type, self._syntax.arithmetic_compound_assignment):
                return self.random_operator_range(
                    [
                        # OABA: a {+,-,*,/,%}= b -> a {|,&,^}= b
                        self._syntax.bitwise_compound_assignment,
                        # OAEA: a {+,-,*,/,%}= b -> a = b
                        self._syntax.plain_assignment,
                        # OASA: a {+,-,*,/,%}= b -> a {<<,>>}= b
                        self._syntax.shift_compound_assignment,
                    ],
                    rnd_range, rnd_operator
                )

            # Domain: Aritmetic operator
            if self._syntax.in_types(node.type, self._syntax.arithmetic_operators):
                return self.random_operator_range(
                    [
                        # OABN: a {+,-,*,/,%} b -> a {|,&,^} b
                        self._syntax.bitwise_operators,
                        # OALN: a {+,-,*,/,%} b -> a {&&,||} b
                        self._syntax.logical_operators,
                        # OARN: a {+,-,*,/,%} b -> a {>,>=,<,<=,==,!=} b
                        self._syntax.relational_operators,
                        # OASN: a {+,-,*,/,%} b -> a {<<,>>} b
                        self._syntax.shift_operators,
                    ],
                    rnd_range, rnd_operator
                )

            # Domain: Bitwise operator
            if self._syntax.in_types(node.type, self._syntax.bitwise_operators):
                return self.random_operator_range(
                    [
                        # OBAN: a {|,&,^} b -> a {+,-,*,/,%} b
                        self._syntax.arithmetic_operators,
                        # OBLN: a {|,&,^} b -> a {&&,||} b
                        self._syntax.logical_operators,
                        # OBRN: a {|,&,^} b -> a {>,>=,<,<=,==,!=} b
                        self._syntax.relational_operators,
                        # OBSN: a {|,&,^} b -> a {<<,>>} b
                        self._syntax.shift_operators,
                    ],
                    rnd_range, rnd_operator
                )

            # Domain: Bitwise assignment
            if self._syntax.in_types(node.type, self._syntax.bitwise_compound_assignment):
                return self.random_operator_range(
                    [
                        # OBAA: a {|,&,^}= b -> a {+,-,*,/,%}= b
                        self._syntax.arithmetic_compound_assignment,
                        # OBEA: a {|,&,^}= b -> a = b
                        self._syntax.plain_assignment,
                        # OBSA: a {|,&,^}= b -> a {<<,>>}= b
                        self._syntax.shift_compound_assignment,
                    ],
                    rnd_range, rnd_operator
                )

            # Domain: Plain assignment
            if self._syntax.in_types(node.type, self._syntax.plain_assignment):
                return self.random_operator_range(
                    [
                        # OEAA: a = b -> a {+,-,*,/,%}= b
                        self._syntax.arithmetic_compound_assignment,
                        # OEBA: a = b -> a {|,&,^}= b
                        self._syntax.bitwise_compound_assignment,
                        # OESA: a = b -> a {<<,>>}= b
                        self._syntax.shift_compound_assignment,
                    ],
                    rnd_range, rnd_operator
                )

            # Domain: Logical operator
            if self._syntax.in_types(node.type, self._syntax.logical_operators):
                return self.random_operator_range(
                    [
                        # OLAN: a {&&,||} b -> a {+,-,*,/,%} b
                        self._syntax.arithmetic_operators,
                        # OLBN: a {&&,||} b -> a {|,&,^} b
                        self._syntax.bitwise_operators,
                        # OLRN: a {&&,||} b -> a {>,>=,<,<=,==,!=} b
                        self._syntax.relational_operators,
                        # OLSN: a {&&,||} b -> a {<<,>>} b
                        self._syntax.shift_operators,
                        # OSLN: a {<<,>>}= b -> a {&&,||} b
                        self._syntax.logical_operators,
                    ],
                    rnd_range, rnd_operator
                )

            # Domain: Relational operator
            if self._syntax.in_types(node.type, self._syntax.relational_operators):
                return self.random_operator_range(
                    [
                        # ORAN: a {>,>=,<,<=,==,!=} b -> a {+,-,*,/,%} b
                        self._syntax.arithmetic_operators,
                        # ORBN: a {>,>=,<,<=,==,!=} b -> a {|,&,^} b
                        self._syntax.bitwise_operators,
                        # ORLN: a {>,>=,<,<=,==,!=} b -> a {&&,||} b
                        self._syntax.logical_operators,
                        # ORSN: a {>,>=,<,<=,==,!=} b -> a {<<,>>} b
                        self._syntax.shift_operators,
                    ],
                    rnd_range, rnd_operator
                )

            # Domain: Shift assignment
            if self._syntax.in_types(node.type, self._syntax.shift_compound_assignment):
                return self.random_operator_range(
                    [
                        # OSAA: a {<<,>>}= b -> a {+,-,*,/,%}= b
                        self._syntax.arithmetic_compound_assignment,
                        # OSBA: a {<<,>>}= b -> a {|,&,^}= b
                        self._syntax.bitwise_compound_assignment,
                        # OSEA: a {<<,>>}= b -> a = b
                        self._syntax.plain_assignment,
                    ],  
                    rnd_range, rnd_operator
                )

            # Domain: Shift operator
            if self._syntax.in_types(node.type, self._syntax.shift_operators):
                return self.random_operator_range(
                    [
                        # OSAN: a {<<,>>} b -> a {+,-,*,/,%} b
                        self._syntax.arithmetic_operators,
                        # OSBN: a {<<,>>} b -> a {|,&,^} b
                        self._syntax.bitwise_operators,
                        # OSRN: a {<<,>>} b -> a {>,>=,<,<=,==,!=} b
                        self._syntax.relational_operators,
                    ],
                    rnd_range, rnd_operator
                )