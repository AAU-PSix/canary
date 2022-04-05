from enum import Enum
from typing import Dict
from ts import (
    Node,
    CField,
    Tree,
    CNodeType
)
from symbol_table import (
    LexicalDeclaration,
    LexicalSymbolTabelBuilder,
    LexicalSymbolTable
)
from .type import *

class CTypeQualifier(Enum):
    CONST = "const",
    VOLATILE = "volatile",
    RESTRICT = "restrict",
    ATOMIC = "_Atomic",
    STATIC = "static"

class CType(Type):
    def __init__(
        self,
    ) -> None:
        super().__init__()

class CPrimitiveType(CType, PrimitiveType): pass

class CAggregateType(AggregateType):
    def __init__(self, type: Type) -> None:
        super().__init__(type)

class PointerType(CType):
    def __init__(self, multiple_indirection: int, type: Type) -> None:
        self._multiple_indirection = multiple_indirection
        self._type = type
        super().__init__()

    @property
    def type(self) -> Type:
        return self._type

    @property
    def multiple_indirection(self) -> int:
        return self._multiple_indirection

class CSubroutineType(CType, SubroutineType): pass

class CTypeStruct(CType, CompositeType):
    def __init__(self, identifier: str, composition: List[CompositeField]) -> None:
        super().__init__(identifier, composition)

class CUnionType(CType, CompositeType):
    def __init__(self, identifier: str, composition: List[CompositeField]) -> None:
        super().__init__(identifier, composition)

class CSymbolTable(LexicalSymbolTable["CSymbolTable"]):
    def __init__(
        self,
        minimum_lexical_index: int,
        maximum_lexical_index: int,
        parent: "LexicalSymbolTable" = None,
        children: List["LexicalSymbolTable"] = list()
    ) -> None:
        super().__init__(
            minimum_lexical_index,
            maximum_lexical_index,
            parent,
            children
        )

    def can_be_referenced(self, declaration: LexicalDeclaration, lexical_upper_bound: int) -> bool:
                # Compilers for C allows "implicit declaration of function"
                #   Which means that "functions" can be used before they are declared.
        return super().can_be_referenced(declaration, lexical_upper_bound) or \
            isinstance(declaration.type, SubroutineType)

class CTypeFactory():
    def __init__(self) -> None:
        self._declaration_factory = CDeclaratorFactory()
        self._primitives: Dict[str, PrimitiveType] = {
            "int": PrimitiveType("int"),
            "double": PrimitiveType("double"),
            "void": PrimitiveType("void")
        }

    def create_type_for(
        self,
        tree: Tree,
        node: Node
    ) -> Type:
        if node.is_type(CNodeType.PRIMITIVE_TYPE):
            return self.create_primitive_type(tree, node)

    def create_specifier_name(
        self,
        tree: Tree,
        type_definition: Node
    ) -> str:
        name_node = type_definition.child_by_field(CField.NAME)
        name_contents = tree.contents_of(name_node)
        if type_definition.is_type(CNodeType.STRUCT_SPECIFIER): return f'struct {name_contents}'
        if type_definition.is_type(CNodeType.UNION_SPECIFIER): return f'union {name_contents}'
        if type_definition.is_type(CNodeType.ENUM_SPECIFIER): return f'enum {name_contents}'
        return tree.contents_of(name_node)

    def create_primitive_type(
        self,
        tree: Tree,
        node: Node
    ) -> PrimitiveType:
        return self._primitives[tree.contents_of(node)]

    def create_composite_type(
        self,
        tree: Tree,
        type_node: Node
    ) -> CompositeType:
        body = type_node.child_by_field(CField.BODY)
        fields: List[CompositeField] = list()
        for field in body.named_children:
            field_type_node = field.child_by_field(CField.TYPE)
            field_type = self.create_type_for(tree, field_type_node)
            field_identifier_node = field.child_by_field(
                CField.DECLARATOR
            )
            field_identifier = tree.contents_of(field_identifier_node)
            fields.append(CompositeField(field_identifier, field_type))
        return CompositeType(fields)

    def create_enum_type(
        self,
        tree: Tree,
        enum_type: Node
    ) -> EnumType:
        enumerators: List[EnumField] = list()
        body = enum_type.child_by_field(CField.BODY)
        for enumerator in body.named_children:
            value_node = enumerator.child_by_field(CField.VALUE)
            # An "enumerator" does not require a value
            if value_node is not None:
                enumerator_value = int(tree.contents_of(value_node))
            else: enumerator_value = None

            identifier_node = enumerator.child_by_field(CField.NAME)
            enumerator_identifier = tree.contents_of(identifier_node)
            field = EnumField(
                enumerator_identifier,
                enumerator_value,
            )
            enumerators.append(field)
        return EnumType(enumerators)

    def create_subroutine_type(
        self,
        tree: Tree,
        function_definition: Node
    ) -> SubroutineType[LexicalDeclaration]:
        return_type_node = function_definition.child_by_field(CField.TYPE)
        declarator_node = function_definition.child_by_field(CField.DECLARATOR)
        parameters_node = declarator_node.child_by_field(CField.PARAMETERS)
        return_type = self.create_primitive_type(tree, return_type_node)

        parameters: List[LexicalDeclaration] = [ ]
        for parameter_declaration_node in parameters_node.named_children:
            parameter_declaration = self._declaration_factory.create_parameter_declaration(
                tree, self, parameter_declaration_node
            )
            parameters.append(parameter_declaration)
        function_type = SubroutineType(return_type, parameters)

        return function_type

class CDeclaratorFactory():
    def __init__(self) -> None: pass

    def create_parameter_declaration(
        self,
        tree: Tree,
        type_factory: CTypeFactory,
        parameter_declaration_node: Node
    ) -> CDeclaration:
        declaration_storage_class_specifier_nodes = parameter_declaration_node.get_children_of_type(
            CNodeType.STORAGE_CLASS_SPECIFIERS
        )
        declaration_storage_class_specifiers = [
            tree.contents_of(node) for node in declaration_storage_class_specifier_nodes
        ]

        declaration_type_qualifier_nodes = parameter_declaration_node.get_children_of_type(
            CNodeType.TYPE_QUALIFIER
        )
        declaration_type_qualifiers = [
            tree.contents_of(node) for node in declaration_type_qualifier_nodes
        ]

        type_node = parameter_declaration_node.child_by_field(CField.TYPE)
        type = type_factory.create_type_for(tree, type_node)
        declarator = parameter_declaration_node.child_by_field(CField.DECLARATOR)
        return self.create_declaration(
            type, tree, declarator,
            declaration_storage_class_specifiers,
            declaration_type_qualifiers
        )

    def create_declaration(
        self,
        type: Type,
        tree: Tree,
        declarator: Node,
        declaration_storage_class_specifiers: List[str],
        declaration_type_qualifiers: List[str],
    ) -> CDeclaration:
        # Case 1: The declarator is just the identifier ("int a;")
        if declarator.is_type(CNodeType.IDENTIFIER):
            return CDeclaration(
                tree.contents_of(declarator),
                type,
                declarator.end_byte,
                declaration_storage_class_specifiers,
                declaration_type_qualifiers
            )
        # Case 2: The declarator has an initilization ("int a=0;")
        elif declarator.is_type(CNodeType.INIT_DECLARATOR):
            # The "declarator" of the "declarator" is the identifier
            identifier = declarator.child_by_field(CField.DECLARATOR)
            return CDeclaration(
                tree.contents_of(identifier),
                type,
                declarator.end_byte,
                declaration_storage_class_specifiers,
                declaration_type_qualifiers
            )
        # Case 3: It is an array declarator ("int a[]")
        elif declarator.is_type(CNodeType.ARRAY_DECLARATOR):
            # The "declarator" of the "declarator" is the identifier
            identifier = declarator.child_by_field(CField.DECLARATOR)
            return CDeclaration(
                tree.contents_of(identifier),
                CAggregateType(type),
                declarator.end_byte,
                declaration_storage_class_specifiers,
                declaration_type_qualifiers
            )
        # Case 4: n-Pointers (int *****a, *a)
        elif declarator.is_type(CNodeType.POINTER_DECLARATOR):
            pointer_node = declarator
            multiple_indirection: int = 0
            while pointer_node.is_type(CNodeType.POINTER_DECLARATOR):
                multiple_indirection += 1
                pointer_node = pointer_node.first_named_child
            identifier = pointer_node

            pointer = PointerType(multiple_indirection, type)
            return CDeclaration(
                tree.contents_of(identifier),
                pointer,
                declarator.end_byte,
                declaration_storage_class_specifiers,
                declaration_type_qualifiers
            )

class CSymbolTableBuilder(LexicalSymbolTabelBuilder[CSymbolTable]):
    def __init__(self, minimum_lexical_index: int, maximum_lexical_index: int) -> None:
        super().__init__(minimum_lexical_index, maximum_lexical_index)

    def _create(
        self,
        minimum_lexical_index: int,
        maximum_lexical_index: int,
        parent: CSymbolTable = None,
        children: List[CSymbolTable] = list()
    ) -> CSymbolTable:
        return CSymbolTable(
            minimum_lexical_index,
            maximum_lexical_index,
            parent,
            children
        )