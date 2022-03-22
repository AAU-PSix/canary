from cgi import test
from hashlib import new
from imghdr import tests
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

        for line in fileStr[3:-2]:
            testName = re.findall(r"\d+\) \w+", line)
            testSrc = re.findall(r"[\/?\w?\/?]*\w+\.c.\d+", line)
            expected = re.findall(r"expected <\d+>", line)
            actual = re.findall(r"but was <\d+>", line)

            if len(expected) > 0:
                expectedTemp = re.findall(r'\d+', expected[0])
                actualTemp = re.findall(r'\d+', actual[0])
                expected = list(map(int, expectedTemp))[0]    
                actual = list(map(int,actualTemp))[0]
                failedTest = FailedCuTest(testName, testSrc, expected, actual)

            failedTests.append(failedTest)
        file.close()
        return failedTests