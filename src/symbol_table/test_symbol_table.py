import unittest
from typing import List

from . import (
    LexicalSymbolTable,
    LexicalSymbolTabelBuilder,
    PrimitiveType,
    SubroutineType
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
        #       1
        #      /|\
        #     o 0 o
        # 0: Is the start
        # [0-2]: Is the traversed
        #   tables and their order.
        builder = LexicalSymbolTabelBuilder()
        builder.open().close() # o
        builder.open().close() # 0
        builder.open().close() # o

        tree = builder.build()
        root = tree.root
        start = root.children[1]

        traversal = [ *start.lexical_traversal() ]
        table_0 = root.children[1]
        table_1 = root

        self.assertEqual(len(traversal), 2)
        self.assertEqual(table_0, traversal[0])
        self.assertEqual(table_1, traversal[1])

    def test_lexical_traversal_disjoint_children(self) -> None:
        #       2
        #      /|\
        #     o 1 o
        #    / / \ \
        #   o o   0 o
        # 0: Is the start
        # [0-4]: Is the traversed
        #   tables and their order.
        builder = LexicalSymbolTabelBuilder()
        builder.open()  # o
        builder.open()  # | o
        builder.close() # | |
        builder.close() # |

        builder.open()  # 1
        builder.open()  # | o
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
        table_0 = start
        table_1 = table_0.parent
        table_2 = table_1.parent

        self.assertEqual(len(traversal), 3)
        self.assertEqual(table_0, traversal[0])
        self.assertEqual(table_1, traversal[1])
        self.assertEqual(table_2, traversal[2])

    def test_lexical_scoping_on_c_program_only_formal_parameters(self) -> None:
        # int sum(int a, int b) {
        #   return a + b;
        # }
        #
        #   G
        #   |
        #   0
        # G: The global scope, 0: is the "sum"-function scope
        builder = LexicalSymbolTabelBuilder()
        type_int = PrimitiveType("int")
        sum_type = SubroutineType(type_int, [ type_int, type_int ])
        # Add "sum" to the global scope (G)
        #   The lexical-index of the "sum"-scope is its "last_byte"
        #   Because it can only be used after it has been declared.
        builder.enter("sum", sum_type, 35)
        # Create the "sum"-function scope and add the formal parameters
        #   The lexical-index of the formal parameters are their "last_byte"
        builder.open() \
            .enter("a", type_int, 13) \
            .enter("b", type_int, 20) \
            .close()
        
        tree = builder.build()
        root = tree.root

        global_scope = root
        sum_scope = global_scope.children[0]

        global_identifiers = global_scope.identifiers()
        sum_scope_identifiers = sum_scope.identifiers()

        # First we want to verify that the correct identifiers
        #   are found in the correct scopes.
        self.assertTrue("sum" in global_identifiers)
        self.assertEqual(len(global_identifiers), 1)
        self.assertTrue("a" in sum_scope_identifiers)
        self.assertTrue("b" in sum_scope_identifiers)
        self.assertTrue("sum" in sum_scope_identifiers)
        self.assertEqual(len(sum_scope_identifiers), 3)

        global_sum_type = global_scope.lookup("sum")
        sum_sum_type = sum_scope.lookup("sum")
        sum_a_type = sum_scope.lookup("a")
        sum_b_type = sum_scope.lookup("b")
        
        # Secondly we want to ensure looking these identifiers up
        #   we are finding the correct types in their respective scopes
        self.assertIsInstance(global_sum_type, SubroutineType)
        self.assertIsInstance(sum_sum_type, SubroutineType)
        # Here we ensure that the "sum_type" from the "sum_scope"
        #   is "taken/found" in the "global_scope" by comparing their
        #   referenace values.
        self.assertEqual(global_sum_type, sum_sum_type)
        self.assertIsInstance(sum_a_type, PrimitiveType)
        self.assertIsInstance(sum_b_type, PrimitiveType)


    def test_lexical_scoping_on_c_program_nests(self) -> None:
        # G
        # | F      int sum(int a, int b) {
        # | | I      if (a > b) {
        # | | |          int z = a + b;
        # | | -          return z;
        # | | E      } else if (a < b) {
        # | | | B        {
        # | | | |            int i = b;
        # | | | -        }
        # | | |          int z = b + a;
        # | | |          return z;
        # | | -      }
        # | |        int imm = a + b;
        # | |        return imm;
        # | -      }
        #
        #       G
        #       |
        #       F
        #      / \
        #     I   E
        #         |
        #         B
        # G: The global scope, F: The "sum"-scope
        # I: "if (a > b)"-body
        # E: "else if (a < b)"-body
        # B: "{ int i = b; }"-block in E
        builder = LexicalSymbolTabelBuilder()
        type_int = PrimitiveType("int")
        sum_type = SubroutineType(type_int, [ type_int, type_int ])

        # The lexical-indices are approximations
        builder \
            .enter("sum", sum_type, 0) \
                .open() \
                .enter("a", type_int, 13) \
                .enter("b", type_int, 20) \
                    .open() \
                    .enter("z", type_int, 30) \
                    .close() \
                    .open() \
                        .open() \
                        .enter("i", type_int, 60) \
                        .close() \
                    .enter("z", type_int, 80) \
                    .close() \
                .enter("imm", type_int, 93) \
                .close()

        tree = builder.build()
        root = tree.root

        g_scope = root
        f_scope = root.children[0]
        i_scope = f_scope.children[0]
        e_scope = f_scope.children[1]
        b_scope = e_scope.children[0]

        g_identifiers = g_scope.identifiers()
        f_identifiers = f_scope.identifiers()
        i_identifiers = i_scope.identifiers()
        e_identifiers = e_scope.identifiers()
        b_identifiers = b_scope.identifiers()

        # "+ 1 + 2" is "sum" and its formal parameters
        self.assertTrue("sum" in g_identifiers)
        self.assertEqual(len(g_identifiers), 1)
        self.assertTrue("sum" in f_identifiers)
        self.assertTrue("a" in f_identifiers)
        self.assertTrue("b" in f_identifiers)
        self.assertTrue("imm" in f_identifiers)
        self.assertEqual(len(f_identifiers), 1 + 1 + 2)
        self.assertTrue("sum" in i_identifiers)
        self.assertTrue("a" in i_identifiers)
        self.assertTrue("b" in i_identifiers)
        self.assertTrue("z" in i_identifiers)
        self.assertEqual(len(i_identifiers), 1 + 1 + 2)
        self.assertTrue("sum" in e_identifiers)
        self.assertTrue("a" in e_identifiers)
        self.assertTrue("b" in e_identifiers)
        self.assertTrue("z" in e_identifiers)
        self.assertEqual(len(e_identifiers), 1 + 1 + 2)
        self.assertTrue("sum" in b_identifiers)
        self.assertTrue("a" in b_identifiers)
        self.assertTrue("b" in b_identifiers)
        self.assertTrue("i" in b_identifiers)
        self.assertEqual(len(b_identifiers), 1 + 1 + 2)

        self.assertIsInstance(g_scope.lookup("sum"), SubroutineType)
        self.assertEqual(f_scope.lookup("sum"), g_scope.lookup("sum"))
        self.assertIsInstance(f_scope.lookup("a"), PrimitiveType)
        self.assertIsInstance(f_scope.lookup("b"), PrimitiveType)
        self.assertIsInstance(f_scope.lookup("imm"), PrimitiveType)
        self.assertEqual(i_scope.lookup("a"), f_scope.lookup("a"))
        self.assertEqual(i_scope.lookup("b"), f_scope.lookup("b"))
        self.assertEqual(i_scope.lookup("imm"), f_scope.lookup("imm"))
        self.assertIsInstance(i_scope.lookup("z"), PrimitiveType)
        self.assertEqual(e_scope.lookup("a"), f_scope.lookup("a"))
        self.assertEqual(e_scope.lookup("b"), f_scope.lookup("b"))
        self.assertEqual(e_scope.lookup("imm"), f_scope.lookup("imm"))
        self.assertIsInstance(e_scope.lookup("z"), PrimitiveType)
        self.assertEqual(i_scope.lookup("z"), e_scope.lookup("z"))
        self.assertEqual(b_scope.lookup("a"), f_scope.lookup("a"))
        self.assertEqual(b_scope.lookup("b"), f_scope.lookup("b"))
        self.assertEqual(b_scope.lookup("imm"), f_scope.lookup("imm"))
        self.assertIsInstance(b_scope.lookup("i"), PrimitiveType)

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
        self.assertFalse("bar" in first_identifiers)
        self.assertEqual(len(last_identifiers), 1)
        self.assertFalse("foo" in last_identifiers)
        self.assertTrue("bar" in last_identifiers)