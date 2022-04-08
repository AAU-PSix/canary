from decorators import *
from unittest import TestCase
from src.cfa.c_cfa_factory import CCFAFactory
from ts import (
    LanguageLibrary,
    Parser
)
from .location_decorator import (
    LocationDecorator
)

class TestLocationDecorator(TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)

        return super().setUp()

    def test_extract_location_text_from_tweet_returns_empty_string_on_no_location(self):
        program = "a=2;"
        tree = self._parser.parse(program)
        decorator = LocationDecorator(tree)
        expr_stmt = tree.root_node.first_named_child    

        text = decorator.extract_location_text_from_tweet(expr_stmt)

        self.assertIsNone(text)
  
    def test_can_detect_location_tweet_normal_letters(self):
        location_text = '12343ldæs'
        program = f"CANARY_TWEET_LOCATION({location_text});"
        tree = self._parser.parse(program)
        decorator = LocationDecorator(tree)
        expr_stmt = tree.root_node.first_named_child    

        text = decorator.extract_location_text_from_tweet(expr_stmt)

        self.assertEqual(location_text, text)

    def test_can_detect_location_tweet_special_chars(self):
        location_text = '\"(; ); _+098?=)(/&%¤#¡@£$€¥{[]}12343ldæs(;); ; );}][{!#¤%&/()=\"'
        program = f"CANARY_TWEET_LOCATION({location_text});"
        tree = self._parser.parse(program)
        decorator = LocationDecorator(tree)
        expr_stmt = tree.root_node.first_named_child    

        text = decorator.extract_location_text_from_tweet(expr_stmt)

        self.assertEqual(location_text, text)

    def test_can_detect_location_tweet_special_ends_with_parenthesis_and_semi_colon(self):
        location_text = '   \"abc;)\"'
        program = f"CANARY_TWEET_LOCATION({location_text});"
        tree = self._parser.parse(program)
        decorator = LocationDecorator(tree)
        expr_stmt = tree.root_node.first_named_child    

        text = decorator.extract_location_text_from_tweet(expr_stmt)

        self.assertEqual(location_text, text)
    
    def test_location_tweet_tree_node_starts_with_tweet_string(self):
        location_text = '   \"abc;)\"'
        program = f"CANARY_TWEET_LOCATION({location_text});"
        tree = self._parser.parse(program)
        decorator = LocationDecorator(tree)
        expr_stmt = tree.root_node.first_named_child

        text = decorator.extract_location_text_from_tweet(expr_stmt)
        
        self.assertEqual(location_text, text)

    def test_get_all_location_tweet_nodes_finds_cfa_nodes(self):
        program = """
        CANARY_TWEET_LOCATION(a);
        CANARY_TWEET_LOCATION(b);
        """
        tree = self._parser.parse(program)
        factory = CCFAFactory(tree)
        cfa = factory.create(tree.root_node)
        decorator = LocationDecorator(tree)

        tweet_nodes = decorator.get_all_location_tweet_nodes(cfa)
        tweet_a = cfa.root
        tweet_b = cfa.nodes[1]

        self.assertEqual(len(tweet_nodes), 2)
        self.assertEqual(tweet_nodes[0], tweet_a)
        self.assertEqual(tweet_nodes[1], tweet_b)

    def test_map_node_to_location_finds_all_locations(self):
        program = """
        CANARY_TWEET_LOCATION(a);
        CANARY_TWEET_LOCATION(b);
        """
        tree = self._parser.parse(program)
        factory = CCFAFactory(tree)
        cfa = factory.create(tree.root_node)
        decorator = LocationDecorator(tree)

        locations = decorator.map_node_to_location(cfa)
        tweet_a = cfa.root
        tweet_b = cfa.nodes[1]

        self.assertEqual(len(locations), 2)
        self.assertEqual(locations['a'], tweet_a)
        self.assertEqual(locations['b'], tweet_b)

    def test_decorate_program_4(self):
        program = """
        CANARY_TWEET_LOCATION(a);
        a=2;
        """
        tree = self._parser.parse(program)
        factory = CCFAFactory(tree)
        cfa = factory.create(tree.root_node)
        decorator = LocationDecorator(tree)

        localised_cfa = decorator.decorate(cfa)



