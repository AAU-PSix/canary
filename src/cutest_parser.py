from cgi import test
from hashlib import new
from imghdr import tests
from nis import match
import re
from typing import List
from utilities import FileHandler


class FailedCuTest:
    def __init__(self, testName: str, testSrc: str, expected: int, actual: int):
        self.testName = testName
        self.testSrc = testSrc
        self.expected = expected
        self.actual = actual
    
class CuTestParser:
    def __init__(self, source:str):
        self.src = source

    @staticmethod
    def parse(source : str) -> List[FailedCuTest]:
        file = open(source, "r")
        fileStr : str = file.readlines()      
        failedTests : List[FailedCuTest] = []

        regex_error_msg = {
            'whole_err_line' : r'(\d+\) \w+): ([\/?\w?\/?]*\w+\.c.\d+): (.*)',
            'test_name': r"\d+\) \w+:",
            'test_src': r'[\/?\w?\/?]*\w+\.c.\d+',
            'assert_failed': r'assert failed',
            'expected_int': r'expected <(\d+)> ',
            'actual_int': r'but was <(\d+)>',
            'expected_double':  r'expected <(\d+\.\d+)>',
            'actual_double': r'but was <(\d+\.\d+)>',
        }

        for line in fileStr:
            if (re.search(regex_error_msg['test_name'], line) is not None):
                match = re.search(regex_error_msg['whole_err_line'], line)
                if match:
                    print(match.group())
                    print(match.group(1))
                    print(match.group(2))
                    print(match.group(3))
                    testName = re.findall(regex_error_msg['test_name'], line)
                    testSrc = re.findall(regex_error_msg['test_src'], line)
                    
                    expected = re.findall(regex_error_msg['expected_int'], line)
                    
            #         actual = re.findall(r"but was <\d+>", line)


            # if len(testName) > 0:
            #     expectedTemp = re.findall(r'\d+', expected[0])
            #     actualTemp = re.findall(r'\d+', actual[0])
            #     expected = list(map(int, expectedTemp))[0]    
            #     actual = list(map(int,actualTemp))[0]
            #     failedTest = FailedCuTest(testName, testSrc, expected, actual)
            #     failedTests.append(failedTest)
            
        file.close()
        # return failedTests

    def _findHest(string : str) -> str:
        pass


CuTestParser.parse("../examples/c_06/src/original.h.mut.results")