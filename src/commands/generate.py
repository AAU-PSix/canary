from typing import Union, List
from mutator import Mutator
from ts import (
    LanguageLibrary,
    Parser,
    Tree
)
from utilities import (
    FileHandler
)
from tree_infestator import TreeInfestator
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
    mutant_results_filepath: str = f'{filepath}.org.results'

    # Step 0: Initialize the system
    LanguageLibrary.build()

    # Step 1: Infest the original file with canaries
    # Step 1.1: Read the file of the orginal program
    inf_original_file: FileHandler = open(filepath, "r")
    inf_original_contents: str = inf_original_file.read()
    inf_original_file.close()
    # Step 1.2: Parse the file
    inf_parser: Parser = Parser.c()
    inf_tree: Tree = inf_parser.parse(inf_original_contents)
    # Step 1.3: Create CFA
    inf_cfa_factory: TreeCFAVisitor = TreeCFAVisitor(inf_tree)
    inf_cfa: CFA = inf_cfa_factory.create(inf_tree)
    # Step 1.4: Infest
    infestator: TreeInfestator = TreeInfestator(inf_parser)
    inf_int_tree: Tree = infestator.infect(inf_tree, inf_cfa)
    # Step 1.5: Write the infestation
    new_inf_original_file: FileHandler = open(filepath, "w+")
    new_inf_original_file.write(inf_int_tree.text)
    new_inf_original_file.close()

    # Step 2: Test the original program
    original_results_file: str = open(original_results_filepath, 'w')
    subprocess.run(build_cmd)
    subprocess.run(test_cmd, stdout=original_results_file)
    original_results_file.close()

    # Step 3: Rename the original file to the temp
    os.rename(filepath, tmp_filepath)

    # Step 4: Generate the mutant
    # Step 4.1: Read the original file, which is now the temp
    original_file: FileHandler = open(tmp_filepath, "r")
    original_contents: str = original_file.read()
    original_file.close()
    # Step 4.2: Parse the tree for the original program
    parser: Parser = Parser.c()
    tree: Tree = parser.parse(original_contents)
    # Step 4.3: Create the mutant
    mutator: Mutator = Mutator(parser)
    mutated_tree: Tree = mutator.mutate(tree)
    # Step 4.4: Write the mutant to the original filepath
    mutant_file: FileHandler = open(filepath, "w+")
    mutant_file.write(mutated_tree.text)
    mutant_file.close()

    # Step 5: Test the mutant program
    mutant_results_file: str = open(f'{mutant_results_filepath}', 'w')
    subprocess.run(build_cmd)
    subprocess.run(test_cmd, stdout=mutant_results_file)
    mutant_results_file.close()

    # Step 6: Move the original program into the mutant
    #   If we want to persist then store the mutant another place
    if persist: os.rename(filepath, f'{filepath}.mut')
    os.rename(tmp_filepath, filepath)
