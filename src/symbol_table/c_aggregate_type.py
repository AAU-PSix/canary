from .type import Type
from .aggregate_type import AggregateType

class CAggregateType(AggregateType):
    def __init__(self, type: Type) -> None:
        super().__init__(type)