from mutator import Mutator
from ts import (
    LanguageLibrary,
    Parser,
    Tree,
)
from utilities import (
    ArgumentParser,
    setupCommandLine,
    FileHandler
)


def main():
    LanguageLibrary.build()
    commandLineParser: ArgumentParser = setupCommandLine()
    args = commandLineParser.parse_args()
    input: str = args.input
    output: str = args.output

    input_file: FileHandler = open(input, "r")
    input_contents: str = input_file.read()
    input_file.close()

    parser: Parser = Parser.c()
    tree: Tree = parser.parse(input_contents)

    mutator = Mutator(parser)
    mutated_tree: Tree = mutator.mutate(tree)

    output_file: str = open(output, "w+")
    output_file.write(mutated_tree.text)

if __name__ == "__main__":
    main()
