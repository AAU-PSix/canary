from abc import ABC, abstractmethod
from typing import Iterable
from ts import Node
from .tree_infection import TreeInfection
from .tree_infection_append import TreeInfectionAppend
from .tree_infection_insert import TreeInfectionInsert

class CanaryFactory(ABC):
    @abstractmethod
    def create_location_tweet(self, prefix: str = "", postfix: str = "") -> str:
        pass

    @abstractmethod
    def create_state_tweet(self, prefix: str = "", postfix: str = "") -> str:
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
        tweet: str = self.create_state_tweet(prefix, postfix)
        return self.append(node, tweet)

    def insert_state_tweet(self, node: Node, prefix: str = "", postfix: str = "") -> TreeInfection:
        tweet: str = self.create_state_tweet(prefix, postfix)
        return self.insert(node, tweet)

    def surround_scope_tweet(self, node: Node, prefix: str = "", postfix: str = "") -> Iterable[TreeInfection]:
        return [
            self.insert(node, prefix),
            self.append(node, postfix)
        ]

    def surround_insert_location_tweet(self, node: Node, prefix: str = "", postfix: str = "") -> Iterable[TreeInfection]:
        return self.surround_scope_tweet(node, f'{prefix}{self.create_location_tweet()}', postfix)

    def surround_insert_state_tweet(self, node: Node, prefix: str = "", postfix: str = "") -> Iterable[TreeInfection]:
        return self.surround_scope_tweet(node, f'{prefix}{self.create_state_tweet()}', postfix)