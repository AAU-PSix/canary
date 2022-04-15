from argparse import ArgumentParser

from .utilities import FileHandler, CanaryIOHandler


def setupCommandLine() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "action",
        type=str,
        help="The action to do",
        default="generate",
        choices=["tests", "cfg", "mutate", "instrument"]
    )
    parser.add_argument(
        "-p", "--persist",
        help="If true mutated files and graphs will persist in 'out'",
        default=False,
        action="store_true"
    )
    parser.add_argument(
        "-l", "--log",
        help="If true the a log file is created at 'out'",
        default=False,
        action="store_true"
    )
    parser.add_argument(
        "-m", "--mutations",
        help="The amount of mutations",
        type=int,
        default=1000,
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
    parser.add_argument(
        "-o", "--out",
        type=str,
        default="./",
        help="The output directory"
    )
    parser.add_argument(
        "-bc", "--build_command",
        type=str,
        default=None,
        help="The command used to build the project"
    )
    parser.add_argument(
        "-tc", "--test_command",
        type=str,
        default=None,
        help="The command used to test the project"
    )
    return parser


def setupIOHandler(commandLineParser: ArgumentParser):
    args = commandLineParser.parse_args()
    return CanaryIOHandler(args, FileHandler())
