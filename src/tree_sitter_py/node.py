import Point


class Node:
    def __init__(self, node_obj):
        self._string: str = node_obj.string
        self._type: str = node_obj.type
        self._childCount: int = node_obj.childCount
        self._namedChildCount: int = node_obj.namedChildCount
        self._startByte: int = node_obj.startByte
        self._endByte: int = node_obj.endByte
        self._startPoint: Point = node_obj.startPoint
        self._endPoint: Point = node_obj.endPoint
        self._isNamed: bool = node_obj.isNamed
        self._isNull: bool = node_obj.isNull
        self._nextNamedSibling: Node = node_obj.nextNamedSibling
        self._internalNode = node_obj

        pass
