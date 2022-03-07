from tree_sitter import Language, Parser

Language.build_library(
  # Store the library in the `build` directory
  'build/my-languages.so',

  # Include one or more languages
  [
    'vendor/tree-sitter-javascript'
  ]
)
JS_LANGUAGE = Language('build/my-languages.so', 'javascript')

parser = Parser()
parser.set_language(JS_LANGUAGE)

tree = parser.parse(bytes("console.log(\"Hello, World\");\n 1+2", "utf8"))
print(tree)
cursor = tree.walk()
print(cursor)

print(tree.root_node.sexp())

class Node:
  _obj
  
  def __init__(self, obj):
    self._obj = obj

reached_root = False
while not reached_root:
  curr = cursor.node
  print(curr)
  print(curr.type)
  print(curr.start_point)
  print(curr.start_byte)
  print(curr.end_point)
  print(curr.end_byte)

  if cursor.goto_first_child():
    continue

  if cursor.goto_next_sibling():
    continue

  retracing = True
  while retracing:
    if not cursor.goto_parent():
      retracing = False
      reached_root = True
    
    if cursor.goto_next_sibling():
      retracing = False

print("Hello, World!")

