from typing import Iterable, List
from .type import Type
from .tree import Tree, Node

class Declaration():
    def __init__(self, identifier: str, type: Type) -> None:
        self._identifier = identifier
        self._type = type

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def type(self) -> Type:
        return self._type

class LexicalSymbolTable(Node["LexicalSymbolTable"]):
    def __init__(
        self,
        parent: "LexicalSymbolTable" = None,
        children: List["LexicalSymbolTable"] = list(),
    ) -> None:
        self._declarations: List[Declaration] = [ ]
        super().__init__(parent, children)

    def enter(self, identifier: str, type: Type) -> bool:
        for declaration in self._declarations:
            if declaration.identifier == identifier: return False
        self._declarations.append(Declaration(identifier, type))
        return True

    def local_lookup(self, identifier: str) -> Type:
        for declaration in self._declarations:
            if declaration.identifier == identifier: return declaration.type
        return None

    def lookup(self, identifier: str) -> Type:
        local_result = self.local_lookup(identifier)
        if local_result is not None: return local_result
        parent: LexicalSymbolTable = self._parent
        return None if parent is None else parent.lookup(identifier)

    def local_index(self, identifier: str) -> int:
        for idx, declaration in enumerate(self._declarations):
            if declaration.identifier == identifier: return idx
        raise ValueError()

    def find(self, identifier: str) -> "LexicalSymbolTable":
        local_result = self.local_lookup(identifier)
        if local_result is not None: return self
        parent: LexicalSymbolTable = self._parent
        return None if parent is None else parent.find(identifier)

    def local_identifiers(self, index: int = None) -> List[str]:
        if index is None: index = len(self._declarations) - 1
        return [ declaration.identifier for declaration in self._declarations[0 : index + 1] ]

    def identifiers(self, index: int = None) -> List[str]:
        identifiers = self.local_identifiers(index)

        for table in self.lexical_traversal():
            if table is self: continue
            for declaration in table._declarations:
                identifiers.append(declaration.identifier)
        return identifiers

    def has_local(self, identifier: str) -> bool:
        for declaration in self._declarations:
            if declaration.identifier == identifier: return True
        return False

    def has(self, identifier: str) -> bool:
        return self.lookup(identifier) is not None

    def lexical_traversal(self) -> Iterable["LexicalSymbolTable"]:
        """Traverses the connected symbols tables in lexical order for declaration
        """
        closed_set: List[LexicalSymbolTable] = [ ]
        curr: LexicalSymbolTable = self
        while curr is not None:
            if curr.child_count > 0 and \
                curr.first_child not in closed_set:
                curr = curr.first_child
            yield curr
            closed_set.append(curr)
            if not curr.has_previous_sibling:
                curr = curr.parent
            else: curr = curr.previous_sibling

class LexicalSymbolTabelBuilder():
    def __init__(self) -> None:
        self._root = LexicalSymbolTable(None, list())
        self._scope_stack = [ self._root ]

    @property
    def current(self) -> LexicalSymbolTable:
        return self._scope_stack[-1]

    @property
    def depth(self) -> int:
        return len(self._scope_stack)

    def open(self) -> "LexicalSymbolTabelBuilder":
        new_table = LexicalSymbolTable(self.current, list())
        self.current.children.append(new_table)
        self._scope_stack.append(new_table)
        return self

    def enter(self, identifier: str, type: Type) -> "LexicalSymbolTabelBuilder":
        self.current.enter(identifier, type)
        return self

    def close(self) -> "LexicalSymbolTabelBuilder":
        if len(self._scope_stack) == 1:
            raise Exception("Cannot close root symbol table as forests are not supported")
        self._scope_stack.pop()
        return self

    def build(self) -> Tree[LexicalSymbolTable]:
        return Tree(self._root)