import unittest

from .setupCommandLine import *


class Test_CommandLine(unittest.TestCase):
    def setUp(self):
        self.parser = setupCommandLine()

    # def test_does_not_throw_on_two_c_file_inputs(self):
    #     self.parser.parse_args(['file_name.c file_name.c', "test"])

    # def test_does_throw_on_only_one_input(self):
    #     self.assertRaises(Exception, self.parser.parse_args(['file_name.c', "test"]))


