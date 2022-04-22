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
    if args.action == "cfg":
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
            args.build_command,
            args.test_command,
            args.out,
            args.base,
            args.testing_backend,
            args.placement_strategy,
            args.mutation_strategy,
            args.unit_whitelist,
            args.unit_blacklist,
        )

if __name__ == "__main__":
    main()
