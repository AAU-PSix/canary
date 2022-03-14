from typing import List
from ts import Parser, Tree, Node
from utilities import setupCommandLine, setupIOHandler
from unit_analyser import UnitAnalyser
from argparse import ArgumentParser

def main():
    commandLineParser: ArgumentParser = setupCommandLine()
    ioHandler = setupIOHandler(commandLineParser)
    c_parser = Parser.c()
    c_language = c_parser.language
    programtree: Tree = c_parser.parse(ioHandler.input_file_text)
    unitAnalyser: UnitAnalyser = UnitAnalyser(c_language, programtree.root_node)

    structs = unitAnalyser.get_struct_declarations()
    functions = unitAnalyser.get_function_declarations()
    languageConstructs: List[Node] = functions.__add__(structs)
    print(languageConstructs)

if __name__ == "__main__":
    main()
