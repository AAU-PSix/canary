from typing import Iterable
from abc import ABC, abstractmethod
from enum import Enum
from .node import Node

class Field(Enum): pass
class NodeType(Enum): pass

class Syntax(ABC):
    @abstractmethod
    def is_field(self, node_type: str, field: NodeType) -> bool:
        pass

    @abstractmethod
    def in_fields(self, node_type: str, fields: Iterable[NodeType]) -> bool:
        pass

    @abstractmethod
    def node_field(self, node_type: str) -> NodeType:
        pass

    @abstractmethod
    def child_by_field(self, node: Node, field: Field) -> Node:
        pass