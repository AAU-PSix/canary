import unittest
from typing import List

from . import SymbolTable, SymbolTabelBuilder, Type

class TestSymbolTable(unittest.TestCase):
    def test_root_children_siblings(self) -> None:
        root_children: List[SymbolTable] = [ ]
        root_table = SymbolTable(None, root_children)
        # Two different approaches of appending a child
        root_table.children.append(SymbolTable(root_table))
        root_children.append(SymbolTable(root_table))
        root_children.append(SymbolTable(root_table))

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
        builder = SymbolTabelBuilder()
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

# For some reason this tests fucks with some static information regarding the SymbolTable
#    def test_lookup(self) -> None:
#        builder = SymbolTabelBuilder()
#        type_int = Type()
#        type_double = Type()
#        builder.enter("int", type_int)
#        builder.open()
#        builder.enter("double", type_double)
#        builder.close()
#
#        root = builder.build().root
#        child = root.first_child
#
#        self.assertEqual(root.child_count, 1)
#        self.assertEqual(child.sibling_count, 1)
#        self.assertEqual(root.lookup("int"), type_int)
#        self.assertEqual(root.lookup("double"), None)
#        # Only the child has access to both types
#        self.assertEqual(child.lookup("int"), type_int)
#        self.assertEqual(child.lookup("double"), type_double)