import re
from src.ts.ts import LanguageLibrary, Node, Query


class QueryApi:
    @staticmethod
    def findFunctionDeclarations(node: Node):
        query: Query = LanguageLibrary.c().query("( (function_declarator)) @dec "
                                                 "(function_definition (pointer_declarator)) @voidDec")
        declarations = query.captures(node)
        result = []
        for node_string_tuple in declarations:
            result.append(node_string_tuple[0])  # Get node of tuple
        return result

    @staticmethod
    def findStructDeclaration(node: Node):
        query: Query = LanguageLibrary.c().query("(struct_specifier ) @struct")

        declarations = query.captures(node)
        result = []
        for node_string_tuple in declarations:
            result.append(node_string_tuple[0])  # Get node of tuple
        return result