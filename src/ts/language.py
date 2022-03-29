from typing import TypeVar, Generic
from tree_sitter import Language as _Language
from .query import Query
from .syntax import Syntax

TSyntax = TypeVar("TSyntax", bound=Syntax)
class Language(Generic[TSyntax]):
    def __init__(self, syntax: TSyntax, language: _Language) -> None:
        self._language = language
        self._syntax = syntax

    @property
    def syntax(self) -> TSyntax:
        return self._syntax

    @property
    def id(self) -> int:
        return self._language.language_id

    @property
    def name(self):
        return self._language.name

    def field_id_for_name(self, name: str) -> int:
        """Returns the id of a field found in 'grammer.js' as a 'field' function call

        Args:
            name (str): The name of the field, also the first parameter in the function call

        Returns:
            int: The int id of the field
        """
        return self._language.field_id_for_name(name)

    def query(self, source: str) -> Query:
        """Creates a query from the soruce for a given language

        Args:
            source (str): The query source

        Returns:
            Query: A query for the given language
        """
        return Query(self._language.query(source))