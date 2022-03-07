from tree_sitter import Language as _Language

from src.tree_sitter_py.query import Query

class Language:
    def __init__(self, language: _Language) -> None:
        self._language = language

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
    def build() -> str:
        _Language.build_library(
            LanguageLibrary.full_build_path(),
            [ f'{LanguageLibrary.vendor_path()}/tree-sitter-javascript' ]
        )

    @staticmethod
    def js() -> Language:
        return Language(
            _Language(LanguageLibrary.full_build_path(), 'javascript')
        )