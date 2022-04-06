from ts import Node, Tree
from typing import List

from .ast_formal_parameter import FormalParameter

class FunctionDeclaration:
    def __init__(
        self,
        name: str,
        return_type: str,
        formal_parameters: List[FormalParameter]
    ) -> None:
        self._name = name
        self._return_type = return_type
        self._formal_parameters = formal_parameters

    @property
    def name(self) -> str:
        return self._name

    @property
    def return_type(self) -> str:
        return self._return_type

    @property
    def formal_parameters(self) -> List[FormalParameter]:
        return self._formal_parameters

    @staticmethod
    def create_c(tree: Tree, node: Node) -> "FunctionDeclaration":
        return_type_node: Node = node.child_by_field_name("type")
        return_type: str = tree.contents_of(return_type_node)

        formal_parameters: List[FormalParameter] = list()
        declarator_node: Node = node.child_by_field_name("declarator")

        function_name_node: Node = declarator_node.child_by_field_name("declarator")
        function_name: str = tree.contents_of(function_name_node)

        parameter_list: Node = declarator_node.child_by_field_name("parameters")
        for parameter_declaration in parameter_list.named_children:
            parameter_type_node = parameter_declaration.child_by_field_name("type")
            parameter_identifier_node = parameter_declaration.child_by_field_name("declarator")

            formal_type: str = tree.contents_of(parameter_type_node)
            formal_identifier = tree.contents_of(parameter_identifier_node)

            parameter_declarator_node: Node = parameter_declaration.child_by_field_name("declarator")
            while parameter_declarator_node.type == "pointer_declarator":
                formal_type += "*"
                parameter_declarator_node = parameter_declarator_node.named_children[0]

            formal_parameters.append(
                FormalParameter(formal_identifier, formal_type)
            )

        return FunctionDeclaration(
            function_name, return_type, formal_parameters
        )
