from typing import Iterable
from symbol_table import SymbolTable
from ts import Node, CNodeType
from .tree_infection import TreeInfection
from .canary_factory import CanaryFactory

class CCanaryFactory(CanaryFactory):
    def __init__(self, symbol_table: SymbolTable = SymbolTable()) -> None:
        self._current_location = 0
        self._symbol_table = symbol_table
        super().__init__()

    @property
    def _next_location(self) -> int:
        curr = self._current_location
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

    def create_location_tweet(self, prefix: str = "", postfix: str = "") -> str:
        return f"{prefix}CANARY_TWEET_LOCATION({self._next_location});{postfix}"

    def create_state_tweet(self, _: Node, prefix: str, postfix: str) -> str:
        return f"{prefix}CANARY_TWEET_LOCATION(l);{postfix}"

    def create_location_tweets(self, node: Node) -> Iterable[TreeInfection]:
        if node.is_type(CNodeType.COMPOUND_STATEMENT):
            # Appends a location tweet after the "{" (index 0 child of the "consequence")
            return [ self.append_location_tweet(node.children[0]) ]
        return self.surround_insert_location_tweet(node, "{", "}")