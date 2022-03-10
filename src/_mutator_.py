from ts import *

LanguageLibrary.build()
parser: Parser = Parser.create_with_language(LanguageLibrary.js())

print("-----------------------------------------")
simple_tree: Tree = parser.parse("function hejsa1(){let a = 1+1;} function hejsa2(){let a =2+2;}")
query: Query = LanguageLibrary.js().query("""
(binary_expression
    (number) @left
    (number)) @right
""")
captures = query.captures(simple_tree.root_node)
print(captures)