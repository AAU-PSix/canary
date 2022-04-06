from typing import Generic, List
from ts import Node as TsNode
from .types import Type
from .c_types import CDeclaration
from .tree import Tree
from .lexical_symbol_table import (
    LexicalSymbolTable,
    TLexicalSymbolTable,
)

class LexicalSymbolTabelBuilder(Generic[TLexicalSymbolTable]):
    def __init__(
        self,
        minimum_lexical_index: int,
        maximum_lexical_index: int,
    ) -> None:
        self._root = self._create(
            minimum_lexical_index,
            maximum_lexical_index,
            None, list()
        )
        self._scope_stack = [ self._root ]

    @property
    def current(self) -> TLexicalSymbolTable:
        return self._scope_stack[-1]

    @property
    def depth(self) -> int:
        return len(self._scope_stack)

    def open_for(
        self, node: TsNode
    ) -> "LexicalSymbolTabelBuilder[TLexicalSymbolTable]":
        return self.open(node.start_byte, node.end_byte)

    def open(
        self,
        minimum_lexical_index: int,
        maximum_lexical_index: int
    ) -> "LexicalSymbolTabelBuilder[TLexicalSymbolTable]":
        new_table = self._create(
            minimum_lexical_index,
            maximum_lexical_index,
            self.current,
            list()
        )
        self.current.children.append(new_table)
        self._scope_stack.append(new_table)
        return self

    def enter_declaration(
        self,
        declaration: CDeclaration
    ) -> "LexicalSymbolTabelBuilder[TLexicalSymbolTable]":
        self.current.enter_declaration(declaration)

    def enter(
        self,
        identifier: str,
        type: Type,
        lexical_index: int,
        storage_class_specifiers: List[str] = list(),
        type_qualifiers: List[str] = list(),
    ) -> "LexicalSymbolTabelBuilder[TLexicalSymbolTable]":
        self.current.enter(
            identifier,
            type,
            lexical_index,
            storage_class_specifiers,
            type_qualifiers,
        )
        return self

    def close(self) -> "LexicalSymbolTabelBuilder[TLexicalSymbolTable]":
        if len(self._scope_stack) == 1:
            raise Exception("Cannot close root symbol table as forests are not supported")
        self._scope_stack.pop()
        return self

    def _create(
        self,
        minimum_lexical_index: int,
        maximum_lexical_index: int,
        parent: "TLexicalSymbolTable" = None,
        children: List["TLexicalSymbolTable"] = list(),
    ) -> TLexicalSymbolTable:
        return LexicalSymbolTable[LexicalSymbolTable](
            minimum_lexical_index,
            maximum_lexical_index,
            parent,
            children
        )

    def build(self) -> Tree[TLexicalSymbolTable]:
        return Tree(self._root)