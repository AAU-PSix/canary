import re

from typing.io import TextIO


class FileHandler:
    def __init__(self):
        pass

    @staticmethod
    def open(file, mode='r', buffering=None, encoding=None, errors=None, newline=None, closefd=True) -> TextIO:
        return open(file, mode, buffering, encoding, errors, newline, closefd)


class CanaryIOHandler:
    def __init__(self, args, fileHandler: FileHandler):
        if not re.match("^[^\n ]*\.c$", args.inputfile):
            raise Exception("Input is not a c file.")
        self.input_file_name: str = args.inputfile
        self.input_file = fileHandler.open(self.input_file_name, "r")
        self.input_file_text = self.input_file.read()
        self.input_file.close()

        if not re.match("^[^\n ]*\.c$", args.outputfile):
            raise Exception("Output is not a c file.")
        self.output_file_name: str = args.inputfile

    def write_file(self, program: any):
        file = open(self.output_file_name, "w+")
        file.write(program.to_string())
