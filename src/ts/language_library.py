from tree_sitter import Language as _Language
from .c_syntax import CSyntax
from .language import Language

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
    def c() -> Language[CSyntax]:
        return Language[CSyntax](
            CSyntax(),
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