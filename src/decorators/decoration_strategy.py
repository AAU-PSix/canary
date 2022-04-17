
from abc import ABC, abstractmethod
from typing import List
from cfa import CFAEdge
from cfa import LocalisedCFA, LocalisedNode
from .tweet_handler import TweetHandler

class DecorationStrategy(ABC):
    
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def decorate_frontier(
        self,
        frontier: List[LocalisedNode],
        visited: List[LocalisedNode],
        location: str,
        edge: CFAEdge[LocalisedNode]
    ): pass

    @abstractmethod
    def decorate_initial_locations(self, localised_cfa: LocalisedCFA):
        pass

class StandardDecorationStrategy(DecorationStrategy):
    def __init__(self, tweet_handler: TweetHandler) -> None:
        self.tweet_handler = tweet_handler

    def decorate_frontier(
        self,
        frontier: List[LocalisedNode],
        visited: List[LocalisedNode],
        location: str,
        edge: CFAEdge[LocalisedNode]
    ):
        if edge.destination not in visited and \
            edge.destination not in frontier:
            frontier.append(edge.destination)

        if edge.destination.location is None:
            edge.destination.location = location

    def decorate_initial_locations(self, localised_cfa: LocalisedCFA):
        for cfa_node in localised_cfa.nodes:
            if self.tweet_handler.is_location_tweet(cfa_node.node):
                location = self.tweet_handler.extract_location_text_from_tweet(cfa_node.node)
                cfa_node.location = location
