from cgi import test
from hashlib import new
import re
from utilities import FileHandler

class CuTestParser:
    def __init__(self) -> None:
        self.re_dict = {
            "failed_test_expected" : re.compile(r'expected <(?<failed__test_expected>\d+)>'),
            "failed_test_actual" : re.compile(r'but was (?<failed_test_actual>\d+)')
        }

    @staticmethod
    def parse(source : str = "examples/c_06/src/original.h.mut.results"):
        
        file = open("../examples/c_06/src/original.h.mut.results", "r")
        fileStr : str = file.readlines()      
        

        # x = re.search("^\d*" , fileStr)
        for line in fileStr[3:-2]:
            expected = re.findall(r"expected <\d+>", line)
            actual = re.findall(r"but was <\d+>", line)
            if len(expected)> 0:
                expectedTemp = re.findall(r'\d+', expected[0])
                actualTemp = re.findall(r'\d+', actual[0])

                expected = list(map(int, expectedTemp))[0]    
                actual = list(map(int,actualTemp))[0]
                print("Expected Number:" + str(expected))
                print("Actual number: " + str(expected))

        file.close()


CuTestParser.parse()

class FailedCuTest:
    def __init__(self, testName: str, testSrc: str, expected: int, actual: 0) -> None:
        self.testName = testName
        self.testSrc = testSrc
        self.expected = expected
        self.actual = actual
    