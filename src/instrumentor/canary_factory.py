from abc import ABC, abstractmethod
from typing import Iterable
from ts import Node
from .tree_infection import TreeInfection
from .tree_infection_append import TreeInfectionAppend
from .tree_infection_insert import TreeInfectionInsert

class CanaryFactory(ABC):
    @abstractmethod
    def create_begin_test_tweet(self, _: str, prefix: str = "", postfix: str = "") -> str:
        pass

    @abstractmethod
    def create_end_test_tweet(self, _: str, prefix: str = "", postfix: str = "") -> str:
        pass

    @abstractmethod
    def create_begin_unit_tweet(self, _: str, prefix: str = "", postfix: str = "") -> str:
        pass

    @abstractmethod
    def create_end_unit_tweet(self, _: str, prefix: str = "", postfix: str = "") -> str:
        pass

    @abstractmethod
    def create_location_tweet(self, prefix: str = "", postfix: str = "") -> str:
        pass

    @abstractmethod
    def create_state_tweet(self, _: Node, prefix: str, postfix: str) -> str:
        pass

    def append(self, node: Node, text: str) -> TreeInfection:
        return TreeInfectionAppend(node, text)

    def insert(self, node: Node, text: str) -> TreeInfection:
        return TreeInfectionInsert(node, text)

    def append_location_tweet(self, node: Node, prefix: str = "", postfix: str = "") -> TreeInfection:
        tweet: str = self.create_location_tweet(prefix, postfix)
        return self.append(node, tweet)

    def insert_location_tweet(self, node: Node, prefix: str = "", postfix: str = "") -> TreeInfection:
        tweet: str = self.create_location_tweet(prefix, postfix)
        return self.insert(node, tweet)

    def append_state_tweet(self, node: Node, prefix: str = "", postfix: str = "") -> TreeInfection:
        tweet: str = self.create_state_tweet(node, prefix, postfix)
        return self.append(node, tweet)

    def insert_state_tweet(self, node: Node, prefix: str = "", postfix: str = "") -> TreeInfection:
        tweet: str = self.create_state_tweet(node, prefix, postfix)
        return self.insert(node, tweet)

    def append_begin_unit_tweet(self, unit: str, node: Node, prefix: str = "", postfix: str = "") -> TreeInfection:
        tweet: str = self.create_begin_unit_tweet(unit, prefix, postfix)
        return self.append(node, tweet)

    def insert_begin_unit_tweet(self, unit: str, node: Node, prefix: str = "", postfix: str = "") -> TreeInfection:
        tweet: str = self.create_begin_unit_tweet(unit, prefix, postfix)
        return self.insert(node, tweet)

    def append_end_unit_tweet(self, unit: str, node: Node, prefix: str = "", postfix: str = "") -> TreeInfection:
        tweet: str = self.create_end_unit_tweet(unit, prefix, postfix)
        return self.append(node, tweet)

    def insert_end_unit_tweet(self, unit: str, node: Node, prefix: str = "", postfix: str = "") -> TreeInfection:
        tweet: str = self.create_end_unit_tweet(unit, prefix, postfix)
        return self.insert(node, tweet)

    def append_test_tweet(self, test: str, node: Node, prefix: str = "", postfix: str = "") -> TreeInfection:
        tweet: str = self.create_begin_test_tweet(test, prefix, postfix)
        return self.append(node, tweet)

    def insert_test_tweet(self, test: str, node: Node, prefix: str = "", postfix: str = "") -> TreeInfection:
        tweet: str = self.create_begin_test_tweet(test, prefix, postfix)
        return self.insert(node, tweet)

    def surround_scope_tweet(
        self,
        node: Node,
        prefix: str = "",
        pre_infix: str = "",
        post_infix: str = "",
        postfix: str = "",
    ) -> Iterable[TreeInfection]:
        return [
            self.insert(node, prefix + "{" + pre_infix),
            self.append(node, post_infix + "}" + postfix),
        ]

    def surround_insert_location_tweet(
        self,
        node: Node,
        prefix: str = "",
        postfix: str = ""
    ) -> Iterable[TreeInfection]:
        return self.surround_scope_tweet(node, prefix + self.create_location_tweet(), postfix)

    def surround_insert_state_tweet(self, node: Node, prefix: str = "", postfix: str = "") -> Iterable[TreeInfection]:
        return self.surround_scope_tweet(node, prefix + self.create_state_tweet(), postfix)