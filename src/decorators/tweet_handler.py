from ts.c_syntax import CNodeType
from ts import Tree, Node
from cfa import CFANode, CFA
from typing import List

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
