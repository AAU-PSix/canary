from .point import Point
from tree_sitter.binding import Node as _Node

class Node:
    def __init__(self, _node: _Node):
        self._string: str = _node.string
        self._type: str = _node.type
        self._childCount: int = _node.childCount
        self._namedChildCount: int = _node.namedChildCount
        self._startByte: int = _node.startByte
        self._endByte: int = _node.endByte
        self._startPoint: Point = _node.startPoint
        self._endPoint: Point = _node.endPoint
        self._isNamed: bool = _node.isNamed
        self._isNull: bool = _node.isNull
        self._nextNamedSibling: Node = _node.nextNamedSibling
        self._node = _node

        pass
