from typing import List
from decorators import *
from unittest import TestCase
from cfa import CCFAFactory, CFAEdge, CFANode
from ts import (
    LanguageLibrary,
    Parser
)
from . import (
    LocationDecorator,
    LocalisedNode
)

class TestLocationDecorator(TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)

        return super().setUp()

    def assertIngoingEqual(self, a: List[CFAEdge[CFANode]], b: List[CFAEdge[CFANode]], ingoing_amount: int = None):
        if len(a) == 0 or len(b) == 0:
            return

        sources_from_a = [ ingoing.source.node for ingoing in a ]
        sources_from_b = [ ingoing.source.node for ingoing in b ]

        if ingoing_amount is not None:
            self.assertEqual(len(sources_from_a), ingoing_amount)
            self.assertEqual(len(sources_from_b), ingoing_amount)
        self.assertEqual(len(sources_from_a), len(sources_from_b))

        destinations_from_a = [ ingoing.destination.node for ingoing in a ]
        destinations_from_b = [ ingoing.destination.node for ingoing in b ]
        correct_destination = destinations_from_a[0]
        for idx, _ in enumerate(destinations_from_a):
            self.assertEqual(destinations_from_a[idx], correct_destination)
            self.assertEqual(destinations_from_b[idx], correct_destination)

        for source in sources_from_a:
            self.assertIn(source, sources_from_b)

    def assertOutgoingEqual(self, a: List[CFAEdge[CFANode]], b: List[CFAEdge[CFANode]], outgoing_amount: int = None):
        if len(a) == 0 or len(b) == 0:
            return

        destinations_from_a = [ outgoing.destination.node for outgoing in a ]
        destinations_from_b = [ outgoing.destination.node for outgoing in b ]

        if outgoing_amount is not None:
            self.assertEqual(len(destinations_from_a), outgoing_amount)
            self.assertEqual(len(destinations_from_b), outgoing_amount)
        self.assertEqual(len(destinations_from_a), len(destinations_from_b))

        sources_from_a = [ outgoing.source.node for outgoing in a ]
        sources_from_b = [ outgoing.source.node for outgoing in b ]
        correct_source = sources_from_a[0]
        for idx, _ in enumerate(sources_from_a):
            self.assertEqual(sources_from_a[idx], correct_source)
            self.assertEqual(sources_from_b[idx], correct_source)

        for destination in destinations_from_a:
            self.assertIn(destination, destinations_from_b)

    def assertBranchEqual(self, a: CFAEdge[CFANode], b: CFAEdge[CFANode]):
        self.assertEqual(a.source.node, b.source.node)
        self.assertEqual(a.destination.node, b.destination.node)
        self.assertEqual(a.label, b.label)

    def test_extract_location_text_from_tweet_returns_empty_string_on_no_location(self):
        program = "a=2;"
        tree = self._parser.parse(program)
        decorator = LocationDecorator(tree)
        expr_stmt = tree.root.first_named_child    

        text = decorator.tweet_handler.extract_location_text_from_tweet(expr_stmt)

        self.assertIsNone(text)
  
    def test_can_detect_location_tweet_normal_letters(self):
        location_text = '12343ldæs'
        program = f"CANARY_TWEET_LOCATION({location_text});"
        tree = self._parser.parse(program)
        decorator = LocationDecorator(tree)
        expr_stmt = tree.root.first_named_child    

        text = decorator.tweet_handler.extract_location_text_from_tweet(expr_stmt)

        self.assertEqual(location_text, text)

    def test_can_detect_location_tweet_special_chars(self):
        location_text = '\"(; ); _+098?=)(/&%¤#¡@£$€¥{[]}12343ldæs(;); ; );}][{!#¤%&/()=\"'
        program = f"CANARY_TWEET_LOCATION({location_text});"
        tree = self._parser.parse(program)
        decorator = LocationDecorator(tree)
        expr_stmt = tree.root.first_named_child    

        text = decorator.tweet_handler.extract_location_text_from_tweet(expr_stmt)

        self.assertEqual(location_text, text)

    def test_can_detect_location_tweet_special_ends_with_parenthesis_and_semi_colon(self):
        location_text = '   \"abc;)\"'
        program = f"CANARY_TWEET_LOCATION({location_text});"
        tree = self._parser.parse(program)
        decorator = LocationDecorator(tree)
        expr_stmt = tree.root.first_named_child    

        text = decorator.tweet_handler.extract_location_text_from_tweet(expr_stmt)

        self.assertEqual(location_text, text)
    
    def test_location_tweet_tree_node_starts_with_tweet_string(self):
        location_text = '   \"abc;)\"'
        program = f"CANARY_TWEET_LOCATION({location_text});"
        tree = self._parser.parse(program)
        decorator = LocationDecorator(tree)
        expr_stmt = tree.root.first_named_child

        text = decorator.tweet_handler.extract_location_text_from_tweet(expr_stmt)
        
        self.assertEqual(location_text, text)

    def test_get_all_location_tweet_nodes_finds_cfa_nodes(self):
        program = """
        CANARY_TWEET_LOCATION(a);
        CANARY_TWEET_LOCATION(b);
        """
        tree = self._parser.parse(program)
        factory = CCFAFactory(tree)
        cfa = factory.create(tree.root)
        decorator = LocationDecorator(tree)

        tweet_nodes = decorator.tweet_handler.get_all_location_tweet_nodes(cfa)
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
        cfa = factory.create(tree.root)
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
        cfa = factory.create(tree.root)
        decorator = LocationDecorator(tree)
        decorator.decorate(cfa)

    def test_convert_cfa_to_localised_root_conversion(self) -> None:
        program = """
            a=2;
        """
        tree = self._parser.parse(program)
        factor = CCFAFactory(tree)
        cfa = factor.create(tree.root)
        decorator = LocationDecorator(tree)

        localised_cfa = decorator.convert_cfa_to_localised(cfa)

        self.assertIsInstance(localised_cfa.root, LocalisedNode)
        self.assertEqual(cfa.root.node, localised_cfa.root.node)

    def test_convert_cfa_to_localised_sequential_branch_conversion(self) -> None:
        program = """
            a=2;
            b=2;
        """
        tree = self._parser.parse(program)
        factor = CCFAFactory(tree)
        cfa = factor.create(tree.root)
        decorator = LocationDecorator(tree)

        localised_cfa = decorator.convert_cfa_to_localised(cfa)

        a_cfa_node = cfa.root
        b_cfa_node = cfa.nodes[-1]

        a_cfa_localised_node = localised_cfa.root
        b_cfa_localised_node = localised_cfa.nodes[-1]

        self.assertEqual(a_cfa_node.node, a_cfa_localised_node.node)
        self.assertEqual(b_cfa_node.node, b_cfa_localised_node.node)

        self.assertOutgoingEqual(
            cfa.outgoing_edges(a_cfa_node),
            localised_cfa.outgoing_edges(a_cfa_localised_node),
            outgoing_amount = 1
        )
        self.assertOutgoingEqual(
            cfa.outgoing_edges(b_cfa_node),
            localised_cfa.outgoing_edges(b_cfa_localised_node),
            outgoing_amount = 0
        )

        self.assertIngoingEqual(
            cfa.ingoing_edges(a_cfa_node),
            localised_cfa.ingoing_edges(a_cfa_localised_node),
            ingoing_amount = 0
        )
        self.assertIngoingEqual(
            cfa.ingoing_edges(b_cfa_node),
            localised_cfa.ingoing_edges(b_cfa_localised_node),
            ingoing_amount = 1
        )

    def test_convert_cfa_to_localised_if_else_branch_conversion(self) -> None:
        #   0:a
        #     |
        #   1:b
        #    / \
        # 2:c 3:d
        program = """
            a=2;
            if(b == 2) {
                c = 1;
            } else {
                d = 3;
            }
        """
        tree = self._parser.parse(program)
        factor = CCFAFactory(tree)
        cfa = factor.create(tree.root)
        decorator = LocationDecorator(tree)

        localised_cfa = decorator.convert_cfa_to_localised(cfa)

        a_cfa_node = cfa.nodes[0]
        b_cfa_node = cfa.nodes[1]
        c_cfa_node = cfa.nodes[2]
        d_cfa_node = cfa.nodes[3]

        a_cfa_localised_node = localised_cfa.nodes[0]
        b_cfa_localised_node = localised_cfa.nodes[1]
        c_cfa_localised_node = localised_cfa.nodes[2]
        d_cfa_localised_node = localised_cfa.nodes[3]

        self.assertIsNotNone(a_cfa_node.node)
        self.assertIsNotNone(b_cfa_node.node)
        self.assertIsNotNone(c_cfa_node.node)
        self.assertIsNotNone(d_cfa_node.node)

        self.assertIsNotNone(a_cfa_localised_node.node)
        self.assertIsNotNone(b_cfa_localised_node.node)
        self.assertIsNotNone(c_cfa_localised_node.node)
        self.assertIsNotNone(d_cfa_localised_node.node)

        self.assertEqual(a_cfa_node.node, a_cfa_localised_node.node)
        self.assertEqual(b_cfa_node.node, b_cfa_localised_node.node)
        self.assertEqual(c_cfa_node.node, c_cfa_localised_node.node)
        self.assertEqual(d_cfa_node.node, d_cfa_localised_node.node)

        self.assertOutgoingEqual(
            cfa.outgoing_edges(a_cfa_node),
            localised_cfa.outgoing_edges(a_cfa_localised_node),
            outgoing_amount = 1
        )

        self.assertOutgoingEqual(
            cfa.outgoing_edges(b_cfa_node),
            localised_cfa.outgoing_edges(b_cfa_localised_node),
            outgoing_amount = 2
        )

        self.assertOutgoingEqual(
            cfa.outgoing_edges(c_cfa_node),
            localised_cfa.outgoing_edges(c_cfa_localised_node),
            outgoing_amount = 0
        )

        self.assertOutgoingEqual(
            cfa.outgoing_edges(d_cfa_node),
            localised_cfa.outgoing_edges(d_cfa_localised_node),
            outgoing_amount = 0
        )

        self.assertIngoingEqual(
            cfa.ingoing_edges(a_cfa_node),
            localised_cfa.ingoing_edges(a_cfa_localised_node),
            ingoing_amount=0
        )

        self.assertIngoingEqual(
            cfa.ingoing_edges(b_cfa_node),
            localised_cfa.ingoing_edges(b_cfa_localised_node),
            ingoing_amount=1
        )

        self.assertIngoingEqual(
            cfa.ingoing_edges(c_cfa_node),
            localised_cfa.ingoing_edges(c_cfa_localised_node),
            ingoing_amount=1
        )

        self.assertIngoingEqual(
            cfa.ingoing_edges(d_cfa_node),
            localised_cfa.ingoing_edges(d_cfa_localised_node),
            ingoing_amount=1
        )

    def test_decorate_check_nest_location_tweets_single_tweet(self):
        program = """
        CANARY_TWEET_LOCATION(a);
        """
        tree = self._parser.parse(program)
        factory = CCFAFactory(tree)
        cfa = factory.create(tree.root)
        decorator = LocationDecorator(tree)

        localised_cfa = decorator.decorate(cfa)

        self.assertEqual(localised_cfa.root.location, "a")

    def test_decorate_check_nest_location_tweets_two_tweets(self):
        program = """
        CANARY_TWEET_LOCATION(a);
        int a = 0;
        CANARY_TWEET_LOCATION(b);
        """
        tree = self._parser.parse(program)
        factory = CCFAFactory(tree)
        cfa = factory.create(tree.root)
        decorator = LocationDecorator(tree)

        localised_cfa = decorator.decorate(cfa)

        self.assertEqual(localised_cfa.nodes[0].location, "a")
        self.assertEqual(localised_cfa.nodes[-1].location, "b")

    def test_decorate_program_11(self):
        program = """
        CANARY_TWEET_LOCATION(0);
            do {CANARY_TWEET_LOCATION(1); a=a; CANARY_TWEET_LOCATION(0);} while(0);CANARY_TWEET_LOCATION(2);

            while(1) {CANARY_TWEET_LOCATION(3); a=a; break; CANARY_TWEET_LOCATION(2);}CANARY_TWEET_LOCATION(4);
            for(;;) {CANARY_TWEET_LOCATION(7);{CANARY_TWEET_LOCATION(5);break;CANARY_TWEET_LOCATION(6);}CANARY_TWEET_LOCATION(8);CANARY_TWEET_LOCATION(4);}CANARY_TWEET_LOCATION(6);

            for (;0;) {CANARY_TWEET_LOCATION(9);a=a;CANARY_TWEET_LOCATION(8);}CANARY_TWEET_LOCATION(10);

            if (a==a) {CANARY_TWEET_LOCATION(11); a=a; }
            else if(b==b) {CANARY_TWEET_LOCATION(13); b=b; }
            else {CANARY_TWEET_LOCATION(14); b=b; }CANARY_TWEET_LOCATION(12);

            int sum;
            CANARY_TWEET_LOCATION(15);goto SUM;
        SUM:CANARY_TWEET_LOCATION(16);
            sum = a + b;
            return sum;
        """
        tree = self._parser.parse(program)
        factory = CCFAFactory(tree)
        cfa = factory.create(tree.root)
        decorator = LocationDecorator(tree)

        localised_cfa = decorator.decorate(cfa)
        
        for node in localised_cfa.nodes:
            self.assertIsNotNone(node.location, f'{node.node.start_byte}, {node.node.end_byte} :: {tree.contents_of(node.node)}')