from typing import Iterable
from abc import ABC, abstractmethod
from enum import Enum

class Field(Enum): pass
class NodeType(Enum): pass

class Syntax(ABC):
    def is_type(self, node_type: str, field: NodeType) -> bool:
        return node_type == field.value

    def in_types(self, node_type: str, fields: Iterable[NodeType]) -> bool:
        return self.node_field(node_type) in fields

    @abstractmethod
    def node_field(self, node_type: str) -> NodeType:
        pass