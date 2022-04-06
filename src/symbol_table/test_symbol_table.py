import unittest
from typing import List
from graphviz import Digraph
from . import *

class TestSymbolTable(unittest.TestCase):
    def test_root_children_siblings(self) -> None:
        root_children: List[LexicalSymbolTable] = [ ]
        root_table = LexicalSymbolTable(-10, 10, None, root_children)
        # Two different approaches of appending a child
        root_table.children.append(LexicalSymbolTable(1, 2, root_table, list()))
        root_children.append(LexicalSymbolTable(3, 4, root_table, list()))
        root_children.append(LexicalSymbolTable(5, 6, root_table, list()))

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
        builder = CSymbolTableBuilder(-10, 10)
        builder.open(1, 1)
        builder.close()
        builder.open(2, 2)
        builder.close()
        builder.open(3, 3)
        builder.close()

        root = builder.build().root

        self.assertEqual(root.child_count, 3)
        self.assertEqual(root.first_child.sibling_count, 3)
        self.assertEqual(root.first_child, root.children[0])
        self.assertEqual(root.last_child, root.children[-1])
        self.assertEqual(root.children[0].next_sibling, root.children[1])
        self.assertEqual(root.children[1].previous_sibling, root.children[0])

    def test_lookup(self) -> None:
        builder = CSymbolTableBuilder(-10, 10)
        type_int = PrimitiveType("int")
        type_double = PrimitiveType("double")
        builder.enter("foo", type_int, 0)
        builder.open(1, 2)
        builder.enter("bar", type_double, 1)
        builder.close()

        root: LexicalSymbolTable = builder.build().root
        child = root.first_child

        self.assertEqual(root.child_count, 1)
        self.assertEqual(child.sibling_count, 1)
        self.assertEqual(root.lookup("foo").type, type_int)
        self.assertTrue(root.has("foo"))
        self.assertEqual(root.lookup("bar"), None)
        self.assertFalse(root.has("bar"))
        # Only the child has access to both types
        self.assertEqual(child.lookup("foo").type, type_int)
        self.assertTrue(child.has("foo"))
        self.assertEqual(child.lookup("bar").type, type_double)
        self.assertTrue(child.has("bar"))

    def test_lexical_traversal_trivial_child(self) -> None:
        #       1
        #      /|\
        #     0-o-o
        # 0: Is the start
        # [0-2]: Is the traversed
        #   tables and their order.
        builder = CSymbolTableBuilder(0, 10)
        builder.open(1, 1).close() # 0
        builder.open(2, 2).close() # o
        builder.open(3, 3).close() # o

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
        # [0-1]: Is the traversed
        #   tables and their order.
        builder = CSymbolTableBuilder(0, 10)
        builder.open(1, 1).close() # o
        builder.open(2, 2).close() # 0
        builder.open(3, 3).close() # o

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
        builder = CSymbolTableBuilder(0, 20)
        builder.open(1, 5)  # o
        builder.open(2, 4)  # | o
        builder.close() # | |
        builder.close() # |

        builder.open(6, 10)  # 1
        builder.open(7, 7)  # | o
        builder.close() # | |
        builder.open(8, 9)  # | 0
        builder.close() # | |
        builder.close() # |

        builder.open(11, 15)  # o
        builder.open(13, 14)  # | o
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
        builder = CSymbolTableBuilder(0, 35)
        type_int = PrimitiveType("int")
        sum_type = SubroutineType(type_int, [ type_int, type_int ])
        # Add "sum" to the global scope (G)
        #   The lexical-index of the "sum"-scope is its "last_byte"
        #   Because it can only be used after it has been declared.
        builder.enter("sum", sum_type, 35)
        # Create the "sum"-function scope and add the formal parameters
        #   The lexical-index of the formal parameters are their "last_byte"
        builder.open(13, 20) \
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

        global_sum_type = global_scope.lookup("sum").type
        sum_sum_type = sum_scope.lookup("sum").type
        sum_a_type = sum_scope.lookup("a").type
        sum_b_type = sum_scope.lookup("b").type

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
        builder = CSymbolTableBuilder(0, 93)
        type_int = PrimitiveType("int")
        sum_type = SubroutineType(type_int, [ type_int, type_int ])

        # The lexical-indices are approximations
        builder \
            .enter("sum", sum_type, 0) \
            .open(13, 93) \
                .enter("a", type_int, 13) \
                .enter("b", type_int, 20) \
                .open(30, 30) \
                    .enter("z", type_int, 30) \
                .close() \
                .open(60, 80) \
                    .open(60, 60) \
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

        self.assertIsInstance(g_scope.lookup("sum").type, SubroutineType)
        self.assertEqual(f_scope.lookup("sum").type, g_scope.lookup("sum").type)
        self.assertIsInstance(f_scope.lookup("a").type, PrimitiveType)
        self.assertIsInstance(f_scope.lookup("b").type, PrimitiveType)
        self.assertIsInstance(f_scope.lookup("imm").type, PrimitiveType)
        self.assertEqual(i_scope.lookup("a").type, f_scope.lookup("a").type)
        self.assertEqual(i_scope.lookup("b").type, f_scope.lookup("b").type)
        self.assertEqual(i_scope.lookup("imm").type, f_scope.lookup("imm").type)
        self.assertIsInstance(i_scope.lookup("z").type, PrimitiveType)
        self.assertEqual(e_scope.lookup("a").type, f_scope.lookup("a").type)
        self.assertEqual(e_scope.lookup("b").type, f_scope.lookup("b").type)
        self.assertEqual(e_scope.lookup("imm").type, f_scope.lookup("imm").type)
        self.assertIsInstance(e_scope.lookup("z").type, PrimitiveType)
        self.assertEqual(i_scope.lookup("z").type, e_scope.lookup("z").type)
        self.assertEqual(b_scope.lookup("a").type, f_scope.lookup("a").type)
        self.assertEqual(b_scope.lookup("b").type, f_scope.lookup("b").type)
        self.assertEqual(b_scope.lookup("imm").type, f_scope.lookup("imm").type)
        self.assertIsInstance(b_scope.lookup("i").type, PrimitiveType)

    def test_bounded_identifiers_single_scope(self) -> None:
        # The lines of code can be viewed like this:
        # 0: int a;
        # 1: int b;
        # 2: int c;
        # 3: int d;
        # 4: int e;
        # The questions answered by "identifiers_at" is the following:
        #   "what identifiers can be used at line n", resulting in the
        #   set of valid identifiers to reference at a given line.

        builder = CSymbolTableBuilder(0, 4)
        type_int = PrimitiveType("int")
        builder.open(0, 4) \
            .enter("a", type_int, 0) \
            .enter("b", type_int, 1) \
            .enter("c", type_int, 2) \
            .enter("d", type_int, 3) \
            .enter("e", type_int, 4) \
            .close()

        tree = builder.build()
        root = tree.root

        identifiers_at_0 = root.identifiers(0)
        identifiers_at_1 = root.identifiers(1)
        identifiers_at_2 = root.identifiers(2)
        identifiers_at_3 = root.identifiers(3)
        identifiers_at_4 = root.identifiers(4)

        self.assertEqual(root.minimum_lexical_index, 0)
        self.assertEqual(root.maximum_lexical_index, 4)

        self.assertEqual(len(identifiers_at_0), 0)
        self.assertEqual(len(identifiers_at_1), 1)
        self.assertTrue("a" in identifiers_at_1)
        self.assertEqual(len(identifiers_at_2), 2)
        self.assertTrue("a" in identifiers_at_2)
        self.assertTrue("b" in identifiers_at_2)
        self.assertEqual(len(identifiers_at_3), 3)
        self.assertTrue("a" in identifiers_at_3)
        self.assertTrue("b" in identifiers_at_3)
        self.assertTrue("c" in identifiers_at_3)
        self.assertEqual(len(identifiers_at_4), 4)
        self.assertTrue("a" in identifiers_at_4)
        self.assertTrue("b" in identifiers_at_4)
        self.assertTrue("c" in identifiers_at_4)
        self.assertTrue("d" in identifiers_at_4)

    def test_bounded_identifiers_multiple_scopes(self) -> None:
        # 0: {
        # 1:     {
        # 2:         int a;
        # 3:     }
        # 4:     int b;
        # 5:     {
        # 6:         int c;
        # 7:     }
        # 8: }

        builder = CSymbolTableBuilder(0, 8)
        type_int = PrimitiveType("int")
        builder.open(1, 3) \
                .enter("a", type_int, 2) \
            .close() \
            .enter("b", type_int, 4) \
            .open(5, 7) \
                .enter("c", type_int, 6) \
            .close()

        tree = builder.build()
        root = tree.root

        identifiers_at_3 = root.identifiers(3)
        identifiers_at_5 = root.identifiers(5)
        identifiers_at_7 = root.identifiers(7)

        self.assertEqual(len(identifiers_at_3), 1)
        self.assertTrue("a" in identifiers_at_3)
        self.assertEqual(len(identifiers_at_5), 1)
        self.assertTrue("b" in identifiers_at_5)
        self.assertEqual(len(identifiers_at_7), 2)
        self.assertTrue("b" in identifiers_at_7)
        self.assertTrue("c" in identifiers_at_7)

    def test_get(self) -> None:
        builder = CSymbolTableBuilder(-10, 10)
        type_int = PrimitiveType("int")
        builder.open(0, 0)
        builder.enter("foo", type_int, 0)
        builder.close()
        builder.open(1, 1)
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

    def test_draw(self) -> None:
        builder = CSymbolTableBuilder(0, 8)
        type_int = PrimitiveType("int")
        builder.open(1, 3) \
                .enter("foo", type_int, 2) \
                .enter("a", type_int, 2) \
            .close() \
            .enter("b", type_int, 4) \
            .open(5, 7) \
                .enter("bar", type_int, 6) \
            .close()

        tree = builder.build()
        root = tree.root

        dot: Digraph = root.draw("symbol_table_test")
        dot.save(directory="graphs")