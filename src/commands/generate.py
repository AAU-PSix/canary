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
)

from mutator import Mutator
from ts import (
    Parser,
    Tree,
)
from utilities import (
    FileHandler
)
import subprocess
import os

def generate(
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
        filepath, Parser.c(), "add"
    )
    unit_analysis_response = UnitAnalyseFileUseCase().do(
        unit_analysis_request
    )

    # Step 2: Create initial test case for FUT
    create_initial_test_case_request = CreateInitialTestCasesRequest(
        unit_analysis_response.tree,
        unit_analysis_response.unit_function,
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
        unit_analysis_response.unit_function,
        filepath
    )
    infest_program_response = InfestProgramUseCase().do(
        infest_program_request
    )

    # Step 4: Test the original program
    original_results_file: str = open(original_results_filepath, 'w')
    subprocess.run(build_cmd)
    subprocess.run(test_cmd, stdout=original_results_file)
    original_results_file.close()

    # Step 5: Rename the original file to the temp
    os.rename(filepath, tmp_filepath)

    # Step 6: Generate the mutant
    # Step 6.1: Read the original file, which is now the temp
    original_file: FileHandler = open(tmp_filepath, "r")
    original_contents: str = original_file.read()
    original_file.close()
    # Step 6.2: Parse the tree for the original program
    parser: Parser = Parser.c()
    tree: Tree = parser.parse(original_contents)
    # Step 6.3: Create the mutant
    mutator: Mutator = Mutator(parser)
    mutated_tree: Tree = mutator.mutate(tree)
    # Step 6.4: Write the mutant to the original filepath
    mutant_file: FileHandler = open(filepath, "w+")
    mutant_file.write(mutated_tree.text)
    mutant_file.close()

    # Step 7: Test the mutant program
    mutant_results_file: str = open(f'{mutant_results_filepath}', 'w')
    subprocess.run(build_cmd)
    subprocess.run(test_cmd, stdout=mutant_results_file)
    mutant_results_file.close()

    # Step 8: Move the original program into the mutant
    #   If we want to persist then store the mutant another place
    if persist: os.rename(filepath, f'{filepath}.mut')
    os.rename(tmp_filepath, filepath)

    # Step 9: Clean up
    # Step 9.1: Remove canaries in the original file
    new_inf_original_file: FileHandler = open(filepath, "w+")
    new_inf_original_file.write(unit_analysis_response.tree.text)
    new_inf_original_file.close()