from typing import Callable, Dict
from ts import (
    Node,
    CNodeType,
    CField,
    CSyntax,
    Tree as Tree
)
from .c_symbol_table import CSymbolTable
from .c_symbol_table_builder import CSymbolTableBuilder
from .c_type_factory import CDeclaratorFactory, CTypeFactory
from ..lexical_symbol_table_builder import LexicalSymbolTable
from ..symbol_table_filler import SymbolTableFiller
from ..tree import Tree

class CSymbolTableFiller(SymbolTableFiller):
    def __init__(self,syntax: CSyntax) -> None:
        self._c_declarator_factory = CDeclaratorFactory()
        self._syntax = syntax
        self._type_factory = CTypeFactory()
        self._visits: Dict[str, Callable[[Tree, Node, CSymbolTableBuilder], None]] = {
            CNodeType.TRANSLATION_UNIT.value: self._visit_translation_unit,
            CNodeType.DECLARATION.value: self._visit_declaration,
            CNodeType.COMPOUND_STATEMENT.value: self._visit_compound_statement,
            CNodeType.FUNCTION_DEFINITION.value: self._visit_function_definition,
            CNodeType.IF_STATEMENT.value: self._visit_if_statement,
            CNodeType.WHILE_STATEMENT.value: self._visit_while_statement,
            CNodeType.DO_STATEMENT.value: self._visit_do_statement,
            CNodeType.FOR_STATEMENT.value: self._visit_for_statement,
            CNodeType.SWITCH_STATEMENT.value: self._visit_switch_statement,
            CNodeType.TYPE_DEFINITION.value: self._visit_type_definition,
            CNodeType.STRUCT_SPECIFIER.value: self._visit_struct_specifier,
            CNodeType.UNION_SPECIFIER.value: self._visit_union_specifier,
            CNodeType.ENUM_SPECIFIER.value: self._visit_enum_specifier,
            CNodeType.PREPROC_IFDEF.value: self._visit_preproc_ifdef,
            CNodeType.PREPROC_DEF.value: self._visit_preproc_def,
        }
        super().__init__()

    def _accept(
        self,
        tree: Tree,
        node: Node,
        builder: LexicalSymbolTable
    ) -> None:
        if node.type in self._visits:
            self._visits[node.type](tree, node, builder)

    def _accept_siblings(
        self,
        tree: Tree,
        node: Node,
        builder: LexicalSymbolTable
    ) -> None:
        sibling: Node = node.next_named_sibling
        while sibling is not None:
            self._accept(tree, sibling, builder)
            sibling = sibling.next_named_sibling
    
    def _accept_children(
        self,
        tree: Tree,
        node: Node,
        builder: LexicalSymbolTable
    ) -> None:
        for child in node.named_children:
            self._accept(tree, child, builder)

    def fill(
        self,
        tree: Tree,
        root: Node = None,
    ) -> Tree[CSymbolTable]:
        if root is None: root = tree.root

        builder = CSymbolTableBuilder(
            root.start_byte, root.end_byte
        )
        self._accept(
            tree, root, builder
        )
        return builder.build()

    def _visit_preproc_ifdef(
        self,
        tree: Tree,
        preproc_ifdef: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        self._accept_children(
            tree, preproc_ifdef, builder
        )

    def _visit_preproc_def(
        self,
        tree: Tree,
        preproc_def: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        self._accept_children(
            tree, preproc_def, builder
        )

    def _visit_translation_unit(
        self,
        tree: Tree,
        translation_unit: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        self._accept_children(tree, translation_unit, builder)

    def _visit_if_statement(
        self,
        tree: Tree,
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

        alternative = if_statement.child_by_field(CField.ALTERNATIVE)
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
        tree: Tree,
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
        tree: Tree,
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
        tree: Tree,
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
        tree: Tree,
        for_statement: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        builder.open_for(for_statement)
        initialization = for_statement.child_by_field(CField.INITIALIZER)
        if initialization is not None:
            self._accept(tree, initialization, builder)
        body = self._syntax.get_for_loop_body(for_statement)
        is_compound = body.is_type(CNodeType.COMPOUND_STATEMENT)
        if not is_compound: builder.open_for(body)
        self._accept(tree, body, builder)
        if not is_compound: builder.close()
        builder.close()

    def _visit_compound_statement(
        self,
        tree: Tree,
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
        tree: Tree,
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

    def _visit_struct_specifier(
        self,
        tree: Tree,
        struct_specifier: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        builder.enter(
            self._type_factory.create_specifier_name(tree, struct_specifier),
            self._type_factory.create_composite_type(tree, struct_specifier),
            struct_specifier.end_byte,
        )

    def _visit_union_specifier(
        self,
        tree: Tree,
        union_specifier: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        builder.enter(
            self._type_factory.create_specifier_name(tree, union_specifier),
            self._type_factory.create_composite_type(tree, union_specifier),
            union_specifier.end_byte,
        )

    def _visit_enum_specifier(
        self,
        tree: Tree,
        enum_specifier: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        builder.enter(
            self._type_factory.create_specifier_name(tree, enum_specifier),
            self._type_factory.create_enum_type(tree, enum_specifier),
            enum_specifier.end_byte
        )

    def _visit_type_definition(
        self,
        tree: Tree,
        type_definition: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        type_node = type_definition.child_by_field(CField.TYPE)
        if (type_node.is_type(CNodeType.STRUCT_SPECIFIER) or \
            type_node.is_type(CNodeType.UNION_SPECIFIER) or \
            type_node.is_type(CNodeType.ENUM_SPECIFIER)) and \
            type_node.child_by_field(CField.BODY) is not None:
            self._accept(tree, type_node, builder)

        type_identifier = self._type_factory.create_specifier_name(tree, type_node)
        reference_declaration = builder.current.lookup(type_identifier)
        declarator_node = type_definition.child_by_field(CField.DECLARATOR)
        declarator_identifier = tree.contents_of(declarator_node)
        builder.enter(
            declarator_identifier,
            reference_declaration.type,
            type_definition.end_byte,
            reference_declaration.storage_class_specifiers,
            reference_declaration.type_qualifiers
        )

    def _visit_declaration(
        self,
        tree: Tree,
        declaration: Node,
        builder: CSymbolTableBuilder
    ) -> None:
        declaration_storage_class_specifier_nodes = declaration.get_children_of_type(
            CNodeType.STORAGE_CLASS_SPECIFIERS
        )
        declaration_storage_class_specifiers = [
            tree.contents_of(node) for node in declaration_storage_class_specifier_nodes
        ]

        declaration_type_qualifier_nodes = declaration.get_children_of_type(
            CNodeType.TYPE_QUALIFIER
        )
        declaration_type_qualifiers = [
            tree.contents_of(node) for node in declaration_type_qualifier_nodes
        ]

        type_field = declaration.child_by_field(CField.TYPE)
        type = self._type_factory.create_type_for(tree, type_field)
        declarator_node = type_field.next_named_sibling
        while declarator_node is not None:
            c_declaration = self._c_declarator_factory.create_declaration(
                type, tree, declarator_node,
                declaration_storage_class_specifiers,
                declaration_type_qualifiers
            )
            builder.enter_declaration(c_declaration)
            declarator_node = declarator_node.next_named_sibling