from typing import List, Tuple
import unittest
from ts import (
    LanguageLibrary,
    Tree,
    Node,
    Parser,
    CSyntax,
    CField,
    CNodeType,
)
from cfa import (
    CFA,
    CCFAFactory,
    CFANode,
)
from . import CTreeInfestator, CCanaryFactory, SimpleTestCanaryFactory

class TestTreeInfestator(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)
        self._infestator = CTreeInfestator(self._parser, CCanaryFactory())
        self._syntax = CSyntax()

    def test_is_condition_of_if_true(self) -> None:
        program: str = "if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        if_node: Node = tree.root.named_children[0]
        condition: Node = if_node.child_by_field_name("condition")
        expected: bool = True

        actual = self._syntax.is_condition_of_if(condition)

        self.assertEqual(if_node.type, "if_statement")
        self.assertEqual(condition.type, "parenthesized_expression")
        self.assertEqual(actual, expected)

    def test_is_condition_of_if_false(self) -> None:
        program: str = "if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        if_node: Node = tree.root.named_children[0]
        alternative: Node = if_node.child_by_field_name("alternative")
        expected: bool = False

        actual = self._syntax.is_condition_of_if(alternative)

        self.assertEqual(if_node.type, "if_statement")
        self.assertEqual(alternative.type, "compound_statement")
        self.assertEqual(actual, expected)

    def test_is_condition_of_while_true(self) -> None:
        program: str = "while(a) { }"
        tree: Tree = self._parser.parse(program)
        while_node: Node = tree.root.named_children[0]
        condition: Node = while_node.child_by_field_name("condition")
        expected: bool = True

        actual = self._syntax.is_condition_of_while(condition)

        self.assertEqual(while_node.type, "while_statement")
        self.assertEqual(condition.type, "parenthesized_expression")
        self.assertEqual(actual, expected)

    def test_is_condition_of_while_false(self) -> None:
        program: str = "while(a) { }"
        tree: Tree = self._parser.parse(program)
        while_node: Node = tree.root.named_children[0]
        not_condition: Node = while_node
        expected: bool = False

        actual = self._syntax.is_condition_of_while(not_condition)

        self.assertEqual(while_node.type, "while_statement")
        self.assertEqual(not_condition.type, "while_statement")
        self.assertEqual(actual, expected)

    def test_nests_of_while(self) -> None:
        program: str = "while(a) { }"
        tree: Tree = self._parser.parse(program)
        while_node: Node = tree.root.named_children[0]
        condition: Node = while_node.child_by_field_name("condition")

        nests = self._infestator.nests_of_while_condition(condition)

        self.assertEqual(len(nests), 1)
        self.assertEqual(nests[0].type, "while_statement")

    def test_infect_while(self) -> None:
        program: str = "while(a) { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        expected = "CANARY_TWEET_LOCATION(0);while(a) {CANARY_TWEET_LOCATION(1); }CANARY_TWEET_LOCATION(2);"
        actual = self._infestator.infect(tree, cfa).text
        nests = self._infestator.nests(cfa)

        self.assertEqual(len(nests), 2)
        self.assertEqual(expected, actual)

    def test_nests_if_if(self) -> None:
        program: str = "if(a) { if(a) { } }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        nests = self._infestator.nests(cfa)

        self.assertEqual(len(nests), 3)
        self.assertEqual(nests[0].type, "translation_unit")
        self.assertEqual(nests[1].type, "if_statement")
        self.assertEqual(nests[2].type, "if_statement")

    def test_infect_if(self) -> None:
        program: str = "if(a) { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        expected = "CANARY_TWEET_LOCATION(0);if(a) {CANARY_TWEET_LOCATION(2); }CANARY_TWEET_LOCATION(1);"
        actual = self._infestator.infect(tree, cfa).text

        self.assertEqual(expected, actual)

    def test_infect_if_else(self) -> None:
        program: str = "if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        expected = "CANARY_TWEET_LOCATION(0);if(a) {CANARY_TWEET_LOCATION(2); } else {CANARY_TWEET_LOCATION(3); }CANARY_TWEET_LOCATION(1);"
        actual = self._infestator.infect(tree, cfa).text

        self.assertEqual(expected, actual)

    def test_infect_if_elseif(self) -> None:
        program: str = "if(a) { } else if(a) { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        expected = "CANARY_TWEET_LOCATION(0);if(a) {CANARY_TWEET_LOCATION(1); } else if(a) {CANARY_TWEET_LOCATION(3); }CANARY_TWEET_LOCATION(2);"
        actual = self._infestator.infect(tree, cfa).text

        self.assertEqual(expected, actual)

    def test_infect_if_elseif_else(self) -> None:
        program: str = "if(a) { } else if(a) { } else { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        expected = "CANARY_TWEET_LOCATION(0);if(a) {CANARY_TWEET_LOCATION(1); } else if(a) {CANARY_TWEET_LOCATION(3); } else {CANARY_TWEET_LOCATION(4); }CANARY_TWEET_LOCATION(2);"
        actual = self._infestator.infect(tree, cfa).text

        self.maxDiff = 1000
        self.assertEqual(expected, actual)

    def test_infect_if_if(self) -> None:
        program: str = "if(a) { if(a) { } }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        expected = "CANARY_TWEET_LOCATION(0);if(a) {CANARY_TWEET_LOCATION(2); if(a) {CANARY_TWEET_LOCATION(4); }CANARY_TWEET_LOCATION(3); }CANARY_TWEET_LOCATION(1);"
        actual = self._infestator.infect(tree, cfa).text

        self.assertEqual(expected, actual)

    def test_infect_if_elseif_elseif(self) -> None:
        program: str = "if(a) { } else if(a) { } else if(a) { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)
        actual: Tree = self._infestator.infect(tree, cfa)
        self.maxDiff = 1000
        self.assertEqual(actual.text, "CANARY_TWEET_LOCATION(0);if(a) {CANARY_TWEET_LOCATION(1); } else if(a) {CANARY_TWEET_LOCATION(2); } else if(a) {CANARY_TWEET_LOCATION(4); }CANARY_TWEET_LOCATION(3);")

    def test_can_add_tweet_for_if_statement(self):
        program: str = "if(a) { }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        actual = self._infestator.infect(tree, cfa).text
        self.maxDiff = 1000
        expected = "CANARY_TWEET_LOCATION(0);if(a) {CANARY_TWEET_LOCATION(2); }CANARY_TWEET_LOCATION(1);"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_else_statement(self):
        program: str = "if(a) { } else { }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        actual = self._infestator.infect(tree, cfa).text
        self.maxDiff = 1000
        expected = "CANARY_TWEET_LOCATION(0);if(a) {CANARY_TWEET_LOCATION(2); } else {CANARY_TWEET_LOCATION(3); }CANARY_TWEET_LOCATION(1);"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_elseif_statement(self):
        program: str = "if(a) { } else if(a) { }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        actual = self._infestator.infect(tree, cfa).text
        self.maxDiff = 1000
        expected = "CANARY_TWEET_LOCATION(0);if(a) {CANARY_TWEET_LOCATION(1); } else if(a) {CANARY_TWEET_LOCATION(3); }CANARY_TWEET_LOCATION(2);"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_elseif_else_statement(self):
        program: str = "if(a) { } else if(a) { } else { }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        actual = self._infestator.infect(tree, cfa).text
        self.maxDiff = 1000
        expected = "CANARY_TWEET_LOCATION(0);if(a) {CANARY_TWEET_LOCATION(1); } else if(a) {CANARY_TWEET_LOCATION(3); } else {CANARY_TWEET_LOCATION(4); }CANARY_TWEET_LOCATION(2);"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_if_statement(self):
        program: str = "if(a) { if(a) { } }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        actual = self._infestator.infect(tree, cfa).text
        self.maxDiff = 1000
        expected = "CANARY_TWEET_LOCATION(0);if(a) {CANARY_TWEET_LOCATION(2); if(a) {CANARY_TWEET_LOCATION(4); }CANARY_TWEET_LOCATION(3); }CANARY_TWEET_LOCATION(1);"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_if_else_statement(self):
        program: str = "if(a) { if(a) { } else { } }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        actual = self._infestator.infect(tree, cfa).text
        self.maxDiff = 1000
        expected = "CANARY_TWEET_LOCATION(0);if(a) {CANARY_TWEET_LOCATION(2); if(a) {CANARY_TWEET_LOCATION(4); } else {CANARY_TWEET_LOCATION(5); }CANARY_TWEET_LOCATION(3); }CANARY_TWEET_LOCATION(1);"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_if_elseif_statement(self):
        program: str = "if(a) { if(a) { } else if(a) { } }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        actual = self._infestator.infect(tree, cfa).text
        self.maxDiff = 1000
        expected = "CANARY_TWEET_LOCATION(0);if(a) {CANARY_TWEET_LOCATION(2); if(a) {CANARY_TWEET_LOCATION(3); } else if(a) {CANARY_TWEET_LOCATION(5); }CANARY_TWEET_LOCATION(4); }CANARY_TWEET_LOCATION(1);"
        self.assertEqual(expected, actual)

    def test_can_add_tweet_for_if_if_elseif_else_statement(self):
        program: str = "if(a) { if(a) { } else if(a) { } else { } }"
        tree: Tree = self._parser.parse(program)

        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        actual = self._infestator.infect(tree, cfa)
        self.maxDiff = 1000
        expected = "CANARY_TWEET_LOCATION(0);if(a) {CANARY_TWEET_LOCATION(2); if(a) {CANARY_TWEET_LOCATION(3); } else if(a) {CANARY_TWEET_LOCATION(5); } else {CANARY_TWEET_LOCATION(6); }CANARY_TWEET_LOCATION(4); }CANARY_TWEET_LOCATION(1);"
        self.assertEqual(expected, actual.text)

    def test_is_condition_of_do_while_true(self) -> None:
        program: str = "do { } while(a);"
        tree: Tree = self._parser.parse(program)
        do_node: Node = tree.root.named_children[0]
        condition: Node = do_node.child_by_field_name("condition")
        expected: bool = True

        actual = self._syntax.is_condition_of_do_while(condition)

        self.assertEqual(do_node.type, "do_statement")
        self.assertEqual(condition.type, "parenthesized_expression")
        self.assertEqual(actual, expected)

    def test_is_condition_of_do_while_false(self) -> None:
        program: str = "do { } while(a);"
        tree: Tree = self._parser.parse(program)
        do_node: Node = tree.root.named_children[0]
        not_condition: Node = do_node
        expected: bool = False

        actual = self._syntax.is_condition_of_do_while(not_condition)

        self.assertEqual(do_node.type, "do_statement")
        self.assertEqual(not_condition.type, "do_statement")
        self.assertEqual(actual, expected)

    def test_nests_of_do_while(self) -> None:
        program: str = "do { } while(a);"
        tree: Tree = self._parser.parse(program)
        do_node: Node = tree.root.named_children[0]
        condition: Node = do_node.child_by_field_name("condition")

        nests = self._infestator.nests_of_do_while_condition(condition)

        self.assertEqual(len(nests), 1)
        self.assertEqual(nests[0].type, "do_statement")

    def test_infect_do_while(self) -> None:
        program: str = "do { } while(a);"
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        expected =  "CANARY_TWEET_LOCATION(0);do {CANARY_TWEET_LOCATION(1); } while(a);CANARY_TWEET_LOCATION(2);"
        actual = self._infestator.infect(tree, cfa).text
        nests = self._infestator.nests(cfa)

        self.assertEqual(len(nests), 2)
        self.assertEqual(expected, actual)

    def test_is_body_of_for_true(self) -> None:
        program: str = "for (;;) { }"
        tree: Tree = self._parser.parse(program)
        for_node: Node = tree.root.named_children[0]
        body: Node = for_node.named_children[-1]
        expected: bool = True

        actual = self._syntax.is_body_of_for_loop(body)

        self.assertEqual(for_node.type, "for_statement")
        self.assertEqual(body.type, "compound_statement")
        self.assertEqual(actual, expected)

    def test_is_body_of_for_false(self) -> None:
        program: str = "for (;;) { }"
        tree: Tree = self._parser.parse(program)
        for_node: Node = tree.root.named_children[0]
        not_body: Node = for_node
        expected: bool = False

        actual = self._syntax.is_body_of_for_loop(not_body)

        self.assertEqual(for_node.type, "for_statement")
        self.assertEqual(not_body.type, "for_statement")
        self.assertEqual(actual, expected)

    def test_nests_of_for_statement(self) -> None:
        program: str = "for (;;) { }"
        tree: Tree = self._parser.parse(program)
        for_node: Node = tree.root.named_children[0]
        body: Node = for_node.named_children[-1]

        nests = self._infestator.nests_of_for_loop_body(body)

        self.assertEqual(len(nests), 1)
        self.assertEqual(nests[0].type, "for_statement")

    def test_infect_for_statement(self) -> None:
        program: str = "for (;;) { }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        expected =  "CANARY_TWEET_LOCATION(0);for (;;) {CANARY_TWEET_LOCATION(1); }CANARY_TWEET_LOCATION(2);"
        
        actual = self._infestator.infect(tree, cfa).text
        nests = self._infestator.nests(cfa)

        self.assertEqual(len(nests), 2)
        self.assertEqual(expected, actual)

    def test_infect_for_1(self) -> None:
        program: str = "for(int i = 0;;) { } a=3;"
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        expected =  "CANARY_TWEET_LOCATION(0);for(int i = 0;;) {CANARY_TWEET_LOCATION(1); }CANARY_TWEET_LOCATION(2); a=3;"
        actual = self._infestator.infect(tree, cfa).text
        nests = self._infestator.nests(cfa)

        self.assertEqual(len(nests), 4)
        self.assertEqual(expected, actual)

    def test_infect_for_10(self) -> None:
        program: str = "for(int i = 0; i<5; ++i) { a=2; } a=3;"
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        expected =  "CANARY_TWEET_LOCATION(0);for(int i = 0; i<5; ++i) {CANARY_TWEET_LOCATION(1); a=2; }CANARY_TWEET_LOCATION(2); a=3;"
        actual = self._infestator.infect(tree, cfa).text
        nests = self._infestator.nests(cfa)

        self.assertEqual(len(nests), 5)
        self.assertEqual(expected, actual)

    def test_infect_for_13(self) -> None:
        program: str = "for(;;); a=3;"
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        expected =  "CANARY_TWEET_LOCATION(0);for(;;){CANARY_TWEET_LOCATION(1);;}CANARY_TWEET_LOCATION(2); a=3;"
        actual = self._infestator.infect(tree, cfa).text
        nests = self._infestator.nests(cfa)

        self.assertEqual(len(nests), 4)
        self.assertEqual(expected, actual)

    def test_infect_for_35(self) -> None:
        program: str = "for(;;) { if(a) { a = 1; } }"
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        expected =  "CANARY_TWEET_LOCATION(0);for(;;) {CANARY_TWEET_LOCATION(3); if(a) {CANARY_TWEET_LOCATION(2); a = 1; }CANARY_TWEET_LOCATION(1); }CANARY_TWEET_LOCATION(4);"
        actual = self._infestator.infect(tree, cfa).text
        nests = self._infestator.nests(cfa)

        self.maxDiff = 1000
        self.assertEqual(len(nests), 4)
        self.assertEqual(expected, actual)

    def test_is_case_value_of_switch_true(self) -> None:
        program: str = """
            switch(a) {
                case 3: { }
            }
        """
        tree: Tree = self._parser.parse(program)
        switch_node: Node = tree.root.named_children[0]
        body: Node = switch_node.child_by_field_name("body")
        case: Node = body.named_children[0]
        switch_condition: Node = switch_node.child_by_field_name("condition")
        expected: bool = True

        actual = self._syntax.is_condition_of_switch(switch_condition)

        self.assertEqual(switch_node.type, "switch_statement")
        self.assertEqual(body.type, "compound_statement")
        self.assertEqual(case.type, "case_statement")
        self.assertEqual(switch_condition.type, "parenthesized_expression")
        self.assertEqual(actual, expected)

    def test_is_case_value_of_switch_false(self) -> None:
        program: str = """
            switch(a) {
                case 3: { }
            }
        """
        tree: Tree = self._parser.parse(program)
        switch_node: Node = tree.root.named_children[0]
        body: Node = switch_node.child_by_field_name("body")
        not_case_value: Node = body
        expected: bool = False

        actual = self._syntax.is_condition_of_switch(not_case_value)

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
        switch_node: Node = tree.root.named_children[0]
        body: Node = switch_node.child_by_field_name("body")
        not_case: Node = body
        expected: bool = False

        actual = self._syntax.is_condition_of_switch(not_case)

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
        switch_node: Node = tree.root.named_children[0]
        body: Node = switch_node.child_by_field_name("body")
        case: Node = body.named_children[0]
        case_value: Node = case.child_by_field_name("value")

        nests = self._infestator.nests_of_case_value_for_switch(case_value)

        self.assertEqual(len(nests), 1)
        self.assertEqual(nests[0].type, "case_statement")

    def test_infect_for_with_only_break(self) -> None:
        program: str = "for(;;) break;"
        tree: Tree = self._parser.parse(program)
        cfg: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        actual = self._infestator.nests(cfg)
        

        self.assertTrue(cfg.nodes[0].node.is_type(CNodeType.BREAK_STATEMENT))

        self.assertEqual(len(actual), 2)
        self.assertTrue(actual[0].is_type(CNodeType.TRANSLATION_UNIT))
        self.assertTrue(actual[1].is_type(CNodeType.FOR_STATEMENT))

    def test_infect_switch(self) -> None:
        program: str = """
            switch(a) {
                case 3: { int a=3; }
                default:
            }
        """
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        expected =  """
            CANARY_TWEET_LOCATION(0);switch(a) {
                case 3:CANARY_TWEET_LOCATION(1); { int a=3; }
                default:CANARY_TWEET_LOCATION(2);
            }CANARY_TWEET_LOCATION(3);
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
        program: str = """
            goto SUM;
        SUM:
            sum = a + b;
        """
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)

        expected: str = """
            CANARY_TWEET_LOCATION(1);CANARY_TWEET_LOCATION(0);goto SUM;
        SUM:CANARY_TWEET_LOCATION(2);
            sum = a + b;
        """
        actual = self._infestator.infect(tree, cfa)

        self.assertEqual(expected, actual.text)
        self.assertTrue(True)

    def test_infect_if_consequence_no_compund_statement(self) -> None:
        program: str = "if (a) a=2;"
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)
        
        expected: str = "CANARY_TWEET_LOCATION(0);if (a) {CANARY_TWEET_LOCATION(2);a=2;}CANARY_TWEET_LOCATION(1);"
        actual = self._infestator.infect(tree, cfa).text

        self.assertEqual(expected, actual)

    def test_infect_if_alternative_no_compund_statement(self) -> None:
        program: str = "if (a) a=2; else a=3;"
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)
        
        expected: str = "CANARY_TWEET_LOCATION(0);if (a) {CANARY_TWEET_LOCATION(2);a=2;} else {CANARY_TWEET_LOCATION(3);a=3;}CANARY_TWEET_LOCATION(1);"
        actual = self._infestator.infect(tree, cfa).text

        self.assertEqual(expected, actual)

    def test_infect_function_body_with_unit(self) -> None:
        program: str = """
        void Foo() {
            a = b;
            return;
        }
        """
        tree: Tree = self._parser.parse(program)
        cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root.named_children[0].child_by_field(CField.BODY))

        expected: str = """
        void Foo() {CANARY_TWEET_LOCATION(0);
            a = b;
            return;
        }
        """
        actual = self._infestator.infect(tree, cfa)

        self.assertEqual(expected, actual.text)
        self.assertTrue(True)

    def test_infect_bunch(self) -> None:
        programs: List[Tuple[str, str, str]] = [
            ("if_1", 
            "a=1; if(a==2) { }",
            "TWEET();a=1; if(a==2) {TWEET(); }TWEET();"),
            ("if_2", 
            "if(a==2) { } else { }",
            "TWEET();if(a==2) {TWEET(); } else {TWEET(); }TWEET();"),
            ("if_3", 
            "a=1; if(a==2) { } else { } a=2;",
            "TWEET();a=1; if(a==2) {TWEET(); } else {TWEET(); }TWEET(); a=2;"),
            ("if_4", 
            "a=1; if(a==2) { } else if(a==3) { } else { }",
            "TWEET();a=1; if(a==2) {TWEET(); } else if(a==3) {TWEET(); } else {TWEET(); }TWEET();"),
            ("if_5", 
            "a=1; if(a==2) { } else if(a==3) { } a=2;",
            "TWEET();a=1; if(a==2) {TWEET(); } else if(a==3) {TWEET(); }TWEET(); a=2;"),
            ("if_6", 
            "a=1; if(a==1) { a=2; }",
            "TWEET();a=1; if(a==1) {TWEET(); a=2; }TWEET();"),
            ("if_7", 
            "a=1; if(a==1) { a=2; } a=3;",
            "TWEET();a=1; if(a==1) {TWEET(); a=2; }TWEET(); a=3;"),
            ("if_8", 
            "a=1; if(a==1) { a=2; } else { a=3; }",
            "TWEET();a=1; if(a==1) {TWEET(); a=2; } else {TWEET(); a=3; }TWEET();"),
            ("if_9", 
            "a=1; if(a==1) { a=2; } else { a=3; } a=4;",
            "TWEET();a=1; if(a==1) {TWEET(); a=2; } else {TWEET(); a=3; }TWEET(); a=4;"),
            ("if_10",
            "a=1; if(a==1) { a=2; } else if(a==2) { a=3; } a=4;",
            "TWEET();a=1; if(a==1) {TWEET(); a=2; } else if(a==2) {TWEET(); a=3; }TWEET(); a=4;"),
            ("if_11",
            "a=1; if(a==1) { a=2; } else if(a==2) { a=3; } a=4;",
            "TWEET();a=1; if(a==1) {TWEET(); a=2; } else if(a==2) {TWEET(); a=3; }TWEET(); a=4;"),
            ("if_12",
            "a=1; if(a==1) { a=2; } else if(a==2) { a=3; } else { a=4; } a=5; a=6;",
            "TWEET();a=1; if(a==1) {TWEET(); a=2; } else if(a==2) {TWEET(); a=3; } else {TWEET(); a=4; }TWEET(); a=5; a=6;"),
            ("if_13",
            "a=1; if(a==1) { a=2; } else if(a==2) { a=3; } else if(a==3) { a=4; } a=5;",
            "TWEET();a=1; if(a==1) {TWEET(); a=2; } else if(a==2) {TWEET(); a=3; } else if(a==3) {TWEET(); a=4; }TWEET(); a=5;"),
            ("if_14",
            "a=1; if(a==1) { a=2; } else if(a==2) { } else if(a==3) { a=4; } else if(a==4) { a=5; } else { a=6; } a=7;",
            "TWEET();a=1; if(a==1) {TWEET(); a=2; } else if(a==2) {TWEET(); } else if(a==3) {TWEET(); a=4; } else if(a==4) {TWEET(); a=5; } else {TWEET(); a=6; }TWEET(); a=7;"),
            ("if_15",
            "a=1; if(a==1) { a=2; } else if(a==2) { a=3; } else if(a==3) { a=4; } else if(a==4) { a=5; } else { a=6; } a=7;",
            "TWEET();a=1; if(a==1) {TWEET(); a=2; } else if(a==2) {TWEET(); a=3; } else if(a==3) {TWEET(); a=4; } else if(a==4) {TWEET(); a=5; } else {TWEET(); a=6; }TWEET(); a=7;"),
            ("if_16",
            "a=1; if(a==1) { a=2; } a=3; if(a==2) { a=2; } a=3; if(a==3) { a=2; } a=3;",
            "TWEET();a=1; if(a==1) {TWEET(); a=2; }TWEET(); a=3; if(a==2) {TWEET(); a=2; }TWEET(); a=3; if(a==3) {TWEET(); a=2; }TWEET(); a=3;"),
            ("if_17",
            "a=1; if((((a==1)))) { a=2; }",
            "TWEET();a=1; if((((a==1)))) {TWEET(); a=2; }TWEET();"),
            ("if_18",
            "a=1; if(a==1) { } a=3;",
            "TWEET();a=1; if(a==1) {TWEET(); }TWEET(); a=3;"),
            ("if_18",
            "a=1; if(a==1) { a=2; } else { } a=3;",
            "TWEET();a=1; if(a==1) {TWEET(); a=2; } else {TWEET(); }TWEET(); a=3;"),
            ("if_19",
            "if(a==1) { } if(a==3) { b=2; }",
            "TWEET();if(a==1) {TWEET(); }TWEET(); if(a==3) {TWEET(); b=2; }TWEET();"),
            ("if_20",
            "if(a==1) { a=1; a=2; } if(a==3) { b=2; }",
            "TWEET();if(a==1) {TWEET(); a=1; a=2; }TWEET(); if(a==3) {TWEET(); b=2; }TWEET();"),
            ("if_21",
            "if (a) { { { { { } } } } } else { a=2; } a=2;",
            "TWEET();if (a) {TWEET(); { { { { } } } } } else {TWEET(); a=2; }TWEET(); a=2;"),
            ("if_22",
            "if (a) { { A=1; { { { } b=2; } } } } else { a=2; } a=2;",
            "TWEET();if (a) {TWEET(); { A=1; { { { } b=2; } } } } else {TWEET(); a=2; }TWEET(); a=2;"),
            ("if_23",
            "if(a) { if(a) { } }",
            "TWEET();if(a) {TWEET(); if(a) {TWEET(); }TWEET(); }TWEET();"),
            ("if_24",
            "if(a) a=1;",
            "TWEET();if(a) {TWEET();a=1;}TWEET();"),
            ("if_25",
            "if(a) a=1; else a=2;",
            "TWEET();if(a) {TWEET();a=1;} else {TWEET();a=2;}TWEET();"),
            ("if_26",
            "if(a) a=1; else if(a) a=2;",
            "TWEET();if(a) {TWEET();a=1;} else if(a) {TWEET();a=2;}TWEET();"),
            ("if_27",
            "if(a) a=1; else if(a) a=2; else a=3;",
            "TWEET();if(a) {TWEET();a=1;} else if(a) {TWEET();a=2;} else {TWEET();a=3;}TWEET();"),
            ("if_28",
            "if(a) { { { { { } } } } }",
            "TWEET();if(a) {TWEET(); { { { { } } } } }TWEET();"),
        ]

        for program in programs:
            name: str = program[0]
            tree: Tree = self._parser.parse(program[1])
            expected =  program[2]
            cfa: CFA[CFANode] = CCFAFactory(tree).create(tree.root)
            canary_factory = SimpleTestCanaryFactory()
            infestator = CTreeInfestator(self._parser, canary_factory)
            actual = infestator.infect(tree, cfa).text
            self.assertEqual(actual, expected, f'Infestation for {name} failed')