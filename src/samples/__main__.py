from mutator import *
from ts import *

LanguageLibrary.build()
parser: Parser = Parser.create_with_language(LanguageLibrary.js())

tree: Tree = parser.parse("1>=3")
print("\n" + tree.text) # '1>=3'

cursor: TreeCursor = tree.walk()
cursor.goto_first_child() # expression_statement
cursor.goto_first_child() # binary_expression
cursor.goto_first_child() # number: 1
node_1: Node = cursor.node

print("\n" + tree.contents_of(node_1)) # '1'

tree_str_replaced: Tree = tree.replace(parser, node_1, "asd")
print("\n" + tree_str_replaced.text) # 'asd>=3'

tree_line_inserted: Tree = tree.insert_line(parser, 0, "canary()")
print("\n" + tree_line_inserted.text) # 'canary() \n 1>=3'

tree_line_inserted: Tree = tree.append_line(parser, 0, "canary()")
print("\n" + tree_line_inserted.text) # '1>=3 \n canary()'

cursor: TreeCursor = tree.walk()
curr: Node
print("\n")
for curr in cursor.pre_order_traverse():
  print(curr.type) # 'program', 'expression_statement', ...

tree_from_lines: Tree = parser.parse_lines([ "a>b", "b<c" ])
print("\n" + tree_from_lines.text) # 'a>b \n b<c'

simple_tree: Tree = parser.parse_lines(["1+2", "2+3"])
print(simple_tree.root_node.sexp) # '(program (...'
query: Query = LanguageLibrary.js().query("(binary_expression) @left @right")
captures: Capture = query.captures(simple_tree.root_node)
print(captures)

print("\n")
mutation_tree: Tree = parser.parse_lines(
  [
    "console.log(1+2)",
    "1+'asd'"
  ]
)

query: Query = LanguageLibrary.js().query("(binary_expression (number) @left (number))")

mutator: Mutator = Mutator(parser)
mutated_tree: Tree = mutator.mutate(mutation_tree, mutation_tree.root_node, query)
print(mutated_tree.text)

# mutation_cursor: TreeCursor = mutation_tree.walk()
# mutation_cursor.goto_first_child() # expression_statement
# mutation_cursor.goto_first_child() # binary_expression
# mutation_cursor.goto_first_child() # number
# mutation_cursor.goto_next_sibling() # +
# plus_node: Node = mutation_cursor.node
# print(plus_node.type)
# 
# mutation_analyser: MutationAnalyser = MutationAnalyser(parser)
# mutated_tree: Tree = mutation_analyser.mutate(mutation_tree, plus_node)
# print(mutated_tree.text)
