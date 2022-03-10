import re
from src.ts.ts import LanguageLibrary, Node, Query

def findFunctionDeclarations(node: Node):
  query: Query = LanguageLibrary.c().query("(function_definition (primitive_type) (function_declarator)) @dec")
  declarations = query.captures(node)
  result=[]
  for tuple in declarations:
    result.append(tuple[0])

  return result  