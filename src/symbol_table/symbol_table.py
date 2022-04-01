from typing import Dict, List
from .type import Type
from .tree import Tree, Node

class SymbolTable(Node["SymbolTable"]):
    def __init__(
        self,
        parent: "SymbolTable" = None,
        children: List["SymbolTable"] = list(),
    ) -> None:
        self._declarations: Dict[str, Type] = dict()
        super().__init__(parent, children)

    def enter(self, type: Type) -> bool:
        if type.identifier in self._declarations: return False
        self._declarations[type.identifier] = type
        return True

    def lookup(self, identifier: str) -> Type:
        if identifier in self._declarations:
            return self._declarations[identifier]
        # Explicit case from "Node" to "SymbolTable"
        parent: SymbolTable = self._parent
        return None if parent is None else parent.lookup(identifier)

    def has(self, identifier: str) -> bool:
        return self.lookup(identifier) is not None

class SymbolTabelBuilder():
    def __init__(self) -> None:
        self._root = SymbolTable(None, list())
        self._scope_stack = [ self._root ]

    @property
    def current(self) -> SymbolTable:
        return self._scope_stack[-1]

    @property
    def depth(self) -> int:
        return len(self._scope_stack)

    def open(self) -> "SymbolTabelBuilder":
        new_table = SymbolTable(self.current, list())
        self.current.children.append(new_table)
        self._scope_stack.append(new_table)
        return self

    def enter(self, type: Type) -> "SymbolTabelBuilder":
        self.current.enter(type)
        return self

    def close(self) -> "SymbolTabelBuilder":
        if len(self._scope_stack) == 1:
            raise Exception("Cannot close root symbol table as forests are not supported")
        self._scope_stack.pop()
        return self

    def build(self) -> Tree:
        return Tree(self._root)