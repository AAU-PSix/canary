from abc import ABC
from distutils.log import error
from ftplib import error_perm, error_reply
import re
from typing import Any, List

class FailedCuTest(ABC):
    def __init__(self, testName: str, testSrc: str):
        self.testName = testName
        self.testSrc = testSrc

class IntFailedCutest(FailedCuTest):
    def __init__(self, testName: str, testSrc: str):
        self.expected : int = None
        self.actual : int = None
        super().__init__(testName, testSrc)

class DoubleFailedCutest(FailedCuTest):
    def __init__(self, testName: str, testSrc: str):
        self.expected : float = None
        self.actual : float = None
        super().__init__(testName, testSrc)

class BoolFailedCutest(FailedCuTest):
    def __init__(self, testName: str, testSrc: str):
        self.assert_bool : str = None 
        super().__init__(testName, testSrc)

class PointerFailedCutest(FailedCuTest):
    def __init__(self, testName: str, testSrc: str):
        self.expected : str = None
        self.actual : str = None
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
                if "expected pointer" in error_line[2]:
                    error = CuTestParser.trim_pointer_group(error_line, PointerFailedCutest(error_line[0], error_line[1]))
                    CuTestList.append(error)

                # Assert bool
                if "assert failed" in error_line[2]:
                    error = CuTestParser.trim_bool_assert_group(error_line, BoolFailedCutest(error_line[0], error_line[1]))
                    CuTestList.append(error)

                # Assert int
                if "expected <" in error_line[2] and "but was <" in error_line[2] and "." not in error_line[2]:
                    error = CuTestParser.trim_int_group(error_line, IntFailedCutest(error_line[0], error_line[1]))
                    CuTestList.append(error)
               
               # Assert double
                if "expected <" in error_line[2] and "but was <" in error_line[2] and "." in error_line[2]:
                    error = CuTestParser.trim_double_group(error_line, DoubleFailedCutest(error_line[0], error_line[1]))
                    CuTestList.append(error)
                    
     
        file.close()
        return CuTestList  
    
    @staticmethod
    def trim_int_group(error_line: str, intCuTest: IntFailedCutest) -> IntFailedCutest:
        error_line[2] = error_line[2].replace("expected <", "")
        error_line[2] = error_line[2].replace("> but was <", " ")
        error_line[2] = error_line[2].replace(">\n", "")
        
        error = error_line[2].split()

        intCuTest.testName = error_line[0]
        intCuTest.testSrc = error_line[1]
        intCuTest.expected = int(error[0])
        intCuTest.actual = int(error[1])

        return intCuTest

    @staticmethod
    def trim_double_group(error_line: str, doubleCuTest: DoubleFailedCutest ) -> DoubleFailedCutest:
        error_line[2] = error_line[2].replace("expected <", "")
        error_line[2] = error_line[2].replace("> but was <", " ")
        error_line[2] = error_line[2].replace(">\n", "")

        error = error_line[2].split()

        doubleCuTest.testName = error_line[0]
        doubleCuTest.testSrc = error_line[1]
        doubleCuTest.expected = float(error[0])
        doubleCuTest.actual = float(error[1])

        return doubleCuTest

    @staticmethod
    def trim_pointer_group(error_line: str, pointerCuTest: PointerFailedCutest) -> PointerFailedCutest:
        error_line[2] = error_line[2].replace("expected pointer <", "")
        error_line[2] = error_line[2].replace("> but was <", " ")
        error_line[2] = error_line[2].replace(">\n", "")

        error_line[2] = error_line[2].split(" ")
        
        pointerCuTest.testName = error_line[0]
        pointerCuTest.testSrc = error_line[1]
        pointerCuTest.expected = error_line[2][0]
        pointerCuTest.actual = error_line[2][1]
        
        return error_line

    @staticmethod
    def trim_bool_assert_group(error_line: str, boolCuTest: BoolFailedCutest) -> BoolFailedCutest:
        error_line[2] = error_line[2].replace("\n", "")
        
        return error_line

    @staticmethod
    def trim_function_name_group(error_line: str) -> str:
        error_line = error_line.split()
        return error_line[1]

# When running this, remember to include correct asserts in your test suite :))) 
CuTestList = CuTestParser.parse("../examples/c_06/src/original.h.mut.results")

for test in CuTestList:
    print(test.testName)
