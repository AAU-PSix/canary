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
            CNodeType.IF_STATEMENT.value: self._visit_if_statement,
            CNodeType.WHILE_STATEMENT.value: self._visit_while_statement,
            CNodeType.DO_STATEMENT.value: self._visit_do_statement,
            CNodeType.FOR_STATEMENT.value: self._visit_for_statement,
            CNodeType.SWITCH_STATEMENT.value: self._visit_switch_statement,
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

    def _visit_if_statement(
        self,
        tree: TsTree,
        if_statement: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        consequence = if_statement.child_by_field(CField.CONSEQUENCE)
        if consequence is not None:
            is_compound = consequence.is_type(CNodeType.COMPOUND_STATEMENT)
            if not is_compound: builder.open_for(consequence)
            self._accept(
                tree,
                consequence,
                builder
            )
            if not is_compound: builder.close()

        alternative = if_statement.child_by_field_name(CField.ALTERNATIVE)
        if alternative is not None:
            is_compound = alternative.is_type(CNodeType.COMPOUND_STATEMENT)
            if not is_compound: builder.open_for(alternative)
            self._accept(
                tree,
                alternative,
                builder
            )
            if not is_compound: builder.close()

    def _visit_while_statement(
        self,
        tree: TsTree,
        while_statement: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        body = while_statement.child_by_field(CField.BODY)
        is_compound = body.is_type(CNodeType.COMPOUND_STATEMENT)
        if not is_compound: builder.open_for(body)
        self._accept(tree, body, builder)
        if not is_compound: builder.close()

    def _visit_do_statement(
        self,
        tree: TsTree,
        do_statement: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        body = do_statement.child_by_field(CField.BODY)
        is_compound = body.is_type(CNodeType.COMPOUND_STATEMENT)
        if not is_compound: builder.open_for(body)
        self._accept(tree, body, builder)
        if not is_compound: builder.close()

    def _visit_switch_statement(
        self,
        tree: TsTree,
        switch_statement: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        # It is not possible for C programs to have
        #   declaration immediately after a label
        #   for this reason a declaration cannot be an
        #   immediate child of a case-label. But we do
        #   however parse it correctly, even though neither
        #   C++ allows this code construction (Funny enough
        #   because they violate scoping rules).
        body = switch_statement.child_by_field(CField.BODY)
        is_compound = body.is_type(CNodeType.COMPOUND_STATEMENT)
        if not is_compound: builder.open_for(body)
        self._accept(tree, body, builder)
        if not is_compound: builder.close()

    def _visit_for_statement(
        self,
        tree: TsTree,
        for_statement: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        builder.open(for_statement)
        initialization = for_statement.child_by_field(CField.INITIALIZER)
        if initialization is not None:
            self._accept(initialization)
        body = self._syntax.get_for_loop_body(for_statement)
        is_compound = body.is_type(CNodeType.COMPOUND_STATEMENT)
        if not is_compound: builder.open_for(body)
        self._accept(tree, body, builder)
        if not is_compound: builder.close()
        builder.close()

    def _visit_compound_statement(
        self,
        tree: TsTree,
        compound_statement: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        builder.open_for(compound_statement)
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