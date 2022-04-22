from argparse import ArgumentParser
from ast import parse

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
        "-f", "--file",
        type=str,
        help="The file to target"
    )
    parser.add_argument(
        "-u", "--unit",
        type=str,
        default=None,
        help="The unit to test"
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
    parser.add_argument(
        "-o", "--out",
        type=str,
        default="./",
        help="The output directory"
    )
    parser.add_argument(
        "-b", "--base",
        type=str,
        help="The base directory",
        default=""
    )
    parser.add_argument(
        "-tb", "--testing_backend",
        type=str,
        help="The action to do",
        default="generate",
        choices=["ffs_gnu_assert", "cutest"]
    )
    parser.add_argument(
        "-ps", "--placement_strategy",
        type=str,
        help="The mutation placement strategy",
        default="randomly",
        choices=["randomly", "pathbased"]
    )
    parser.add_argument(
        "-ms", "--mutation_strategy",
        type=str,
        help="The mutation placement strategy",
        choices=["obom"]
    )
    parser.add_argument(
        "-uwl", "--unit_whitelist",
        type=str,
        help="A space sperated list of units to whitelist",
        default=""
    )
    parser.add_argument(
        "-ubl", "--unit_blacklist",
        type=str,
        help="A space sperated list of units to blacklist",
        default=""
    )
    return parser

def setupIOHandler(commandLineParser: ArgumentParser):
    args = commandLineParser.parse_args()
    return CanaryIOHandler(args, FileHandler())
