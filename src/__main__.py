import argparse
from typing import List
from src.ts.language_library import Language
from src.ts.syntax import Syntax
from src.ts.parser import Parser
from src.ts.tree import Tree
from src.ts.node import Node
from utilities.setupCommandLine import setupCommandLine
from utilities.setupCommandLine import setupIOHandler


def main():
    commandLineParser: argparse.ArgumentParser = setupCommandLine()
    ioHandler = setupIOHandler(commandLineParser)
    parser: Parser = Parser.c()
    language: Language = parser.language
    syntax: Syntax = language.syntax
    tree: Tree = parser.parse(ioHandler.input_file_text)
    functions: List[Node] = language.query(
        syntax.query_function_declaration
    ).captures(tree.root_node).nodes(syntax.get_function_declaration)
    structs: List[Node] = language.query(
        syntax.query_struct_declaration
    ).captures(tree.root_node).nodes(syntax.get_struct_declaration)
    languageConstructs: List[Node] = functions.__add__(structs)
    print(languageConstructs)


if __name__ == "__main__":
    main()
