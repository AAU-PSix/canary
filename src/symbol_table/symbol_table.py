from typing import Dict, List, TypeVar, Generic

class Type: pass

class CompositeField():
    def __init__(self, type: str, identifier: str) -> None:
        self._type = type
        self._identifier = identifier

    @property
    def type(self) -> str:
        return self._type

    @property
    def identifier(self) -> str:
        return self._identifier

class CompositeType(Type):
    """Structured data like structs and their fields
    """
    def __init__(self, composition: List[CompositeField]) -> None:
        self._composition = composition
        super().__init__()

    @property
    def composition(self) -> List[CompositeField]:
        return self._composition

class PointerType(Type):
    def __init__(self, type: str) -> None:
        super().__init__(type)

class AggregateType(Type):
    """Declaration of list/arrays
    """
    def __init__(self, type: str) -> None:
        super().__init__(type)

TNode = TypeVar("TNode", bound="Node")
class Tree(Generic[TNode]):
    def __init__(self, root: TNode) -> None:
        self._root = root

    @property
    def root(self) -> TNode:
        return self._root

class Node(Generic[TNode]):
    def __init__(
        self,
        parent: "TNode" = None,
        children: List["TNode"] = [ ],
    ) -> None:
        self._parent = parent
        self._children = children

    @property
    def parent(self) -> "TNode":
        return self._parent

    @property
    def siblings(self) -> List["TNode"]:
        if self.parent is None: return [ ]
        return self.parent.children

    @property
    def sibling_count(self) -> int:
        return len(self.siblings)

    @property
    def next_sibling(self) -> "TNode":
        index = self.siblings.index(self)
        # Check if the next siblings is out of bounds.
        if index + 1 == len(self.siblings) - 1: return None
        return self.siblings[index + 1]

    @property
    def previous_sibling(self) -> "TNode":
        index = self.siblings.index(self)
        # Check if the next siblings is out of bounds.
        if index - 1 < 0: return None
        return self.siblings[index - 1]

    @property
    def children(self) -> List["TNode"]:
        return self._children

    @property
    def first_child(self) -> "TNode":
        return self.children[0]

    @property
    def last_child(self) -> "TNode":
        return self.children[-1]

    @property
    def child_count(self) -> int:
        return len(self.children)

class SymbolTable(Node["SymbolTable"]):
    def __init__(
        self,
        parent: "SymbolTable" = None,
        children: List["SymbolTable"] = []
    ) -> None:
        self._declarations: Dict[str, Type] = dict()
        super().__init__(parent, children)

    def enter(self, identifier: str, declaration: Type) -> bool:
        if identifier in self._declarations: return False
        self._declarations[identifier] = declaration

    def lookup(self, identifier: str) -> Type:
        if identifier in self._declarations:
            return self._declarations[identifier]
        # Explicit case from "Node" to "SymbolTable"
        parent: SymbolTable = self._parent
        return None if parent is None else parent.lookup(identifier)

class SymbolTabelBuilder():
    def __init__(self, root: SymbolTable = SymbolTable()) -> None:
        self._root = root
        self._scope_stack = [ self._root ]

    @property
    def _current(self) -> SymbolTable:
        return self._scope_stack[-1]

    @property
    def depth(self) -> int:
        return len(self._scope_stack)

    def open(self) -> "SymbolTabelBuilder":
        new_table = SymbolTable(self._current)
        self._current.children.append(new_table)
        self._scope_stack.append(new_table)
        return self

    def enter(self, identifier: str, declaration: Type) -> "SymbolTabelBuilder":
        self._current.enter(identifier, declaration)
        return self

    def close(self) -> "SymbolTabelBuilder":
        if len(self._scope_stack) == 1:
            raise Exception("Cannot close root symbol table as forests are not supported")
        self._scope_stack.pop()
        return self

    def build(self) -> Tree[SymbolTable]:
        return Tree(self._root)