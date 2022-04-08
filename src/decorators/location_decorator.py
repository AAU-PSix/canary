from typing import List, Dict
from ts.c_syntax import CNodeType
from ts import Tree, Node
from cfa import CFANode, CFA

class LocalisedNode(CFANode):
    def __init__(self, node: Node) -> None:
        self.location: str = ''
        super().__init__(node)

class LocalisedCFA(CFA[CFANode]):
    pass

class LocationDecorator():
    def __init__(self, tree: Tree) -> None:
        self.tree: Tree = tree
    
    def is_location_tweet(self, node: Node) -> bool:
        text = self.tree.contents_of(node)
        return text.startswith("CANARY_TWEET_LOCATION(")

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

    def map_node_to_location(self, cfa: CFA[CFANode]) -> Dict[CFANode, str]:
        location_tweets = self.get_all_location_tweet_nodes(cfa)
        result: Dict[CFANode, str] = dict()

        for tweet in location_tweets:
            location = self.extract_location_text_from_tweet(tweet.node)
            result[location] = tweet

        return result
    
    def decorate(self, cfa: CFA[CFANode]) -> CFA[LocalisedNode]:
        localised_cfa: CFA[LocalisedNode] = CFA(LocalisedNode(cfa.root.node))
        
        conversions: Dict[CFANode, LocalisedNode] = dict()

        for node in cfa.nodes:
            conversions[node] = LocalisedNode(node.node)
        return localised_cfa