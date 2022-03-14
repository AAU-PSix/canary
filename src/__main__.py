import argparse
from typing import List
from src.ts.language_library import Language
from src.ts.parser import Parser
from src.ts.tree import Tree
from src.ts.node import Node
from src.unit_analyser import UnitAnalyser
from .Utilities import setupCommandLine
from .Utilities import setupIOHandler


def main():
    commandLineParser: argparse.ArgumentParser = setupCommandLine()
    ioHandler = setupIOHandler(commandLineParser)
    parser: Parser = Parser.c()
    language: Language = parser.language
    tree: Tree = parser.parse(ioHandler.input_file_text)
    unitAnalyser: UnitAnalyser = UnitAnalyser(language, tree.root_node)

    structs = unitAnalyser.get_struct_declarations()
    functions = unitAnalyser.get_function_declarations()
    languageConstructs: List[Node] = functions.__add__(structs)
    print(languageConstructs)

if __name__ == "__main__":
    main()
