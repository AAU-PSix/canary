from utilities import (
    ArgumentParser,
    setupCommandLine,
)
from commands import (
    generate_tests,
    create_cfg
)

def main():
    commandLineParser: ArgumentParser = setupCommandLine()
    args = commandLineParser.parse_args()
    if args.action == "tests":
        generate_tests(
            args.file,
            ["make", "-C", "/input/", "build"],
            "/input/build/c_06_test",
            base=args.base,
            persist=args.persist,
            test=args.test
        )
    elif args.action == "cfg":
        create_cfg.create_cfg_from_file(
            args.file,
            args.unit,
            args.out,
            args.base
        )

if __name__ == "__main__":
    main()
