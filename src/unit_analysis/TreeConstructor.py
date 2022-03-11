from src.ts import LanguageLibrary, Parser, Tree


def constructCTree(program : str) -> Tree:
    LanguageLibrary.build()
    language = LanguageLibrary.c()
    parser = Parser.create_with_language(language)
    return parser.parse(program)