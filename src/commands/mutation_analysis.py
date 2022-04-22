from application import (
    InitializeSystemRequest,
    InitializeSystemUseCase,
    UnitAnalyseFileRequest,
    UnitAnalyseFileUseCase,
    RunTestRequest,
    RunTestUseCase,
    InfestProgramRequest,
    InfestProgramUseCase,
    ParseTestResultRequest,
    ParseTestResultUseCase,
    UnitAnalyseTreeRequest,
    UnitAnalyseTreeUseCase,
    MutateAlongAllTracesRequest,
    MutateAlongAllTracesUseCase,
    MutateRandomlyRequest,
    MutateRandomlyUseCase,
)
from cfa import CCFAFactory
from decorators import LocationDecorator
from mutator import ObomStrategy
from test_results_parsing import (
    FfsGnuAssertResultsParser,
    CuTestResultsParser
)
from ts import (
    Parser,
    LanguageLibrary,
)

def mutation_analysis(
    file: str,
    unit: str,
    build_command: str,
    test_command: str,
    out: str = "",
    base: str = "",
    testing_backend: str = "ffs_gnu_assert",
    placement_strategy: str = "randomly",
    mutation_strategy: str = "obom",
) -> None:
    # Step 0: Initialize the system
    initialize_system_request = InitializeSystemRequest()
    InitializeSystemUseCase().do(initialize_system_request)

    # Step 1: Unit analysis
    unit_analysis_of_file_request = UnitAnalyseFileRequest(
        f'{base}/{file}', Parser.c(), unit
    )
    unit_analysis_of_file_response = UnitAnalyseFileUseCase().do(
        unit_analysis_of_file_request
    )

    # Step 2: Instrument the mutable version
    instrumentation_request = InfestProgramRequest(
        Parser.c(),
        unit_analysis_of_file_response.tree,
        unit_analysis_of_file_response.unit_function,
        unit_analysis_of_file_request.filepath
    )
    instrumentation_response = InfestProgramUseCase().do(
        instrumentation_request
    )

    # Step 3: Instrumented tree unit analysis
    instrumented_unit_analysis_of_file_request = UnitAnalyseFileRequest(
        unit_analysis_of_file_request.filepath, Parser.c(), unit
    )
    instrumented_unit_analysis_of_file_response = UnitAnalyseFileUseCase().do(
        instrumented_unit_analysis_of_file_request
    )

    # Step 4: Get the localised CFG
    unit_analysis_of_tree_request = UnitAnalyseTreeRequest(
        instrumented_unit_analysis_of_file_response.tree,
        LanguageLibrary.c(),
        unit_analysis_of_file_request.unit
    )
    unit_analysis_of_tree_response = UnitAnalyseTreeUseCase().do(
        unit_analysis_of_tree_request
    )
    instrumented_cfg = CCFAFactory(instrumentation_response.instrumented_tree).create(
        unit_analysis_of_tree_response.unit_function
    )
    localised_cfg = LocationDecorator(instrumentation_response.instrumented_tree).decorate(
        instrumented_cfg
    )
    localised_cfg.draw(
        instrumentation_response.instrumented_tree,
        "instrumented_cfg"
    ).save(directory=f"{base}/{out}")

    # Step 5: Run tests on original program
    original_test_request = RunTestRequest(
        build_command, test_command, f'{base}/{out}/original_test_results.txt'
    )
    RunTestUseCase().do(original_test_request)

    # Step 6: Parse test results
    if testing_backend == "ffs_gnu_assert":
        test_results_parser = FfsGnuAssertResultsParser()
    elif testing_backend == "cutest":
        test_results_parser = CuTestResultsParser()
    parse_test_results_request = ParseTestResultRequest(
        original_test_request.out,
        test_results_parser
    )
    parse_test_results_response = ParseTestResultUseCase().do(
        parse_test_results_request
    )
    
    # Step 7: Create mutation strategy
    if mutation_strategy == "obom":
        applied_mutation_strategy = ObomStrategy(
            instrumentation_request.parser
        )

    if placement_strategy == "randomly":
        # Step 7: Mutate 'randomly'
        randomly_mutate_request = MutateRandomlyRequest(
            instrumented_unit_analysis_of_file_response.unit_function,
            instrumentation_response.instrumented_tree,
            instrumentation_request.parser,
            applied_mutation_strategy,
            build_command,
            test_command,
            test_results_parser,
            unit_analysis_of_file_request.filepath,
            out,
            base,
        )
        MutateRandomlyUseCase().do(
            randomly_mutate_request
        )
    elif placement_strategy == "pathbased":
        # Step 7: Get individual unit sequences
        unit_traces = localised_cfg.split_on_finals(
            parse_test_results_response.test_results.trace
        )

        # Step 8: Mutate 'pathbased'
        mutate_along_trace_request = MutateAlongAllTracesRequest(
            instrumentation_response.instrumented_tree,
            unit_traces,
            localised_cfg,
            applied_mutation_strategy,
            instrumentation_request.parser,
            test_results_parser,
            build_command,
            test_command,
            base,
            out,
            unit_analysis_of_file_request.filepath,
        )
        MutateAlongAllTracesUseCase().do(
            mutate_along_trace_request
        )

    # Step 6: Revert to the original program after mutation
    file = open(unit_analysis_of_file_request.filepath, "w+")
    file.write(unit_analysis_of_file_response.tree.text)
    file.close()
