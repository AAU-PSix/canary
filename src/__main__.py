import argparse
from typing import List
from ts import *
from utilities import *


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
