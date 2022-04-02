from typing import Iterable, List
from .type import SubroutineType, Type
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

class LexicalDeclaration(Declaration):
    def __init__(self, identifier: str, type: Type, lexical_index: int) -> None:
        self._lexical_index = lexical_index
        super().__init__(identifier, type)

    @property
    def lexical_index(self) -> int:
        return self._lexical_index

class LexicalSymbolTable(Node["LexicalSymbolTable"]):
    def __init__(
        self,
        minimum_lexical_index: int,
        maximum_lexical_index: int,
        parent: "LexicalSymbolTable" = None,
        children: List["LexicalSymbolTable"] = list(),
    ) -> None:
        self._declarations: List[LexicalDeclaration] = [ ]
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

    def enter(self, identifier: str, type: Type, lexical_index: int) -> bool:
        if self.lookup(identifier) is not None: return False
        declaration = LexicalDeclaration(identifier, type, lexical_index)
        self._declarations.append(declaration)
        return True

    def local_lookup(self, identifier: str) -> Type:
        for declaration in self._declarations:
            if declaration.identifier == identifier: return declaration.type
        return None

    def lookup(self, identifier: str) -> Type:
        for table in self.lexical_traversal():
            result = table.local_lookup(identifier)
            if result is not None: return result
        return None

    def local_index(self, identifier: str) -> int:
        for idx, declaration in enumerate(self._declarations):
            if declaration.identifier == identifier: return idx
        raise ValueError()

    def find(self, identifier: str) -> "LexicalSymbolTable":
        local_result = self.local_lookup(identifier)
        if local_result is not None: return self
        parent: LexicalSymbolTable = self._parent
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
                if declaration.lexical_index < lexical_bound:
                    identifiers.append(declaration.identifier)
                # Compilers for C allows "implicit declaration of function"
                #   Which means that "functions" can be used before they are declared.
                elif isinstance(declaration.type, SubroutineType):
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
        # closed_set: List[LexicalSymbolTable] = [ ]
        curr: LexicalSymbolTable = self
        while curr is not None:
            yield curr
            curr = curr.parent

class LexicalSymbolTabelBuilder():
    def __init__(
        self,
        minimum_lexical_index: int,
        maximum_lexical_index: int,
    ) -> None:
        self._root = LexicalSymbolTable(
            minimum_lexical_index,
            maximum_lexical_index,
            None, list()
        )
        self._scope_stack = [ self._root ]

    @property
    def current(self) -> LexicalSymbolTable:
        return self._scope_stack[-1]

    @property
    def depth(self) -> int:
        return len(self._scope_stack)

    def open(
        self,
        minimum_lexical_index: int,
        maximum_lexical_index: int
    ) -> "LexicalSymbolTabelBuilder":
        new_table = LexicalSymbolTable(
            minimum_lexical_index,
            maximum_lexical_index,
            self.current,
            list()
        )
        self.current.children.append(new_table)
        self._scope_stack.append(new_table)
        return self

    def enter(
        self,
        identifier: str,
        type: Type,
        lexical_index: int
    ) -> "LexicalSymbolTabelBuilder":
        self.current.enter(identifier, type, lexical_index)
        return self

    def close(self) -> "LexicalSymbolTabelBuilder":
        if len(self._scope_stack) == 1:
            raise Exception("Cannot close root symbol table as forests are not supported")
        self._scope_stack.pop()
        return self

    def build(self) -> Tree[LexicalSymbolTable]:
        return Tree(self._root)