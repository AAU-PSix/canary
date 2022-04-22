from ts import Parser
from .mutation_strategy import *
from .obom_strategy import *

class MutationStrategyFactory():
    def __init__(self) -> None:
        pass

    def create(
        self,
        name: str,
        parser: Parser,
    ) -> MutationStrategy:
        if name == "obom": return ObomStrategy(parser)