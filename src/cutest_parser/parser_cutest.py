from abc import ABC
from ctypes import pointer
from curses.ascii import isdigit
from distutils.log import error
from ftplib import error_perm, error_reply
from operator import contains
import re
from typing import Any, List
from pprint import pprint

class FailedCuTest(ABC):
    def __init__(self, testName: str, testSrc: str):
        self.testName = testName
        self.testSrc = testSrc

class FailedCuTestExpAss(FailedCuTest):
    def __init__(self, testName: str, testSrc: str):
        self.expected : str = None
        self.actual : str = None
        super().__init__(testName, testSrc)

class FailedCuTestAss(FailedCuTest):
    def __init__(self, testName: str, testSrc: str):
        self.assert_result : str = None 
        super().__init__(testName, testSrc)


class CuTestParser:
    def __init__(self):
        self.lines : List[str] = [] 

    def read_parse_file(source : str) -> List[str]:
        file = open(source, "r")
        file_str : str = file.readlines()
        
        line_list = []
        for line in file_str:
            if line[0].isdigit() and ") " in line:
                line_list.append(line)
        file.close()

        return line_list


    def parse(lines : List[str]) -> List[FailedCuTest]:
        
        CuTestList : List[FailedCuTest] = []
        

        # A line is split into 3 parts: name, source, assert result
        for line in lines:
            
            if line[0].isdigit():
                error_line = line.split(": ")
                error_line[0] = CuTestParser.trim_function_name_group(error_line[0])
                # fixes: expected< test: 1hest: > but was < hest : hesst>
                if len(error_line) > 3:
                    error_line[2] = ": ".join(error_line[2:])
                      
                # Just a single assert_true
                if "assert" in error_line[2]:
                    error = CuTestParser.trim_single_assert_group(error_line, FailedCuTestAss(error_line[0], error_line[1]))
                    CuTestList.append(error)
               
               # Assert with expected and actual 
                if "expected <" in error_line[2] or "expected pointer <" in error_line[2] and "but was <" in error_line[2]:
                    error = CuTestParser.trim_expected_actual_group(error_line, FailedCuTestExpAss(error_line[0], error_line[1]))
                    CuTestList.append(error)
                    

        return CuTestList  
    
    @staticmethod
    def trim_expected_actual_group(error_line: str, exp_ass_cutest: FailedCuTestExpAss) -> FailedCuTestExpAss:
        if "expected pointer <" in error_line[2]:
            error_line[2] = error_line[2].replace("expected pointer <", "")
        else:
            error_line[2] = error_line[2].replace("expected <", "")
        error_line[2] = error_line[2].replace("> but was <", "SplitActualStringThingBading")
        error_line[2] = error_line[2].replace(">\n", "")
        
        error = error_line[2].split("SplitActualStringThingBading")

        exp_ass_cutest.testName = error_line[0]
        exp_ass_cutest.testSrc = error_line[1]
        exp_ass_cutest.expected = error[0]
        exp_ass_cutest.actual = error[1]

        return exp_ass_cutest

    @staticmethod
    def trim_single_assert_group(error_line: str, single_assert: FailedCuTestAss) -> FailedCuTestAss:
        error_line[2] = error_line[2].replace("\n", "")
        single_assert.assert_result = error_line[2]
        return single_assert

    @staticmethod
    def trim_function_name_group(error_line: str) -> str:
        error_line = error_line.split()
        return error_line[1]

# When running this, remember to include correct asserts in your test suite :))) 
CuTestList = CuTestParser.parse("/home/daniel/repos/canary/src/cutest_parser/test_strings/original.h.mut copy.results")

for test in CuTestList:
    pprint(vars(test))