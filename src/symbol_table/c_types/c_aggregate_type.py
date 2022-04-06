from symbol_table.types import (
    Type,
    AggregateType
)

class CAggregateType(AggregateType):
    def __init__(self, type: Type) -> None:
        super().__init__(type)