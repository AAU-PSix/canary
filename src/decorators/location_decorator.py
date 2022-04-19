
from typing import List, Dict
from ts.c_syntax import CSyntax
from ts import Tree
from cfa import CFANode, CFA, CFAEdge
from cfa import LocalisedCFA, LocalisedNode
from .tweet_handler import TweetHandler
from .decoration_strategy import StandardDecorationStrategy, DecorationStrategy
from .conversion_strategy import ConversionStrategy

class LocationDecorator():
    def __init__(
        self,
        tree: Tree,
        conversion_strategy: ConversionStrategy = None,
        tweet_handler: TweetHandler = None,
        decoration_strategy: DecorationStrategy = None
    ) -> None:
        self.tree: Tree = tree
        self._syntax = CSyntax()

        self.tweet_handler = tweet_handler if tweet_handler is not None else TweetHandler(self.tree)          
        self.decoration_strategy = decoration_strategy if decoration_strategy is not None else StandardDecorationStrategy(self.tweet_handler)
        self.edge_converter = conversion_strategy if conversion_strategy is not None else ConversionStrategy()

    def map_node_to_location(self, cfa: CFA[CFANode]) -> Dict[CFANode, str]:
        location_tweets = self.tweet_handler.get_all_location_tweet_nodes(cfa)
        result: Dict[CFANode, str] = dict()
        for tweet in location_tweets:
            location = self.tweet_handler.extract_location_text_from_tweet(tweet.node)
            result[location] = tweet
        return result

    def decorate(self, cfa: CFA[CFANode]) -> LocalisedCFA:
        localised_cfa: LocalisedCFA = self.convert_cfa_to_localised(cfa)

        # Step 1: Seed locations at tweet
        self.decoration_strategy.decorate_initial_locations(localised_cfa)

        # Step 2: Propagate seeds downwards
        frontier: List[LocalisedNode] = list()
        visited: List[LocalisedNode] = list()
        frontier.append(localised_cfa.root)

        while len(frontier) > 0:
            cfa_node = frontier.pop(-1)
            location = cfa_node.location
            visited.append(cfa_node)
            for edge in localised_cfa.outgoing_edges(cfa_node):
                self.decoration_strategy.decorate_frontier(frontier, visited, location, edge)

        # Step 3: Fixes where TWEETS comes after construct
        for cfa_node in localised_cfa.nodes:
            # Case 1: Switch cases propagation
            if self._syntax.is_switch_case(cfa_node.node):
                outgoings = localised_cfa.outgoing(cfa_node)
                # We can assume that each case is followed by a location tweet
                cfa_node.location = outgoings[0].location

        return localised_cfa

    def convert_cfa_to_localised(self, cfa: CFA[CFANode]) -> LocalisedCFA:
        # Step 1: Convert all CFANodes to Localised CFA Nodes (CFANode -> Localised CFA Node)
        converted_nodes: Dict[CFANode, LocalisedNode] = dict()
        for cfa_node in cfa.nodes:
            converted_nodes[cfa_node] = LocalisedNode(cfa_node.node)

        localised_cfa = LocalisedCFA(
            converted_nodes[cfa.root]
        )

        # Step 2: Reconstruct all edges
        converted_edges: List[CFAEdge[CFANode]] = list()
        for cfa_node in cfa.nodes:
            self.edge_converter.convert_edges(
                cfa.outgoing_edges(cfa_node),
                converted_edges,
                localised_cfa,
                converted_nodes
            )

            self.edge_converter.convert_edges(
                cfa.ingoing_edges(cfa_node),
                converted_edges,
                localised_cfa,
                converted_nodes
            )
        return localised_cfa