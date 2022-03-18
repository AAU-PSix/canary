from ts import Node, Tree
from typing import List

class FunctionDeclaration:
    def __init__(
        self,
        return_type: str,
        formal_parameters: List[str]
    ) -> None:
        self._return_type = return_type
        self._formal_parameters = formal_parameters

    @property
    def return_type(self) -> str:
        return self._return_type

    @property
    def formal_parameters(self) -> List[str]:
        return self._formal_parameters

    @staticmethod
    def create_c(tree: Tree, node: Node) -> "FunctionDeclaration":
        return_type_node: Node = node.child_by_field_name("type")
        return_type: str = tree.contents_of(return_type_node)
        
        formal_parameters: List[str] = list()
        declarator_node: Node = node.child_by_field_name("declarator")

        parameter_list: Node = declarator_node.child_by_field_name("parameters")
        for parameter_declaration in parameter_list.named_children:
            parameter_type_node = parameter_declaration.child_by_field_name("type")
            formal_parameters.append(tree.contents_of(parameter_type_node))

        return FunctionDeclaration(
            return_type, formal_parameters
        )