from random import choice
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
from mutator import Mutator
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
    unit_traces = parse_test_results_response.test_results.trace.split_on_finals(
        localised_cfg
    )

    # Step 8: Find candidate nodes
    trace = unit_traces[0]
    candidates = [ *trace.follow(None, localised_cfg) ]
    tweet_handler = TweetHandler(instrumentation_response.instrumented_tree)
    candidates = list(filter(lambda x: not tweet_handler.is_location_tweet(x.node), candidates))
    candidates = list(filter(lambda x: x.node.is_either_type([
        CNodeType.EXPRESSION_STATEMENT, CNodeType.RETURN_STATEMENT,
        CNodeType.PARENTHESIZED_EXPRESSION, CNodeType.LABELED_STATEMENT
    ]), candidates))

    trace_str = ""
    for location in unit_traces[0].sequence:
        trace_str += f'{location.id} '
    print(trace_str)
    dot = localised_cfg.draw(instrumentation_response.instrumented_tree, "localised_cfg")
    dot.save(directory=base)
    
    # Step 9: Run mutation analysis
    mutator = Mutator(Parser.c())
    for _ in range(1):
        # Should be the "a + b" for c_06
        candidate = candidates[-2]
        print(
            instrumentation_response.instrumented_tree.contents_of(candidate.node)
        )
        mutated_tree = mutator.mutate(
            instrumentation_response.instrumented_tree,
            candidate.node
        )
        print(mutated_tree.text)