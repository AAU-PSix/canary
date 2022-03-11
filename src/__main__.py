import argparse

from src.Utilities.setupCommandLine import setupCommandLine
from src.Utilities.setupCommandLine import setupIOHandler




def main():
    commandLineParser = setupCommandLine()
    ioHandler = setupIOHandler(commandLineParser)

    # Do the pipeline stuff
    # TODO Create a pipeline program using a common pipeline pattern
    mutatedProgram: any = 2

    # Write the file
    ioHandler.write_file(mutatedProgram)


if __name__ == "__main__":
    main()
