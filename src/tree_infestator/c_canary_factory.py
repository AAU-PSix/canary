from typing import Iterable
from ts import Node, CNodeType
from .tree_infection import TreeInfection
from .canary_factory import CanaryFactory

class CCanaryFactory(CanaryFactory):
    def create_location_tweet(self, prefix: str = "", postfix: str = "") -> str:
        return f"{prefix}CANARY_TWEET_LOCATION(l);{postfix}"

    def create_state_tweet(self, prefix: str = "", postfix: str = "") -> str:
        return f"{prefix}CANARY_TWEET_LOCATION(l);{postfix}"
    
    def create_location_tweets(self, node: Node) -> Iterable[TreeInfection]:
        if node.is_type(CNodeType.COMPOUND_STATEMENT):
            # Appends a location tweet after the "{" (index 0 child of the "consequence")
            return [ self.append_location_tweet(node.children[0]) ]
        return self.surround_insert_location_tweet(node, "{", "}")