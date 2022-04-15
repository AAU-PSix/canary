from typing import Iterable
from ts import Node, CNodeType
from .tree_infection import TreeInfection
from .canary_factory import CanaryFactory

class CCanaryFactory(CanaryFactory):
    def __init__(self) -> None:
        self._previous_location = None
        self._current_location = 0
        super().__init__()

    @property
    def previous_location(self) -> str:
        return str(self._previous_location)

    @property
    def _next_location(self) -> int:
        curr = self._current_location
        self._previous_location = curr
        self._current_location += 1
        return curr

    def create_begin_test_tweet(self, test: str, prefix: str = "", postfix: str = "") -> str:
        return f"{prefix}CANARY_TWEET_BEGIN_TEST({test});{postfix}"

    def create_end_test_tweet(self, test: str, prefix: str = "", postfix: str = "") -> str:
        return f"{prefix}CANARY_TWEET_END_TEST({test});{postfix}"

    def create_begin_unit_tweet(self, unit: str, prefix: str = "", postfix: str = "") -> str:
        return f"{prefix}CANARY_TWEET_BEGIN_UNIT({unit});{postfix}"

    def create_end_unit_tweet(self, unit: str, prefix: str = "", postfix: str = "") -> str:
        return f"{prefix}CANARY_TWEET_END_UNIT({unit});{postfix}"

    def create_location_tweet(self, prefix: str = "", postfix: str = "", location: str = None) -> str:
        if location is None: location = self._next_location
        return f"{prefix}CANARY_TWEET_LOCATION({location});{postfix}"

    def create_state_tweet(self, _: Node, prefix: str, postfix: str) -> str:
        return f"{prefix}CANARY_TWEET_LOCATION(l);{postfix}"

    def create_location_tweets(
        self,
        node: Node,
        prefix: str = "",
        pre_infix: str = "",
        post_infix: str = "",
        postfix: str = "",
    ) -> Iterable[TreeInfection]:
        if node.is_type(CNodeType.COMPOUND_STATEMENT):
            # Appends a location tweet after the "{" (index 0 child of the "consequence")
            return [
                self.insert(node, prefix),
                self.append(node.children[0], pre_infix),
                self.insert(node.children[-1], post_infix),
                self.append(node, postfix),
            ]
        else:
            return [
                self.insert(node, prefix + "{" + pre_infix),
                self.append(node, post_infix + "}" + postfix),
            ]
        return self.surround_scope_tweet(
            node,
            prefix,
            pre_infix,
            post_infix,
            postfix
        )