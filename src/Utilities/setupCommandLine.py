import argparse

from src.Utilities.Utilities import FileHandler, CanaryIOHandler

def setupCommandLine() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--o", "--output", help="specifies the name of the output file", action="store_true")
    parser.add_argument("inputfile", type=str, help="The file to mutate.")
    parser.add_argument("outputfile", type=str, help="Location of mutated program")
    return parser


def setupIOHandler(commandLineParser: argparse.ArgumentParser):
    args = commandLineParser.parse_args()

    return CanaryIOHandler(args, FileHandler())