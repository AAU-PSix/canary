import argparse

from src.Utilities.setupCommandLine import setupCommandLine
from src.Utilities.setupCommandLine import setupIOHandler
from src.ts import LanguageLibrary, Parser
from src.unit_analysis.QueryApi import QueryApi
from src.unit_analysis.TreeConstructor import constructCTree


def main():
    commandLineParser: argparse.ArgumentParser = setupCommandLine()
    ioHandler = setupIOHandler(commandLineParser)
    tree = constructCTree(ioHandler.input_file_text)
    functions = QueryApi.findFunctionDeclarations(tree.root_node)
    structs = QueryApi.findStructDeclaration(tree.root_node)
    languageConstructs = functions.__add__(structs)


if __name__ == "__main__":
    main()
