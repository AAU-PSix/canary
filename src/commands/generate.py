from typing import Union, List

from graphviz import Digraph
from mutator import Mutator
from ts import (
    LanguageLibrary,
    Parser,
    Tree,
    Syntax,
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
    CanaryFactory,
    CCanaryFactory
)
from cfa import TreeCFAVisitor, CFA
import subprocess
import os

def generate(
    file: str,
    build_cmd: Union[str, List[str]],
    test_cmd: Union[str, List[str]],
    base: str = "",
    persist: bool = False,
):
    filepath: str = f'{base}/{file}'
    tmp_filepath: str = f'{base}/{file}.tmp'
    original_results_filepath: str = f'{filepath}.org.results'
    mutant_results_filepath: str = f'{filepath}.mut.results'

    # Step 0: Initialize the system
    LanguageLibrary.build()

    # Step 1: Unit analysis to find FUT (Funtion Under Test)
    # Step 1.1: Read the file of the orginal program
    unit_original_file: FileHandler = open(filepath, "r")
    unit_original_contents: str = unit_original_file.read()
    unit_original_file.close()
    # Step 1.2: Parse the file
    unit_parser: Parser = Parser.c()
    unit_tree: Tree = unit_parser.parse(unit_original_contents)
    # Step 1.3: Get function definitions
    c_language: Language = LanguageLibrary.c()
    c_syntax: Syntax = c_language.syntax
    c_unit_query: Query = c_language.query(c_syntax.query_function_declaration)
    unit_capture: Capture = c_unit_query.captures(unit_tree.root_node)
    unit_function_definitions: List[Node] = unit_capture.nodes(
        c_syntax.get_function_declaration
    )
    # Step 1.4: Pick a FUT
    fut_root: Node = None
    fut_name: str = "add"
    for func in unit_function_definitions:
        func_declarator: Node = func \
            .child_by_field_name("declarator") \
            .child_by_field_name("declarator")
        func_name: str = unit_tree.contents_of(func_declarator)
        if func_name == fut_name:
            fut_root = func
            break

    if fut_root is None:
        print("Could not find FUT")
        return

    # Step 2: Infest the original file with canaries
    # Step 2.1: Read the file of the orginal program
    inf_original_file: FileHandler = open(filepath, "r")
    inf_original_contents: str = inf_original_file.read()
    inf_original_file.close()
    # Step 2.2: Parse the file
    inf_parser: Parser = Parser.c()
    inf_tree: Tree = inf_parser.parse(inf_original_contents)
    # Step 2.3: Create CFA for the FUT
    inf_cfa_factory: TreeCFAVisitor = TreeCFAVisitor(inf_tree)
    fut_body: Node = fut_root.child_by_field_name("body")
    inf_cfa: CFA = inf_cfa_factory.create(fut_body, False)
    inf_cfa_graph: Digraph = inf_cfa.draw(inf_tree, "cfa_fut_org")
    inf_cfa_graph.save(directory=f'{base}/')
    # Step 2.4: Infest
    canary_factory: CanaryFactory = CCanaryFactory()
    infestator: TreeInfestator = TreeInfestator(inf_parser, canary_factory)
    inf_int_tree: Tree = infestator.infect(inf_tree, inf_cfa)
    # Step 2.5: Write the infestation
    new_inf_original_file: FileHandler = open(filepath, "w+")
    new_inf_original_file.write(inf_int_tree.text)
    new_inf_original_file.close()

    # Step 3: Test the original program
    original_results_file: str = open(original_results_filepath, 'w')
    subprocess.run(build_cmd)
    subprocess.run(test_cmd, stdout=original_results_file)
    original_results_file.close()

    # Step 4: Rename the original file to the temp
    os.rename(filepath, tmp_filepath)

    # Step 5: Generate the mutant
    # Step 5.1: Read the original file, which is now the temp
    original_file: FileHandler = open(tmp_filepath, "r")
    original_contents: str = original_file.read()
    original_file.close()
    # Step 5.2: Parse the tree for the original program
    parser: Parser = Parser.c()
    tree: Tree = parser.parse(original_contents)
    # Step 5.3: Create the mutant
    mutator: Mutator = Mutator(parser)
    mutated_tree: Tree = mutator.mutate(tree)
    # Step 5.4: Write the mutant to the original filepath
    mutant_file: FileHandler = open(filepath, "w+")
    mutant_file.write(mutated_tree.text)
    mutant_file.close()

    # Step 6: Test the mutant program
    mutant_results_file: str = open(f'{mutant_results_filepath}', 'w')
    subprocess.run(build_cmd)
    subprocess.run(test_cmd, stdout=mutant_results_file)
    mutant_results_file.close()

    # Step 7: Move the original program into the mutant
    #   If we want to persist then store the mutant another place
    if persist: os.rename(filepath, f'{filepath}.mut')
    os.rename(tmp_filepath, filepath)

    # Step 8: Clean up
    # Step 8.1: Remove canaries in the original file
    new_inf_original_file: FileHandler = open(filepath, "w+")
    new_inf_original_file.write(unit_original_contents)
    new_inf_original_file.close()