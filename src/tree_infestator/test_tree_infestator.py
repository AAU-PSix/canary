import unittest

from src.ts import *
from src.cfa import *
from . import TreeInfestator

class TestTreeInfestator(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)
        self._infestator = TreeInfestator(self._parser)

    def test_is_condition_of_if_true(self) -> None:
        program: str = "if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        if_node: Node = tree.root_node.named_children[0]
        condition: Node = if_node.child_by_field_name("condition")
        expected: bool = True

        actual = self._infestator.is_condition_of_if(condition)

        self.assertEqual(if_node.type, "if_statement")
        self.assertEqual(condition.type, "parenthesized_expression")
        self.assertEqual(actual, expected)

    def test_is_condition_of_if_false(self) -> None:
        program: str = "if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        if_node: Node = tree.root_node.named_children[0]
        alternative: Node = if_node.child_by_field_name("alternative")
        expected: bool = False

        actual = self._infestator.is_condition_of_if(alternative)

        self.assertEqual(if_node.type, "if_statement")
        self.assertEqual(alternative.type, "compound_statement")
        self.assertEqual(actual, expected)

    def test_is_condition_of_while_true(self) -> None:
        program: str = "while(a) { }"
        tree: Tree = self._parser.parse(program)
        while_node: Node = tree.root_node.named_children[0]
        condition: Node = while_node.child_by_field_name("condition")
        expected: bool = True

        actual = self._infestator.is_condition_of_while(condition)

        self.assertEqual(while_node.type, "while_statement")
        self.assertEqual(condition.type, "parenthesized_expression")
        self.assertEqual(actual, expected)

    def test_is_condition_of_while_false(self) -> None:
        program: str = "while(a) { }"
        tree: Tree = self._parser.parse(program)
        while_node: Node = tree.root_node.named_children[0]
        not_condition: Node = while_node
        expected: bool = False

        actual = self._infestator.is_condition_of_while(not_condition)

        self.assertEqual(while_node.type, "while_statement")
        self.assertEqual(not_condition.type, "while_statement")
        self.assertEqual(actual, expected)

    def test_nests_of_while(self) -> None:
        program: str = "while(a) { }"
        tree: Tree = self._parser.parse(program)
        while_node: Node = tree.root_node.named_children[0]
        condition: Node = while_node.child_by_field_name("condition")

        nests = self._infestator.nests_of_while_condition(condition)

        self.assertEqual(len(nests), 1)
        self.assertEqual(nests[0].type, "compound_statement")

    def test_infect_while(self) -> None:
        program: str = "while(a) { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        expected = "while(a) {TWEET(); }"
        actual = self._infestator.infect(tree, cfa).text
        nests = self._infestator.nests(cfa)

        self.assertEqual(len(nests), 1)
        self.assertEqual(expected, actual)

    def test_nests_if_if(self) -> None:
        program: str = "if(a) { if(a) { } }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        first_if_statement: Node = tree.root_node.named_children[0]
        first_if_consequence: Node = first_if_statement.child_by_field_name("consequence")
        second_if_statement: Node = first_if_consequence.named_children[0]
        second_if_consequence: Node = second_if_statement.child_by_field_name("consequence")

        nests = self._infestator.nests(cfa)

        self.assertEqual(2, len(nests))
        self.assertEqual(first_if_consequence.type, "compound_statement")
        self.assertEqual(second_if_consequence.type, "compound_statement")

        self.assertEqual(nests[0].type, "compound_statement")
        self.assertEqual(nests[1].type, "compound_statement")

    def test_infect_if(self) -> None:
        program: str = "if(a) { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        expected = "if(a) {TWEET(); }"
        actual = self._infestator.infect(tree, cfa).text

        self.assertEqual(expected, actual)

    def test_infect_if_else(self) -> None:
        program: str = "if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        expected = "if(a) {TWEET(); } else {TWEET(); }"
        actual = self._infestator.infect(tree, cfa).text

        self.assertEqual(expected, actual)

    def test_infect_if_elseif(self) -> None:
        program: str = "if(a) { } else if(a) { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        expected = "if(a) {TWEET(); } else if(a) {TWEET(); }"
        actual = self._infestator.infect(tree, cfa).text

        self.assertEqual(expected, actual)

    def test_infect_if_elseif_else(self) -> None:
        program: str = "if(a) { } else if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        expected = "if(a) {TWEET(); } else if(a) {TWEET(); } else {TWEET(); }"
        actual = self._infestator.infect(tree, cfa).text

        self.assertEqual(expected, actual)

    def test_infect_if_if(self) -> None:
        program: str = "if(a) { if(a) { } }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        expected = "if(a) {TWEET(); if(a) {TWEET(); } }"
        actual = self._infestator.infect(tree, cfa).text

        self.assertEqual(expected, actual)

    def test_infect_if_elseif_elseif(self) -> None:
        program: str = "if(a) { } else if(a) { } else if(a) { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)
        actual: Tree = self._infestator.infect(tree, cfa)
        self.assertEqual(actual.text, "if(a) {TWEET(); } else if(a) {TWEET(); } else if(a) {TWEET(); }")

    def test_can_add_tweet_for_if_statement(self):
        program: str = "if(a) { }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        actual = self._infestator.infect(tree, cfa).text
        expected = "if(a) {TWEET(); }"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_else_statement(self):
        program: str = "if(a) { } else { }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        actual = self._infestator.infect(tree, cfa).text
        expected = "if(a) {TWEET(); } else {TWEET(); }"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_elseif_statement(self):
        program: str = "if(a) { } else if(a) { }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        actual = self._infestator.infect(tree, cfa).text
        expected = "if(a) {TWEET(); } else if(a) {TWEET(); }"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_elseif_else_statement(self):
        program: str = "if(a) { } else if(a) { } else { }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        actual = self._infestator.infect(tree, cfa).text
        expected = "if(a) {TWEET(); } else if(a) {TWEET(); } else {TWEET(); }"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_if_statement(self):
        program: str = "if(a) { if(a) { } }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        actual = self._infestator.infect(tree, cfa).text
        expected = "if(a) {TWEET(); if(a) {TWEET(); } }"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_if_else_statement(self):
        program: str = "if(a) { if(a) { } else { } }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        actual = self._infestator.infect(tree, cfa).text
        expected = "if(a) {TWEET(); if(a) {TWEET(); } else {TWEET(); } }"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_if_elseif_statement(self):
        program: str = "if(a) { if(a) { } else if(a) { } }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        actual = self._infestator.infect(tree, cfa).text
        expected = "if(a) {TWEET(); if(a) {TWEET(); } else if(a) {TWEET(); } }"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_if_elseif_else_statement(self):
        program: str = "if(a) { if(a) { } else if(a) { } else { } }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        actual = self._infestator.infect(tree, cfa)
        expected = "if(a) {TWEET(); if(a) {TWEET(); } else if(a) {TWEET(); } else {TWEET(); } }"
        self.assertEqual(expected, actual.text)

    def test_is_condition_of_do_while_true(self) -> None:
        program: str = "do { } while(a);"
        tree: Tree = self._parser.parse(program)
        do_node: Node = tree.root_node.named_children[0]
        condition: Node = do_node.child_by_field_name("condition")
        expected: bool = True

        actual = self._infestator.is_condition_of_do_while(condition)

        self.assertEqual(do_node.type, "do_statement")
        self.assertEqual(condition.type, "parenthesized_expression")
        self.assertEqual(actual, expected)

    def test_is_condition_of_do_while_false(self) -> None:
        program: str = "do { } while(a);"
        tree: Tree = self._parser.parse(program)
        do_node: Node = tree.root_node.named_children[0]
        not_condition: Node = do_node
        expected: bool = False

        actual = self._infestator.is_condition_of_do_while(not_condition)

        self.assertEqual(do_node.type, "do_statement")
        self.assertEqual(not_condition.type, "do_statement")
        self.assertEqual(actual, expected)

    def test_nests_of_do_while(self) -> None:
        program: str = "do { } while(a);"
        tree: Tree = self._parser.parse(program)
        do_node: Node = tree.root_node.named_children[0]
        condition: Node = do_node.child_by_field_name("condition")

        nests = self._infestator.nests_of_do_while_condition(condition)

        self.assertEqual(len(nests), 1)
        self.assertEqual(nests[0].type, "compound_statement")

    def test_infect_do_while(self) -> None:
        program: str = "do { } while(a);"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        expected =  "do {TWEET(); } while(a);"
        actual = self._infestator.infect(tree, cfa).text
        nests = self._infestator.nests(cfa)

        self.assertEqual(len(nests), 1)
        self.assertEqual(expected, actual)

    def test_is_condition_of_for_true(self) -> None:
        program: str = "for (;;) { }"
        tree: Tree = self._parser.parse(program)
        for_node: Node = tree.root_node.named_children[0]
        body: Node = for_node.named_children[-1]
        expected: bool = True

        actual = self._infestator.is_body_of_for_loop(body)

        self.assertEqual(for_node.type, "for_statement")
        self.assertEqual(body.type, "compound_statement")
        self.assertEqual(actual, expected)

    def test_is_condition_of_for_false(self) -> None:
        program: str = "for (;;) { }"
        tree: Tree = self._parser.parse(program)
        for_node: Node = tree.root_node.named_children[0]
        not_body: Node = for_node
        expected: bool = False

        actual = self._infestator.is_body_of_for_loop(not_body)

        self.assertEqual(for_node.type, "for_statement")
        self.assertEqual(not_body.type, "for_statement")
        self.assertEqual(actual, expected)

    def test_nests_of_for_statement(self) -> None:
        program: str = "for (;;) { }"
        tree: Tree = self._parser.parse(program)
        for_node: Node = tree.root_node.named_children[0]
        body: Node = for_node.named_children[-1]

        nests = self._infestator.nests_of_for_loop_body(body)

        self.assertEqual(len(nests), 1)
        self.assertEqual(nests[0].type, "compound_statement")

    def test_infect_for_statement(self) -> None:
        program: str = "for (;;) { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        expected =  "for (;;) {TWEET(); }"
        actual = self._infestator.infect(tree, cfa).text
        nests = self._infestator.nests(cfa)

        self.assertEqual(len(nests), 1)
        self.assertEqual(expected, actual)

    def test_is_case_value_of_switch_true(self) -> None:
        program: str = """
            switch(a) {
                case 3: { }
            }
        """
        tree: Tree = self._parser.parse(program)
        switch_node: Node = tree.root_node.named_children[0]
        body: Node = switch_node.child_by_field_name("body")
        case: Node = body.named_children[0]
        case_value: Node = case.child_by_field_name("value")
        expected: bool = True

        actual = self._infestator.is_case_value_of_switch(case_value)

        self.assertEqual(switch_node.type, "switch_statement")
        self.assertEqual(body.type, "compound_statement")
        self.assertEqual(case.type, "case_statement")
        self.assertEqual(case_value.type, "number_literal")
        self.assertEqual(actual, expected)

    def test_is_case_value_of_switch_false(self) -> None:
        program: str = """
            switch(a) {
                case 3: { }
            }
        """
        tree: Tree = self._parser.parse(program)
        switch_node: Node = tree.root_node.named_children[0]
        body: Node = switch_node.child_by_field_name("body")
        not_case_value: Node = body
        expected: bool = False

        actual = self._infestator.is_case_value_of_switch(not_case_value)

        self.assertEqual(switch_node.type, "switch_statement")
        self.assertEqual(body.type, "compound_statement")
        self.assertEqual(not_case_value.type, "compound_statement")
        self.assertEqual(actual, expected)

    def test_is_default_case_of_switch_false(self) -> None:
        program: str = """
            switch(a) {
                case 3: { }
            }
        """
        tree: Tree = self._parser.parse(program)
        switch_node: Node = tree.root_node.named_children[0]
        body: Node = switch_node.child_by_field_name("body")
        not_case: Node = body
        expected: bool = False

        actual = self._infestator.is_case_value_of_switch(not_case)

        self.assertEqual(switch_node.type, "switch_statement")
        self.assertEqual(body.type, "compound_statement")
        self.assertEqual(not_case.type, "compound_statement")
        self.assertEqual(actual, expected)

    def test_nests_of_case_value_for_switch(self) -> None:
        program: str = """
            switch(a) {
                case 3: { }
            }
        """
        tree: Tree = self._parser.parse(program)
        switch_node: Node = tree.root_node.named_children[0]
        body: Node = switch_node.child_by_field_name("body")
        case: Node = body.named_children[0]
        case_value: Node = case.child_by_field_name("value")

        nests = self._infestator.nests_of_case_value_for_switch(case_value)

        self.assertEqual(len(nests), 1)
        self.assertEqual(nests[0].type, "case_statement")

    def test_infect_switch(self) -> None:
        program: str = """
            switch(a) {
                case 3: { }
            }
        """
        tree: Tree = self._parser.parse(program)
        cfa: CFA = TreeCFAVisitor(tree).create(tree.root_node, False)

        expected =  """
            switch(a) {
                case 3:TWEET(); { }
            }
        """
        actual = self._infestator.infect(tree, cfa).text

        self.assertEqual(expected, actual)

    def test_is_labeled_statement_true(self) -> None:
        pass

    def test_is_labeled_statement_false(self) -> None:
        pass

    def test_nests_of_labeled_statement(self) -> None:
        pass

    def test_infect_labeled_statement(self) -> None:
        pass