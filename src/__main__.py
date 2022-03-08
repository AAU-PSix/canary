from ts import *

LanguageLibrary.build()
parser: Parser = Parser.create_with_language(LanguageLibrary.js())


tree: Tree = parser.parse("1>=3")
cursor: TreeCursor = tree.walk()
cursor.goto_first_child() # expression_statement
cursor.goto_first_child() # binary_expression
cursor.goto_first_child() # number: 1
node_1: Node = cursor.node
tree.edit(
  start_byte=node_1.start_byte,
  old_end_byte=node_1.end_byte,
  new_end_byte=node_1.start_byte + 1,
  start_point=node_1.start_point,
  old_end_point=node_1.start_point,
  new_end_point=FilePoint(node_1.start_point.line, node_1.start_byte)
)

new_tree: Tree = parser.parse("21>=3", tree)




#cursor = tree.walk()
#reached_root = False
#while not reached_root:
#  curr = cursor.node
#  print(curr.type)
#
#  if cursor.goto_first_child():
#    continue
#
#  if cursor.goto_next_sibling():
#    continue
#
#  retracing = True
#  while retracing:
#    if not cursor.goto_parent():
#      retracing = False
#      reached_root = True
#    
#    if cursor.goto_next_sibling():
#      retracing = False

