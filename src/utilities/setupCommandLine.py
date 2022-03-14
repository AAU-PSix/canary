from argparse import ArgumentParser

from .utilities import FileHandler, CanaryIOHandler


def setupCommandLine() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "input",
        metavar="path",
        type=str,
        help="The file to mutate."
    )
    parser.add_argument(
        "output",
        metavar="path",
        type=str,
        help="specifies the name of the output file"
    )
    return parser


def setupIOHandler(commandLineParser: ArgumentParser):
    args = commandLineParser.parse_args()
    return CanaryIOHandler(args, FileHandler())
