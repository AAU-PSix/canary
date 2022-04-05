import os
from graphviz import Digraph
from typing import Dict, Generic, Iterable, List, TypeVar

from ts import Node as TsNode
from .type import CDeclaration, LexicalDeclaration, Type
from .tree import Tree, Node

TLexicalSymbolTable = TypeVar("TLexicalSymbolTable", bound="LexicalSymbolTable")
class LexicalSymbolTable(Generic[TLexicalSymbolTable], Node[TLexicalSymbolTable]):
    def __init__(
        self,
        minimum_lexical_index: int,
        maximum_lexical_index: int,
        parent: TLexicalSymbolTable = None,
        children: List[TLexicalSymbolTable] = list(),
    ) -> None:
        self._declarations: List[CDeclaration] = [ ]
        self._minimum_lexical_index = minimum_lexical_index
        self._maximum_lexical_index = maximum_lexical_index
        super().__init__(parent, children)

    @property
    def minimum_lexical_index(self) -> int:
        return self._minimum_lexical_index

    @property
    def maximum_lexical_index(self) -> int:
        return self._maximum_lexical_index

    @property
    def is_empty(self) -> bool:
        return len(self._declarations) == 0

    def enter(
        self,
        identifier: str,
        type: Type,
        lexical_index: int,
        storage_class_specifiers: List[str] = list(),
        type_qualifiers: List[str] = list(),
    ) -> bool:
        return self.enter_declaration(CDeclaration(
            identifier,
            type,
            lexical_index,
            storage_class_specifiers,
            type_qualifiers,
        ))

    def enter_declaration(
        self,
        declaration: CDeclaration
    ) -> bool:
        if self.lookup(declaration.identifier) is not None: return False
        self._declarations.append(declaration)
        return True

    def local_lookup(self, identifier: str) -> CDeclaration:
        for declaration in self._declarations:
            if declaration.identifier == identifier: return declaration
        return None

    def lookup(self, identifier: str) -> CDeclaration:
        for table in self.lexical_traversal():
            result = table.local_lookup(identifier)
            if result is not None: return result
        return None

    def local_index(self, identifier: str) -> int:
        for idx, declaration in enumerate(self._declarations):
            if declaration.identifier == identifier: return idx
        raise ValueError()

    def find(self, identifier: str) -> TLexicalSymbolTable:
        local_result = self.local_lookup(identifier)
        if local_result is not None: return self
        parent: TLexicalSymbolTable = self._parent
        return None if parent is None else parent.find(identifier)

    def local_identifiers(self) -> List[str]:
        return [ declaration.identifier for declaration in self._declarations ]

    def identifiers(self, lexical_bound: int = None) -> List[str]:
        start = self

        if lexical_bound is None:
            # If no lexical bound is defined then it is because
            #   we want every identifiers avaiable after this scope.
            lexical_bound = self.maximum_lexical_index + 1
        else:
            # If a lexical bound is defined then it is because
            #   we want all identifiers accesible at a given point.
            while start.parent is not None:
                start = start.parent

            # We loop until no child has the "lexical bound"
            #   within its scope, this can happen in the following case:
            # 0: {
            # 1:     {
            # 2:         int a;
            # 3:     }
            # 4:     int b;
            # 5:     {
            # 6:         int c;
            # 7:     }
            # 8: }
            # When search for the bound "4", should stop in the current scope
            #   even through it still has children - for this reason we have
            #   the "loop" variable which handles the iterative deepening.
            loop = True
            while loop:
                for child in start.children:
                    if lexical_bound <= child.maximum_lexical_index and \
                        lexical_bound >= child.minimum_lexical_index:
                        start = child
                        break
                loop = False

        identifiers = [ ]
        for table in start.lexical_traversal():
            for declaration in table._declarations:
                if self.can_be_referenced(declaration, lexical_bound):
                    identifiers.append(declaration.identifier)
        return identifiers

    def can_be_referenced(self, declaration: LexicalDeclaration, lexical_upper_bound: int) -> bool:
        return declaration.lexical_index < lexical_upper_bound

    def has_local(self, identifier: str) -> bool:
        for declaration in self._declarations:
            if declaration.identifier == identifier: return True
        return False

    def has(self, identifier: str) -> bool:
        return self.lookup(identifier) is not None

    def lexical_traversal(self) -> Iterable[TLexicalSymbolTable]:
        """Traverses the connected symbols tables in lexical order for declaration
        """
        curr: TLexicalSymbolTable = self
        while curr is not None:
            yield curr
            curr = curr.parent

    def draw(self, name: str, dot: Digraph = None) -> Digraph:
        if dot is None: dot = Digraph(name)

        def symbol_table_label(table: LexicalSymbolTable) -> str:
            label = f'[{table.minimum_lexical_index}, {table.maximum_lexical_index}]{os.linesep}'
            for declaration in table._declarations:
                label += f'[{declaration.lexical_index}] {declaration.type.__class__.__name__}::{declaration.identifier}\l{os.linesep}'
            return label

        ids: Dict[LexicalSymbolTable, str] = dict()
        counter: int = 0

        openset: List[LexicalSymbolTable] = list()
        openset.append(self)
        
        dot.attr('node', shape='square')
        while len(openset) > 0:
            curr = openset.pop()
            id = counter = counter + 1
            id = str(id)
            dot.node(id, symbol_table_label(curr))
            ids[curr] = id
            openset.extend(curr.children)

            if curr.parent is not None:
                parrent_id = ids[curr.parent]
                dot.edge(parrent_id, id)

        return dot

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