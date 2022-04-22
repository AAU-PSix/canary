from typing import Union, List

from application import (
    InitializeSystemRequest,
    InitializeSystemUseCase,
    UnitAnalyseFileRequest,
    UnitAnalyseFileUseCase,
    CreateInitialTestCasesRequest,
    CreateInitialTestCasesUseCase,
    InfestProgramRequest,
    InfestProgramUseCase,
    RunTestRequest,
    RunTestUseCase,
    ParseTestResultRequest, 
    ParseTestResultUseCase,
    RenameRequest,
    RenameUseCase,
    RevertRequest,
    RevertUseCase, 
    GenerateMutantsRequest,
    GenerateMutantsUseCase
)
from ts import (
    Parser,
    LanguageLibrary,
)

from symbol_table import CSymbolTableFiller, CSyntax

def generate_tests(
    file: str,
    build_cmd: Union[str, List[str]],
    test_cmd: Union[str, List[str]],
    base: str = "",
    test: str = "",
    persist: bool = False,
):
    filepath: str = f'{base}/{file}'
    tmp_filepath: str = f'{base}/{file}.tmp'
    original_results_filepath: str = f'{filepath}.org.results'
    mutant_results_filepath: str = f'{filepath}.mut.results'
    test_directory: str = f'{base}/{test}'

    # Step 0: Initialize the system
    initialize_system_request = InitializeSystemRequest()
    InitializeSystemUseCase().do(initialize_system_request)

    # Step 1: Unit analysis to find FUT (Funtion Under Test)
    unit_analysis_request = UnitAnalyseFileRequest(
        filepath, LanguageLibrary.c(), "add"
    )
    unit_analysis_response = UnitAnalyseFileUseCase().do(
        unit_analysis_request
    )

    # Step 2.0: Create symbol table
    filler = CSymbolTableFiller(CSyntax())
    symbol_table = filler.fill(
        unit_analysis_response.tree
    )

    # Step 2.1: Create initial test case for FUT
    create_initial_test_case_request = CreateInitialTestCasesRequest(
        symbol_table.root,
        "add",
        f'{test_directory}',
        f'{test_directory}/CanaryCuTest.h',
    )
    CreateInitialTestCasesUseCase().do(
        create_initial_test_case_request
    )

    # Step 3: Infest the original file with canaries
    infest_program_request = InfestProgramRequest(
        Parser.c(),
        unit_analysis_response.tree,
        unit_analysis_response.unit_functions,
        filepath
    )
    InfestProgramUseCase().do(infest_program_request)

    # Step 4: Test the original program
    original_test_request = RunTestRequest(
        build_cmd, test_cmd, original_results_filepath
    )
    RunTestUseCase().do(original_test_request)

    # Step 5: Rename the original file to the temp
    rename_original_to_tmp_request = RenameRequest(
        filepath, tmp_filepath
    )
    RenameUseCase().do(rename_original_to_tmp_request)

    # Step 6: Generate the mutant
    generate_mutants_request = GenerateMutantsRequest(
        filepath, tmp_filepath
    )
    GenerateMutantsUseCase().do(generate_mutants_request)

    # Step 7: Test the mutant program
    mutant_test_request = RunTestRequest(
        build_cmd, test_cmd, mutant_results_filepath
    )
    RunTestUseCase().do(mutant_test_request)

    # Step 7.1: Parse the test results
    parse_results_request = ParseTestResultRequest(mutant_results_filepath)
    test_result = ParseTestResultUseCase().do(parse_results_request)

    # Step 8: Move the original program into the mutant
    #   If we want to persist then store the mutant another place
    if persist: 
        mut_rename_request = RenameRequest(
            filepath, f'{filepath}.mut'
        )
        tmp_rename_request = RenameRequest(
            tmp_filepath, filepath
        )
        RenameUseCase().do(mut_rename_request)
        RenameUseCase().do(tmp_rename_request)

    # Step 9: Clean up
    # Step 9.1: Remove canaries in the original file
    revert_request = RevertRequest(
        filepath, unit_analysis_response.tree.text
    )
    RevertUseCase().do(revert_request)