from typing import List
from src.ts.ts import Capture, LanguageLibrary, Node, Query


class QueryApi:
    @staticmethod
    def findFunctionDeclarations(node: Node) -> List[Node]:
        query: Query = LanguageLibrary.c().query("(function_definition (function_declarator)) @dec "
                                                 "(function_definition (pointer_declarator)) @voidDec")
        declarations: Capture = query.captures(node)
        result: List[Node] = []
        for node_string_tuple in declarations:
            result.append(node_string_tuple[0])  # Get node of tuple
        return result

    @staticmethod
    def findStructDeclaration(node: Node) -> List[Node]:
        query: Query = LanguageLibrary.c().query("(struct_specifier ) @struct")

        declarations: Capture = query.captures(node)
        result: List[Node] = []
        for node_string_tuple in declarations:
            result.append(node_string_tuple[0])  # Get node of tuple
        return result