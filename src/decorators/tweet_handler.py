from ts.c_syntax import CNodeType
from ts import Tree, Node
from cfa import CFANode, CFA
from typing import List

class TweetHandler:
    def __init__(self, tree: Tree) -> None:
        self.tree = tree

    def extract_location_text_from_tweet(self, node: Node) -> str:
        if node.is_type(CNodeType.LABELED_STATEMENT):
            return self.extract_location_text_from_tweet(
                node.named_children[-1]
            )

        if not node.is_type(CNodeType.EXPRESSION_STATEMENT):
            return None

        if self.is_location_tweet(node):
            text = self.tree.contents_of(node)
            return text.split("CANARY_TWEET_LOCATION(").pop()[:-2]
        return None

    def get_all_location_tweet_nodes(self, cfa: CFA[CFANode]) -> List[CFANode]:
        return [node for node in cfa.nodes if self.is_location_tweet(node.node)]

    def is_location_tweet(self, node: Node) -> bool:
        if node.is_type(CNodeType.LABELED_STATEMENT):
            return self.is_location_tweet(node.named_children[-1])

        text = self.tree.contents_of(node)
        return text.startswith("CANARY_TWEET_LOCATION(")
