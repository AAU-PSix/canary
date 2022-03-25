from ast import Num
from cgi import test
from hashlib import new
from imghdr import tests
from nis import match
import re
from tokenize import Number
from typing import Any, List

from numpy import mat
from utilities import FileHandler


class FailedCuTest:
    def __init__(self, testName: str, testSrc: str, expected: Any, actual: int):
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
            'test_name': r'\d+\) \w+:',
            'test_src': r'[\/?\w?\/?]*\w+\.c.\d+',
            'assert_failed': r'(assert failed)',
            'expected_int': r'expected <(\d+)> ',
            'actual_int': r'but was <(\d+)>',
            'expected_double':  r'expected <(\d+\.\d+)>',
            'actual_double': r'but was <(\d+\.?\d*)>',
            'expected_pointer' : r'expected pointer <0x([a-zA-Z0-9]*)>',
            'actual_pointer': r'but was <0x([a-zA-Z0-9]*)>',
            'expected_string': r'expected <(.*?)>'
        }

        for line in fileStr:
            if (re.search(regex_error_msg['test_name'], line) is not None):
                match = re.search(regex_error_msg['whole_err_line'], line)
                if match:
                    print("\n\n")
                    print(match.group())
                    print(match.group(1))
                    print(match.group(2))
                    print(match.group(3))
                    test_name = re.findall(regex_error_msg['test_name'], line)
                    test_src = re.findall(regex_error_msg['test_src'], line)
                    testExplanation = match.group(3)
                    if re.search(r'expected <',testExplanation):
                        print("Chose Expected for number values")

                        if re.search(regex_error_msg['expected_int'], testExplanation):
                            int_expected_temp = re.search(regex_error_msg['expected_int'], testExplanation).group(1)
                            int_actual_temp = re.search(regex_error_msg['actual_int'], testExplanation).group(1)
                            int_expected = int(int_expected_temp)
                            int_actual = int(int_actual_temp)
                            print(str(type(int_expected)) + "Value is : " + str(int_expected))
                            print(str(type(int_actual)) + "Value is : " + str(int_actual))
                            print("INT HEREEEEE!!!!!!")

                        elif re.search(regex_error_msg['expected_double'], testExplanation):
                            double_expected_temp = re.search(regex_error_msg['expected_double'], testExplanation).group(1)
                            double_actual_temp = re.search(regex_error_msg['actual_double'], testExplanation).group(1)
                            double_actual = float(double_actual_temp)
                            double_expected = float(double_expected_temp)  
                            print(str(type(double_expected)) + "Value is : " + str(double_expected))
                            print(str(type(double_actual)) + "Value is : " + str(double_actual))
                            print("DOUBLEEEEEEEEEEEE HEREEEEE!!!!!!")

                    elif re.search(r'expected pointer <', testExplanation):
                        #Assuming that pointers will only be shown as ints at the moment
                        pointer_expected = re.search(regex_error_msg['expected_pointer'], testExplanation).group(1)
                        pointer_actual = re.search(regex_error_msg['actual_pointer'], testExplanation).group(1)

                    elif re.search(regex_error_msg['assert_failed'], testExplanation):
                        assert_failed = re.search(regex_error_msg['assert_failed'], testExplanation).group(1)

                




                        
                    expected = re.findall(regex_error_msg['expected_int'], line)
                    
                    actual = re.findall(r"but was <\d+>", line)


            # if len(testName) > 0:
            #     expectedTemp = re.findall(r'\d+', expected[0])
            #     actualTemp = re.findall(r'\d+', actual[0])
            #     expected = list(map(int, expectedTemp))[0]    
            #     actual = list(map(int,actualTemp))[0]
            #     failedTest = FailedCuTest(testName, testSrc, expected, actual)
            #     failedTests.append(failedTest)
            
        file.close()
        # return failedTests  
        



CuTestParser.parse("../examples/c_06/src/original.h.mut.results")