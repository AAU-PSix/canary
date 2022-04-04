from abc import ABC
from typing import Callable, Dict
from ts import (
    Node,
    CNodeType,
    CField,
    CSyntax,
    Tree as TsTree
)
from .type import *
from .symbol_table import LexicalSymbolTable
from .c_type import CSymbolTable, CSymbolTableBuilder, CTypeFactory
from .tree import Tree

class SymbolTableFiller(ABC):
    def fill(self, root: Node) -> Tree[CSymbolTable]:
        pass

class CSymbolTableFiller(SymbolTableFiller):
    def __init__(self,syntax: CSyntax) -> None:
        self._syntax = syntax
        self._type_factory = CTypeFactory()
        self._visits: Dict[str, Callable[[TsTree, Node, CSymbolTableBuilder], None]] = {
            CNodeType.TRANSLATION_UNIT.value: self._visit_translation_unit,
            CNodeType.DECLARATION.value: self._visit_declaration,
            CNodeType.COMPOUND_STATEMENT.value: self._visit_compound_statement,
            CNodeType.FUNCTION_DEFINITION.value: self._visit_function_definition,
        }
        super().__init__()

    def _accept(
        self,
        tree: TsTree,
        node: Node,
        builder: LexicalSymbolTable
    ) -> None:
        if node.type in self._visits:
            self._visits[node.type](tree, node, builder)

    def _accept_siblings(
        self,
        tree: TsTree,
        node: Node,
        builder: LexicalSymbolTable
    ) -> None:
        sibling: Node = node.next_named_sibling
        while sibling is not None:
            self._accept(tree, sibling, builder)
            sibling = sibling.next_named_sibling
    
    def _accept_children(
        self,
        tree: TsTree,
        node: Node,
        builder: LexicalSymbolTable
    ) -> None:
        for child in node.named_children:
            self._accept(tree, child, builder)

    def fill(
        self,
        tree: TsTree,
        root: Node = None,
    ) -> Tree[CSymbolTable]:
        if root is None: root = tree.root_node

        builder = CSymbolTableBuilder(
            root.start_byte, root.end_byte
        )
        self._accept(
            tree, root, builder
        )
        return builder.build()

    def _visit_translation_unit(
        self,
        tree: TsTree,
        translation_unit: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        self._accept_children(tree, translation_unit, builder)

    def _visit_compound_statement(
        self,
        tree: TsTree,
        compound_statement: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        builder.open(
            compound_statement.start_byte,
            compound_statement.end_byte
        )
        self._accept_children(
            tree, compound_statement, builder
        )
        builder.close()

    def _visit_function_definition(
        self,
        tree: TsTree,
        function_definition: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        declarator_node = function_definition.child_by_field(CField.DECLARATOR)
        identifier_node = declarator_node.child_by_field(CField.DECLARATOR)
        body_node = function_definition.child_by_field(CField.BODY)
        function_identifier = tree.contents_of(identifier_node)
        function_type = self._type_factory.create_subroutine_type(
            tree, function_definition
        )

        builder.enter(
            function_identifier,
            function_type,
            function_definition.end_byte
        )
        builder.open(
            function_definition.start_byte,
            function_definition.end_byte
        )
        for parameter in function_type.parameters:
            builder.enter(
                parameter.identifier,
                parameter.type,
                parameter.lexical_index
            )
        self._accept(tree, body_node, builder)
        builder.close()

    def _visit_declaration(
        self,
        tree: TsTree,
        declaration: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        type_field = declaration.child_by_field(CField.TYPE)
        declarator = declaration.child_by_field(CField.DECLARATOR)
        declaration_identifier = declarator.child_by_field(CField.DECLARATOR)

        if type_field.type == CNodeType.PRIMITIVE_TYPE.value:
            builder.enter(
                tree.contents_of(declaration_identifier),
                PrimitiveType(type_field),
                declaration.end_byte
            )