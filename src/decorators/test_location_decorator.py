from decorators import *
from unittest import TestCase
from ts import (
    LanguageLibrary,
    Parser
)

from decorators.location_decorator import (
    LocationDecorator,
    LocalisedCFACFactory
)

class TestLocationDecorator(TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)

        return super().setUp()

    def test_returns_empty_string_on_no_match(self):
        program = "a=2;"
        p = self._parser.parse(program)
        factory = LocalisedCFACFactory(p)
        cfa = factory.create(p.root_node)
        decorator = LocationDecorator(factory, p)

        a = cfa.nodes[0]
        text = decorator.extract_location_text_from_tweet(a)
        self.assertIsNotNone(text)
        self.assertEqual('',text)
        self.assertNotEqual(' ', text)

    def test_always_passes(self):
        self.assertTrue(True)
  
    def test_can_detect_location_tweet_normal_letters(self):
        location_text = '12343ldæs'
        program = f"CANARY_TWEET_LOCATION({location_text});"
        p = self._parser.parse(program)
        factory = LocalisedCFACFactory(p)
        cfa = factory.create(p.root_node)
        decorator = LocationDecorator(factory, p)

        a = cfa.nodes[0]
        text = decorator.extract_location_text_from_tweet(a)
        self.assertEqual(location_text, text)

    def test_can_detect_location_tweet_special_chars(self):
        location_text = '\"(; ); _+098?=)(/&%¤#¡@£$€¥{[]}12343ldæs(;); ; );}][{!#¤%&/()=\"'
        program = f"CANARY_TWEET_LOCATION({location_text});"
        p = self._parser.parse(program)
        factory = LocalisedCFACFactory(p)
        cfa = factory.create(p.root_node)
        decorator = LocationDecorator(factory, p)

        a = cfa.nodes[0]
        text = decorator.extract_location_text_from_tweet(a)
        self.assertEqual(location_text, text)

    def test_can_detect_location_tweet_special_ends_with_parenthesis_and_semi_colon(self):
        location_text = '   \"abc;)\"'
        program = f"CANARY_TWEET_LOCATION({location_text});"
        p = self._parser.parse(program)
        factory = LocalisedCFACFactory(p)
        cfa = factory.create(p.root_node)
        decorator = LocationDecorator(factory, p)

        a = cfa.nodes[0]
        text = decorator.extract_location_text_from_tweet(a)
        self.assertEqual(location_text, text)
