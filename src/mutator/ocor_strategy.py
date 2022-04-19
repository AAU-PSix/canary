import random
from typing import List
from ts import Tree, Node, NodeType, CSyntax, Parser, Capture
from .mutation_strategy import MutationStrategy

class OcorStrategy(MutationStrategy):
    def __init__(self, parser: Parser) -> None:
        self._parser = parser
        self._language = parser.language
        self._syntax = CSyntax()
    
    def capture(self, node: Node) -> List[Node]:
        binary_expression_capture: Capture = self._language.query(
            self._syntax.binary_expression_query
        ).captures(node)
        binary_expression_nodes: List[Node] = binary_expression_capture.nodes(
            self._syntax.get_binary_expression_operator
        )
        
        binary_expression_nodes = list(
            filter(
                lambda x: not x.type == "=",
                binary_expression_nodes
            )
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
            tree, node, self.ocor(node).value, encoding
        )

    def choose(self, collection: list, rnd: float = None) -> any:
        if rnd is None: rnd = random.random()
        else: rnd = max(min(rnd, 1), 0)
        index: int = int(rnd * len(collection))
        return collection[index]

    def random_operator_range(
        self,
        range: List[List[NodeType]],
        rnd_range: float = None,
        rnd_operator: float = None
    ) -> NodeType:
        range: List[NodeType] = self.choose(range, rnd_range)
        return self.choose(range, rnd_operator)

    def ocor(
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
                str: the replacement of the operator node
            """

            # Domain: Arithmetic assignment
            if self._syntax.in_types(node.type, self._syntax.arithmetic_compound_assignment):
                return self.random_operator_range(
                    [
                        # OAAA: a {+,-,*,/,%}= b -> a {+,-,*,/,%}= b
                        self._syntax.arithmetic_compound_assignment,
                    ],
                    rnd_range, rnd_operator
                )

            # Domain: Arithmetic
            if self._syntax.in_types(node.type, self._syntax.arithmetic_operators):
                return self.random_operator_range(
                    [
                        # OAAN: a {+,-,*,/,%} b -> a {+,-,*,/,%} b
                        self._syntax.arithmetic_operators,
                    ],
                    rnd_range, rnd_operator
                )

            # Domain: Bitwise assignment
            if self._syntax.in_types(node.type, self._syntax.bitwise_compound_assignment):
                return self.random_operator_range(
                    [
                        # OBBA: a {|,&,^}= b -> a {|,&,^}= b
                        self._syntax.bitwise_compound_assignment,
                    ],
                    rnd_range, rnd_operator
                )

            # Domain: Bitwise
            if self._syntax.in_types(node.type, self._syntax.bitwise_operators):
                return self.random_operator_range(
                    [
                        # OBBN: a {|,&,^} b -> a {|,&,^} b
                        self._syntax.bitwise_operators,
                    ],
                    rnd_range, rnd_operator
                )
            
            # Domain: Logical
            if self._syntax.in_types(node.type, self._syntax.logical_operators):
                return self.random_operator_range(
                    [
                        # OLLN: a {&&,||} b -> a {&&,||} b
                        self._syntax.logical_operators,
                    ],
                    rnd_range, rnd_operator
                )

            # Domain: Relational
            if self._syntax.in_types(node.type, self._syntax.relational_opearators):
                return self.random_operator_range(
                    [
                        # ORRN: a {>,>=,<,<=,==,!=} b -> a {>,>=,<,<=,==,!=} b
                        self._syntax.relational_opearators,
                    ],
                    rnd_range, rnd_operator
                )   
           
            # Domain: Shift assignment
            if self._syntax.in_types(node.type, self._syntax.shift_compound_assignment):
                return self.random_operator_range(
                    [
                        # OSSA: a {<<,>>}= b -> a {<<,>>}= b
                        self._syntax.shift_compound_assignment,
                    ],
                    rnd_range, rnd_operator
                )

            # Domain: Shift
            if self._syntax.in_types(node.type, self._syntax.shift_operators):
                return self.random_operator_range(
                    [
                        # OSSN: a {<<,>>} b -> a {<<,>>} b
                        self._syntax.shift_operators,
                    ],
                    rnd_range, rnd_operator
                )
