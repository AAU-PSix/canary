from utilities import (
    ArgumentParser,
    setupCommandLine,
)
from commands import (
    generate_tests,
    create_cfg,
    mutation_analysis
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
        create_cfg(
            args.file,
            args.unit,
            args.out,
            args.base
        )
    elif args.action == "mutate":
        mutation_analysis(
            args.file,
            args.unit,
            args.out,
            args.persist,
            args.mutations,
            args.log,
            args.build_command,
            args.test_command,
            args.base
        )

if __name__ == "__main__":
    main()
