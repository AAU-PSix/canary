from application import (
    InitializeSystemRequest,
    InitializeSystemUseCase,
    UnitAnalyseFileRequest,
    UnitAnalyseFileUseCase,
    RunTestRequest,
    RunTestUseCase,
    InfestProgramRequest,
    InfestProgramUseCase,
    RevertRequest,
    RevertUseCase,
    ParseTestResultRequest,
    ParseTestResultUseCase,
    UnitAnalyseTreeRequest,
    UnitAnalyseTreeUseCase
)
from mutator import Mutator, ObomStrategy
from cfa import CCFAFactory
from decorators import LocationDecorator, TweetHandler
from ts import (
    Parser,
    LanguageLibrary,
    CNodeType,
)

def mutation_analysis(
    file: str,
    unit: str,
    out: str,
    persist: bool,
    mutations: int,
    log: bool,
    build_command: str,
    test_command: str,
    base: str = "",
) -> None:
    print(persist)
    print(mutations)
    print(log)

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

    # Step 3: Get the localised CFG
    unit_analysis_of_tree_request = UnitAnalyseTreeRequest(
        instrumentation_response.instrumented_tree,
        LanguageLibrary.c(),
        unit_analysis_of_file_request.unit
    )
    unit_analysis_of_tree_response = UnitAnalyseTreeUseCase().do(
        unit_analysis_of_tree_request
    )
    instrumented_cfa = CCFAFactory(instrumentation_response.instrumented_tree).create(
        unit_analysis_of_tree_response.unit_function
    )
    localised_cfg = LocationDecorator(instrumentation_response.instrumented_tree).decorate(
        instrumented_cfa
    )

    # Step 4: Run tests on original program
    original_test_request = RunTestRequest(
        build_command, test_command, f'{base}/{out}/original_test_results.txt'
    )
    RunTestUseCase().do(original_test_request)

    # Step 5: Revert the file contents to before unit analysis
    revert_request = RevertRequest(
        unit_analysis_of_file_request.filepath,
        unit_analysis_of_file_response.tree.text
    )
    RevertUseCase().do(revert_request)

    # Step 6: Parse test results
    parse_test_results_request = ParseTestResultRequest(
        original_test_request.test_stdout
    )
    parse_test_results_response = ParseTestResultUseCase().do(
        parse_test_results_request
    )

    # Step 7: Get individual unit sequences
    unit_traces = localised_cfg.split_on_finals(
        parse_test_results_response.test_results.trace
    )

    # Step 8: Mutate along all unique traces
    for trace in unit_traces:
        print(trace)
        trace_str = ""
        for location in trace.sequence:
            trace_str += f'{location.id} '
        print(trace_str)
        dot = localised_cfg.draw(instrumentation_response.instrumented_tree, f"localised_cfg_{trace_str}")
        dot.save(directory=base)

        tweet_handler = TweetHandler(instrumentation_response.instrumented_tree)
        trace_nodes = list(
            filter(
                lambda x: not tweet_handler.is_location_tweet(x.node),
                [ *localised_cfg.follow(None, trace) ]
            )
        )

        for trace_node in trace_nodes:
            mutation_strategy = ObomStrategy(Parser.c())
            candidates = mutation_strategy.capture(trace_node.node)

            for candidate in candidates:
                mutated_tree = mutation_strategy.mutate(
                    instrumentation_response.instrumented_tree,
                    candidate
                )