from ts import LanguageLibrary, Parser, Language, Tree, Node
from typing import List
from utilities import setupCommandLine
from unit_analyser import UnitAnalyser
from argparse import ArgumentParser


def main():
    LanguageLibrary.build()
    commandLineParser: ArgumentParser = setupCommandLine()
    args = commandLineParser.parse_args()

    print(args.input)
    print(args.output)



    # ioHandler = setupIOHandler(commandLineParser)
    parser: Parser = Parser.c()
    language: Language = parser.language
    tree: Tree = parser.parse("asd+=1;")
    unitAnalyser: UnitAnalyser = UnitAnalyser(language, tree.root_node)
    print(tree.text)

    structs = unitAnalyser.get_struct_declarations()
    functions = unitAnalyser.get_function_declarations()
    languageConstructs: List[Node] = functions.__add__(structs)
    print(languageConstructs)

if __name__ == "__main__":
    main()
