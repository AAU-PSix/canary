from time import sleep
from mutator import Mutator
from ts import (
    LanguageLibrary,
    Parser,
    Tree,
)
from utilities import (
    ArgumentParser,
    setupCommandLine,
    FileHandler
)
import subprocess
import os 

def main():
    # Mutate, run test on original, switch original with mutant, run tests on the mutant, switch original back
    LanguageLibrary.build()
    commandLineParser: ArgumentParser = setupCommandLine()
    args = commandLineParser.parse_args()
    original_file_path: str = args.input
    mutated_file_path: str = args.output

    input_file: FileHandler = open(original_file_path, "r")
    input_contents: str = input_file.read()
    input_file.close()

    parser: Parser = Parser.c()
    tree: Tree = parser.parse(input_contents)

    mutator = Mutator(parser)
    mutated_tree: Tree = mutator.mutate(tree)

    output_file: str = open(mutated_file_path, "w+")
    output_file.write(mutated_tree.text)
    output_file.close()

<<<<<<< HEAD
    original_results_file: str = open("/input/original_results.txt", "w")
    subprocess.run(["make", "-C", "/input/", "build"])
    subprocess.run(["/input/build/c_06_test"], stdout=original_results_file)
    original_results_file.close()
    
    os.rename(original_file_path, original_file_path + ".tmp")
    os.rename(mutated_file_path, original_file_path)

    mutated_results_file: str = open("/input/mutated_results.txt", "w")
    subprocess.run(["make", "-C", "/input/", "build"])
    subprocess.run(["/input/build/c_06_test"], stdout=mutated_results_file)
    mutated_results_file.close()
    
    os.rename(original_file_path + ".tmp", original_file_path)
=======
    # original_results_file: str = open("/input/original_results.txt", "w")
    # subprocess.run(["make", "-C", "/input/", "build"])
    # subprocess.run(["/input/build/c_06_test"], stdout=original_results_file)
    
    # os.rename(original_file_path, original_file_path + ".tmp")
    # os.rename(mutated_file_path, original_file_path)
    # sleep(1)

    # mutated_results_file: str = open("/input/mutated_results.txt", "w")
    # subprocess.run(["make", "-C", "/input/", "build"])
    # subprocess.run(["/input/build/c_06_test"], stdout=mutated_results_file)
>>>>>>> c14600d93b68bfb7ed8c33e2836472ab39eabff1
    
    # original_results_file: str = open("/input/original_results.txt", "w")
    # subprocess.run(["make", "-C", "/input/", "build"])
    # subprocess.run(["/input/build/c_06_test"], stdout=original_results_file)
    # os.rename(path + mutated_file_name, path + original_file_name)
    


if __name__ == "__main__":
    main()
