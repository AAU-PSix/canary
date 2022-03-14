from tree_sitter import Language as _Language
from query import Query
from syntax import Syntax


class Language:
    def __init__(self, syntax: Syntax, language: _Language) -> None:
        self._language = language
        self._syntax = syntax

    @property
    def syntax(self) -> Syntax:
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


class LanguageLibrary:
    @staticmethod
    def vendor_path() -> str:
        return './vendor'

    @staticmethod
    def build_path() -> str:
        return './build'

    @staticmethod
    def build_file() -> str:
        return 'my-languages.so'

    @staticmethod
    def full_build_path() -> str:
        return f'{LanguageLibrary.build_path()}/{LanguageLibrary.build_file()}'

    @staticmethod
    def build() -> None:
        _Language.build_library(
            LanguageLibrary.full_build_path(),
            [
                f'{LanguageLibrary.vendor_path()}/tree-sitter-c',
                f'{LanguageLibrary.vendor_path()}/tree-sitter-cpp',
                f'{LanguageLibrary.vendor_path()}/tree-sitter-go',
                f'{LanguageLibrary.vendor_path()}/tree-sitter-javascript',
                f'{LanguageLibrary.vendor_path()}/tree-sitter-python',
                f'{LanguageLibrary.vendor_path()}/tree-sitter-rust',
            ]
        )

    @staticmethod
    def c() -> Language:
        return Language(
            Syntax.c(),
            _Language(LanguageLibrary.full_build_path(), 'c')
        )

    @staticmethod
    def cpp() -> Language:
        return Language(
            None,
            _Language(LanguageLibrary.full_build_path(), 'cpp')
        )

    @staticmethod
    def go() -> Language:
        return Language(
            None,
            _Language(LanguageLibrary.full_build_path(), 'go')
        )

    @staticmethod
    def js() -> Language:
        return Language(
            None,
            _Language(LanguageLibrary.full_build_path(), 'javascript')
        )

    @staticmethod
    def python() -> Language:
        return Language(
            None,
            _Language(LanguageLibrary.full_build_path(), 'python')
        )

    @staticmethod
    def rust() -> Language:
        return Language(
            None,
            _Language(LanguageLibrary.full_build_path(), 'rust')
        )