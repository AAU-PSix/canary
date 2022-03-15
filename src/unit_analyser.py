from typing import List
from ts import Language, Node


class UnitAnalyser:
    def __init__(self, language: Language, node: Node):
        self.language = language
        self.node = node

    def get_function_declarations(self) -> List[Node]:
        return self.language.query(
            self.language.syntax.query_function_declaration
        ).captures(self.node).nodes(self.language.syntax.get_function_declaration)

    def get_struct_declarations(self) -> List[Node]:
        return self.language.query(
            self.language.syntax.query_struct_declaration
        ).captures(self.node).nodes(self.language.syntax.get_function_declaration)

    def get_if_statements(self) -> List[Node]:
        return self.language.query(
            self.language.syntax.query_if_statement).captures(self.node).nodes(self.language.syntax.get_function_declaration)