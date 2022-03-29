import re
from typing import Any, List

class FailedCuTest:
    def __init__(self, testName: str, testSrc: str):
        self.testName = testName
        self.testSrc = testSrc
        self.expected : Any = None
        self.actual: Any = None
        self.assert_failed: str = None
    
class CuTestParser:
    def __init__(self, source:str):
        self.src = source

    @staticmethod
    def parse(source : str) -> List[FailedCuTest]:
        file = open(source, "r")
        file_str : str = file.readlines()
        failed_tests : List[FailedCuTest] = []

        # Dictionary for handling CuTest Error messages in Regex
        regex_error_msg = {
            'whole_err_line' : r'(\d+\) \w+): ([\/?\w?\/?]*\w+\.c.\d+): (.*)',  # 5) addTest_StringTest: /input/tests/AllTests.c:72: expected <expected> but was <actual haha snydt>
            'test_name': r'\d+\) \w+:',                                         # 5) addTest_StringTest:
            'test_src': r'[\/?\w?\/?]*\w+\.c.\d+',                              # /input/tests/AllTests.c:72:
            'assert_failed': r'(assert failed)',                                # assert failed
            'expected_int': r'expected <(\d+)> ',                               # expected <2> 
            'actual_int': r'but was <(\d+)>',                                   # but was <4>
            'expected_double':  r'expected <(\d+\.\d+)>',                       # expected <2.00> 
            'actual_double': r'but was <(\d+\.?\d*)>',                          # but was <4.00>
            'expected_pointer' : r'expected pointer <0x([a-zA-Z0-9]*)>',        # expected pointer <0x0x7ffdbabe7b4c> 
            'actual_pointer': r'but was <0x([a-zA-Z0-9]*)>',                    # but was <0x0x7ffdbabe7b48>
            'expected_string': r'expected <(\w*)>',                             # expected <This is the expected string>
            'actual_string': r'but was <(.+?)>'                                 # but was <This is a totally different string>
        }

        for line in file_str:
            failure_message_appears: bool = re.search(regex_error_msg['whole_err_line'], line)
            if failure_message_appears and failure_message_appears is not None:
                test_name = re.findall(regex_error_msg['test_name'], line)
                test_src = re.findall(regex_error_msg['test_src'], line)
                failed_cutest = FailedCuTest(test_name, test_src)
                
                test_explanation = failure_message_appears.group(3)

                is_int_error = re.search(regex_error_msg['expected_int'], test_explanation)
                is_double_error = re.search(regex_error_msg['expected_double'], test_explanation)
                is_pointer_error = re.search(regex_error_msg['expected_pointer'], test_explanation)
                is_assert_error = re.search(regex_error_msg['assert_failed'], test_explanation)
                is_string_error = re.search(regex_error_msg['expected_string'], test_explanation)

                if is_int_error:
                    failed_cutest = CuTestParser.parse_int_error(regex_error_msg, failed_cutest, test_explanation)

                elif is_double_error:
                    failed_cutest = CuTestParser.parse_double_error(regex_error_msg, failed_cutest, test_explanation)

                elif is_pointer_error:
                    failed_cutest = CuTestParser.parse_pointer_error(regex_error_msg, failed_cutest, test_explanation)

                elif is_assert_error:
                    failed_cutest = CuTestParser.parse_assert_true_error(regex_error_msg, failed_cutest, test_explanation)
                elif is_string_error:
                    failed_cutest = CuTestParser.parse_string_error(regex_error_msg, failed_cutest, test_explanation)
                
                failed_tests.append(failed_cutest)
            
        file.close()
        return failed_tests  
    
    @staticmethod
    def parse_int_error(regex_error_msg, failed_cutest: FailedCuTest, test_explanation: str) -> FailedCuTest:
        int_expected_temp = re.search(regex_error_msg['expected_int'], test_explanation).group(1)
        int_actual_temp = re.search(regex_error_msg['actual_int'], test_explanation).group(1)
        int_expected = int(int_expected_temp)
        int_actual = int(int_actual_temp)

        failed_cutest.expected = int_expected
        failed_cutest.actual = int_actual

        return failed_cutest

    @staticmethod
    def parse_double_error(regex_error_msg, failed_cutest: FailedCuTest, test_explanation: str) -> FailedCuTest:
        double_expected_temp = re.search(regex_error_msg['expected_double'], test_explanation).group(1)
        double_actual_temp = re.search(regex_error_msg['actual_double'], test_explanation).group(1)
        double_actual = float(double_actual_temp)
        double_expected = float(double_expected_temp)  

        failed_cutest.expected = double_expected
        failed_cutest.actual = double_actual

        return failed_cutest


    @staticmethod
    def parse_pointer_error(regex_error_msg, failed_cutest: FailedCuTest, test_explanation: str) -> FailedCuTest:
        pointer_expected = re.search(regex_error_msg['expected_pointer'], test_explanation).group(1)
        pointer_actual = re.search(regex_error_msg['actual_pointer'], test_explanation).group(1)

        failed_cutest.expected = pointer_expected
        failed_cutest.actual = pointer_actual
        
        return failed_cutest

    @staticmethod
    def parse_assert_true_error(regex_error_msg, failed_cutest: FailedCuTest, test_explanation: str) -> FailedCuTest:
        assert_failed = re.findall(regex_error_msg['assert_failed'], test_explanation)
        failed_cutest.assert_failed = str(assert_failed)

        return failed_cutest
    
    @staticmethod
    def parse_string_error(regex_error_msg, failed_cutest: FailedCuTest, test_explanation: str) -> FailedCuTest:
        string_expected = re.search(regex_error_msg['expected_string'], test_explanation).group(1)
        string_actual = re.search(regex_error_msg['actual_string'], test_explanation).group(1)

        failed_cutest.expected = string_expected
        failed_cutest.actual = string_actual

        return failed_cutest


# When running this, remember to include correct asserts in your test suite :))) 
# 
# failed = CuTestParser.parse("../examples/c_06/src/original.h.mut.results")

# for fail in failed: 
#     print(fail.testName)
#     print("______________________________")
#     print("Expected:")
#     print(fail.expected)
#     print(type(fail.expected))

#     print("Actual:")
#     print(fail.actual)
#     print(type(fail.actual))

#     print("Assert failed:")
#     print(fail.assert_failed)
#     print(type(fail.assert_failed))
    


#     print("\n\n")
#     print("\n\n")