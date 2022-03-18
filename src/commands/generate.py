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

    # Step 0: Initialize the system
    LanguageLibrary.build()

    # Step 1: Test the original program
    original_results_file: str = open(f'{filepath}.org.results', 'w')
    subprocess.run(build_cmd)
    subprocess.run(test_cmd, stdout=original_results_file)
    original_results_file.close()

    # Step 2: Rename the original file to the temp
    os.rename(filepath, tmp_filepath)

    # Step 3: Generate the mutant
    # Step 3.1: Read the original file, which is now the temp
    original_file: FileHandler = open(tmp_filepath, "r")
    original_contents: str = original_file.read()
    original_file.close()
    # Step 3.2: Parse the tree for the original program
    parser: Parser = Parser.c()
    tree: Tree = parser.parse(original_contents)
    # Step 3.3: Create the mutant
    mutator: Mutator = Mutator(parser)
    mutated_tree: Tree = mutator.mutate(tree)
    # Step 3.4: Write the mutant to the original filepath
    mutant_file: FileHandler = open(filepath, "w+")
    mutant_file.write(mutated_tree.text)
    mutant_file.close()

    # Step 4: Test the mutant program
    mutant_results_file: str = open(f'{filepath}.mut.results', 'w')
    subprocess.run(build_cmd)
    subprocess.run(test_cmd, stdout=mutant_results_file)
    mutant_results_file.close()

    # Step 5: Move the original program into the mutant
    #   If we want to persist then store the mutant another place
    if persist: os.rename(filepath, f'{filepath}.mut')
    os.rename(tmp_filepath, filepath)
