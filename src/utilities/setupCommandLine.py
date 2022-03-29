from argparse import ArgumentParser

from .utilities import FileHandler, CanaryIOHandler


def setupCommandLine() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "action",
        type=str,
        help="The action to do",
        default="generate",
        choices=["generate", "mutate", "canaries"]
    )
    parser.add_argument(
        "-p", "--persist",
        help="If true the mutants are not deleted",
        default=False,
        action="store_true"
    )
    parser.add_argument(
        "-b", "--base",
        type=str,
        help="The base directory",
        default=""
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="The file to target"
    )
    parser.add_argument(
        "-t", "--test",
        type=str,
        help="The directory to the tests"
    )
    parser.add_argument(
        "-u", "--unit",
        type=str,
        help="The unit to test"
    )
    return parser


def setupIOHandler(commandLineParser: ArgumentParser):
    args = commandLineParser.parse_args()
    return CanaryIOHandler(args, FileHandler())
