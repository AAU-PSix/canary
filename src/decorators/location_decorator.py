
from abc import ABC, abstractmethod
from typing import List, Dict
from cfa.t_cfa_node import TCFANode
from ts.c_syntax import CNodeType, CSyntax
from ts import Tree, Node
from cfa import CFANode, CFA, CFAEdge
from .localised_cfa import LocalisedCFA, LocalisedNode
class TweetHandler:

    def __init__(self, tree: Tree) -> None:
        self.tree = tree
        pass

    def extract_location_text_from_tweet(self, node: Node) -> str:
            if not node.is_type(CNodeType.EXPRESSION_STATEMENT):
                return None
            
            if self.is_location_tweet(node):
                text = self.tree.contents_of(node)
                return text.split("CANARY_TWEET_LOCATION(").pop()[:-2]
            return None

    def get_all_location_tweet_nodes(self, cfa: CFA[CFANode]) -> List[CFANode]:
        tweet_nodes: List[CFANode] = []
        for node in cfa.nodes:
            if self.is_location_tweet(node.node):
                tweet_nodes.append(node)
        return tweet_nodes

    def is_location_tweet(self, node: Node) -> bool:
        text = self.tree.contents_of(node)
        return text.startswith("CANARY_TWEET_LOCATION(")


class LocationDecorator():
    def __init__(self, tree: Tree) -> None:
        self.tree: Tree = tree
        self._syntax = CSyntax()
        self.tweet_handler = TweetHandler(self.tree)

    
        


    def extract_location_text_from_tweet(self, node: Node) -> str:
        if not node.is_type(CNodeType.EXPRESSION_STATEMENT):
            return None
        
        if self.tweet_handler.is_location_tweet(node):
            text = self.tree.contents_of(node)
            return text.split("CANARY_TWEET_LOCATION(").pop()[:-2]
        return None

    


    def map_node_to_location(self, cfa: CFA[CFANode]) -> Dict[CFANode, str]:
        location_tweets = self.tweet_handler.get_all_location_tweet_nodes(cfa)
        result: Dict[CFANode, str] = dict()

        for tweet in location_tweets:
            location = self.extract_location_text_from_tweet(tweet.node)
            result[location] = tweet

        return result

    def _convert_edges(self, edges: List[CFAEdge], converted_edges:List[CFAEdge],
                       localised_cfa:LocalisedCFA, converted_nodes: List[CFANode]):
        for edge in edges:
            if edge in converted_edges: continue
            localised_cfa.branch(
                converted_nodes[edge.source],
                converted_nodes[edge.destination],
                edge.label
            )
            converted_edges.append(edge)

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
            self._convert_edges(cfa.outgoing_edges(cfa_node),converted_edges, localised_cfa, converted_nodes)
            self._convert_edges(cfa.ingoing_edges(cfa_node),converted_edges, localised_cfa, converted_nodes)

        return localised_cfa

    def decorate(self, cfa: CFA[CFANode]) -> CFA[LocalisedNode]:
        localised_cfa: CFA[LocalisedNode] = self.convert_cfa_to_localised(cfa)
        # Step 1: Seed locations at tweet
        self._decorate_initial_locations(localised_cfa)

        # Step 2: Propagate seeds downwards
        frontier: List[LocalisedNode] = list()
        visited: List[LocalisedNode] = list()
        frontier.append(localised_cfa.root)

        while len(frontier) > 0:
            cfa_node = frontier.pop(-1)
            location = cfa_node.location
            visited.append(cfa_node)
            for edge in localised_cfa.outgoing_edges(cfa_node):
                self._decorate_frontier(frontier, visited, location, edge)

        # Step 3: Fixes where TWEETS comes after construct
        for cfa_node in localised_cfa.nodes:
            # Case 1: Switch cases propagation
            if self._syntax.is_switch_case(cfa_node.node):
                outgoings = localised_cfa.outgoing(cfa_node)
                # We can assume that each case is followed by a location tweet
                cfa_node.location = outgoings[0].location

        return localised_cfa

    def _decorate_frontier(self, frontier: List[LocalisedNode], visited: List[LocalisedNode],
                        location: str, edge: CFAEdge):

        if edge.destination not in visited and\
                    edge.destination not in frontier:
            frontier.append(edge.destination)
        if edge.destination.location is None:
            edge.destination.location = location

    def _decorate_initial_locations(self, localised_cfa: LocalisedCFA):
        for cfa_node in localised_cfa.nodes:
            if self.tweet_handler.is_location_tweet(cfa_node.node):
                location = self.tweet_handler.extract_location_text_from_tweet(cfa_node.node)
                cfa_node.location = location