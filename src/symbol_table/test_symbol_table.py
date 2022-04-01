import unittest
from typing import List

from . import (
    LexicalSymbolTable,
    LexicalSymbolTabelBuilder,
    PrimitiveType,
)

class TestSymbolTable(unittest.TestCase):
    def test_root_children_siblings(self) -> None:
        root_children: List[LexicalSymbolTable] = [ ]
        root_table = LexicalSymbolTable(None, root_children)
        # Two different approaches of appending a child
        root_table.children.append(LexicalSymbolTable(root_table, list()))
        root_children.append(LexicalSymbolTable(root_table, list()))
        root_children.append(LexicalSymbolTable(root_table, list()))

        self.assertEqual(root_table.child_count, 3)
        self.assertEqual(root_table.children, root_children)
        self.assertEqual(root_table.first_child, root_children[0])
        self.assertEqual(root_table.last_child, root_children[-1])

        self.assertEqual(root_children[0].sibling_count, 3)
        self.assertEqual(root_children[0].next_sibling, root_children[1])
        self.assertEqual(root_children[1].previous_sibling, root_children[0])
        self.assertEqual(root_children[0].siblings, root_table.children)
        self.assertEqual(root_children[1].siblings, root_table.children)
        self.assertEqual(root_children[2].siblings, root_table.children)

    def test_symbol_table_builder(self) -> None:
        builder = LexicalSymbolTabelBuilder()
        builder.open()
        builder.close()
        builder.open()
        builder.close()
        builder.open()
        builder.close()

        root = builder.build().root

        self.assertEqual(root.child_count, 3)
        self.assertEqual(root.first_child.sibling_count, 3)
        self.assertEqual(root.first_child, root.children[0])
        self.assertEqual(root.last_child, root.children[-1])
        self.assertEqual(root.children[0].next_sibling, root.children[1])
        self.assertEqual(root.children[1].previous_sibling, root.children[0])

    def test_lookup(self) -> None:
        builder = LexicalSymbolTabelBuilder()
        type_int = PrimitiveType("int")
        type_double = PrimitiveType("double")
        builder.enter("foo", type_int, 0)
        builder.open()
        builder.enter("bar", type_double, 1)
        builder.close()

        root: LexicalSymbolTable = builder.build().root
        child = root.first_child

        self.assertEqual(root.child_count, 1)
        self.assertEqual(child.sibling_count, 1)
        self.assertEqual(root.lookup("foo"), type_int)
        self.assertTrue(root.has("foo"))
        self.assertEqual(root.lookup("bar"), None)
        self.assertFalse(root.has("bar"))
        # Only the child has access to both types
        self.assertEqual(child.lookup("foo"), type_int)
        self.assertTrue(child.has("foo"))
        self.assertEqual(child.lookup("bar"), type_double)
        self.assertTrue(child.has("bar"))

    def test_lexical_traversal_trivial_child(self) -> None:
        #       1
        #      /|\
        #     0-o-o
        # 0: Is the start
        # [0-2]: Is the traversed
        #   tables and their order.
        builder = LexicalSymbolTabelBuilder()
        builder.open().close() # 0
        builder.open().close() # o
        builder.open().close() # o

        tree = builder.build()
        root = tree.root
        start = root.children[0]

        traversal = [ *start.lexical_traversal() ]
        table_0 = root.children[0]
        table_1 = root

        self.assertEqual(len(traversal), 2)
        self.assertEqual(table_0, traversal[0])
        self.assertEqual(table_1, traversal[1])

    def test_lexical_traversal_simple_tree(self) -> None:
        #       2
        #      /|\
        #     1-0-o
        # 0: Is the start
        # [0-2]: Is the traversed
        #   tables and their order.
        builder = LexicalSymbolTabelBuilder()
        builder.open().close() # 1
        builder.open().close() # 0
        builder.open().close() # o

        tree = builder.build()
        root = tree.root
        start = root.children[1]

        traversal = [ *start.lexical_traversal() ]
        table_0 = root.children[1]
        table_1 = root.children[0]
        table_2 = root

        self.assertEqual(len(traversal), 3)
        self.assertEqual(table_0, traversal[0])
        self.assertEqual(table_1, traversal[1])
        self.assertEqual(table_2, traversal[2])

    def test_lexical_traversal_disjoint_children(self) -> None:
        #       5
        #      /|\
        #     4-2-o
        #    / / \ \
        #   3  1-0  o
        # 0: Is the start
        # [0-5]: Is the traversed
        #   tables and their order.
        builder = LexicalSymbolTabelBuilder()
        builder.open()  # 4
        builder.open()  # | 3
        builder.close() # | |
        builder.close() # |

        builder.open()  # 2
        builder.open()  # | 1
        builder.close() # | |
        builder.open()  # | 0
        builder.close() # | |
        builder.close() # |

        builder.open()  # o
        builder.open()  # | o
        builder.close() # | |
        builder.close() # |

        tree = builder.build()
        root = tree.root
        start = root.children[1].children[1]

        traversal = [ *start.lexical_traversal() ]
        table_0 = root.children[1].children[1]
        table_1 = root.children[1].children[0]
        table_2 = root.children[1]
        table_3 = root.children[0].children[0]
        table_4 = root.children[0]
        table_5 = root

        self.assertEqual(len(traversal), 6)
        self.assertEqual(table_0, traversal[0])
        self.assertEqual(table_1, traversal[1])
        self.assertEqual(table_2, traversal[2])
        self.assertEqual(table_3, traversal[3])
        self.assertEqual(table_4, traversal[4])
        self.assertEqual(table_5, traversal[5])

    def test_get(self) -> None:
        builder = LexicalSymbolTabelBuilder()
        type_int = PrimitiveType("int")
        builder.open()
        builder.enter("foo", type_int, 0)
        builder.close()
        builder.open()
        builder.enter("bar", type_int, 1)
        builder.close()

        root: LexicalSymbolTable = builder.build().root
        first_child = root.children[0]
        last_child = root.children[1]

        first_identifiers = first_child.identifiers()
        last_identifiers = last_child.identifiers()

        self.assertEqual(len(first_identifiers), 1)
        self.assertTrue("foo" in first_identifiers)
        self.assertEqual(len(last_identifiers), 2)
        self.assertTrue("foo" in last_identifiers)
        self.assertTrue("bar" in last_identifiers)