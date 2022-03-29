from typing import Union, List

from application import (
    InitializeSystemRequest,
    InitializeSystemUseCase,
    UnitAnalyseFileRequest,
    UnitAnalyseFileResponse,
    UnitAnalyseFileUseCase,
    CreateInitialTestCasesRequest,
    CreateInitialTestCasesResponse,
    CreateInitialTestCasesUseCase,
)

from graphviz import Digraph
from mutator import Mutator
from ts import (
    LanguageLibrary,
    Parser,
    Tree,
    CSyntax,
    Language,
    Query,
    Capture,
    Node,
)
from utilities import (
    FileHandler
)
from tree_infestator import (
    TreeInfestator,
    CTreeInfestator,
    CanaryFactory,
    CCanaryFactory
)
from test_generator import (
    FunctionDeclaration,
    DependencyResolver,
    CuTestSuiteCodeGenerator,
    TestCase,
    TestSuite,
    CuTestLinker,
)
from cfa import (
    CFAFactory,
    CFA,
    CCFAFactory
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
    create_initial_test_case_response = CreateInitialTestCasesUseCase().do(
        create_initial_test_case_request
    )

    # Step 3: Infest the original file with canaries
    # Step 3.1: Read the file of the orginal program
    inf_original_file: FileHandler = open(filepath, "r")
    inf_original_contents: str = inf_original_file.read()
    inf_original_file.close()
    # Step 3.2: Parse the file
    inf_parser: Parser = Parser.c()
    inf_tree: Tree = inf_parser.parse(inf_original_contents)
    # Step 3.3: Create CFA for the FUT
    inf_cfa_factory: CFAFactory = CCFAFactory(inf_tree)
    fut_body: Node = unit_analysis_response.unit_function.child_by_field_name("body")
    inf_cfa: CFA = inf_cfa_factory.create(fut_body)
    inf_cfa_graph: Digraph = inf_cfa.draw(inf_tree, "cfa_fut_org")
    inf_cfa_graph.save(directory=f'{base}/')
    # Step 3.4: Infest
    canary_factory: CanaryFactory = CCanaryFactory()
    infestator: TreeInfestator = CTreeInfestator(inf_parser, canary_factory)
    inf_int_tree: Tree = infestator.infect(inf_tree, inf_cfa)
    # Step 3.5: Write the infestation
    new_inf_original_file: FileHandler = open(filepath, "w+")
    new_inf_original_file.write(inf_int_tree.text)
    new_inf_original_file.close()

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