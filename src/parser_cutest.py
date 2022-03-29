from abc import ABC
from ctypes import pointer
from distutils.log import error
from ftplib import error_perm, error_reply
import re
from typing import Any, List
from pprint import pprint

class FailedCuTest(ABC):
    def __init__(self, testName: str, testSrc: str):
        self.testName = testName
        self.testSrc = testSrc

class TwoAssertFailedCutest(FailedCuTest):
    def __init__(self, testName: str, testSrc: str):
        self.expected : str = None
        self.actual : str = None
        super().__init__(testName, testSrc)

class OneAssertFailedCutest(FailedCuTest):
    def __init__(self, testName: str, testSrc: str):
        self.assert_result : str = None 
        super().__init__(testName, testSrc)


class CuTestParser:
    def __init__(self, source:str):
        self.src = source

    def parse(source : str) -> List[FailedCuTest]:
        file = open(source, "r")
        file_str : str = file.readlines()
        CuTestList : List[FailedCuTest] = []
        

        # A line is split into 3 parts: name, source, assert result
        for line in file_str:
            
            if line[0].isdigit():
                error_line = line.split(": ")
                error_line[0] = CuTestParser.trim_function_name_group(error_line[0])
                
                # Assert pointer
                if "assert" in error_line[2]:
                    error = CuTestParser.trim_single_assert_group(error_line, OneAssertFailedCutest(error_line[0], error_line[1]))
                    CuTestList.append(error)
               
               # Assert with expected and actual 
                if "expected <" in error_line[2] or "expected pointer <" in error_line[2] and "but was <" in error_line[2]:
                    error = CuTestParser.trim_expected_actual_group(error_line, TwoAssertFailedCutest(error_line[0], error_line[1]))
                    CuTestList.append(error)
                    
     
        file.close()
        return CuTestList  
    
    @staticmethod
    def trim_expected_actual_group(error_line: str, expected_actual: TwoAssertFailedCutest) -> TwoAssertFailedCutest:
        if "expected pointer <" in error_line[2]:
            error_line[2] = error_line[2].replace("expected pointer <", "")
        else:
            error_line[2] = error_line[2].replace("expected <", "")
        error_line[2] = error_line[2].replace("> but was <", " ")
        error_line[2] = error_line[2].replace(">\n", "")
        
        error = error_line[2].split()

        expected_actual.testName = error_line[0]
        expected_actual.testSrc = error_line[1]
        expected_actual.expected = error[0]
        expected_actual.actual = error[1]

        return expected_actual

    @staticmethod
    def trim_single_assert_group(error_line: str, single_assert: OneAssertFailedCutest) -> OneAssertFailedCutest:
        error_line[2] = error_line[2].replace("\n", "")
        single_assert.assert_result = error_line[2]
        return single_assert

    @staticmethod
    def trim_function_name_group(error_line: str) -> str:
        error_line = error_line.split()
        return error_line[1]

# When running this, remember to include correct asserts in your test suite :))) 
CuTestList = CuTestParser.parse("../examples/c_06/src/original.h.mut.results")

for test in CuTestList:
    pprint(vars(test))