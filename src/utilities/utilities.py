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
        self.input_file_name: str = args.input
        self.input_file = fileHandler.open(self.input_file_name, "r")
        self.input_file_text = self.input_file.read()
        self.input_file.close()

        self.output_file_name: str = args.output

    def write_file(self, program: any):
        file = open(self.output_file_name, "w+")
        file.write(program.to_string())