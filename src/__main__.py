from utilities import (
    ArgumentParser,
    setupCommandLine,
)
from commands import generate

def main():
    commandLineParser: ArgumentParser = setupCommandLine()
    args = commandLineParser.parse_args()
    generate(
        args.file,
        ["make", "-C", "/input/", "build"],
        "/input/build/c_06_test",
        base=args.base,
        persist=args.persist
    )

if __name__ == "__main__":
    main()
