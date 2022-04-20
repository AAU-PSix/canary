from typing import List

class FailedCuTest():
    def __init__(self, test_name: str, test_src: str):
        self.test_name = test_name
        self.test_src = test_src
        self.expected: str = None
        self.actual: str = None

class CuTestParser:
    def __init__(self):
        self.lines : List[str] = [] 

    def read_parse_file(self, source : str) -> List[str]:
        file = open(source, "r")
        file_str : str = file.readlines()

        line_list = []
        for line in file_str:
            if line[0].isdigit() and ") " in line:
                line_list.append(line)
        file.close()

        return line_list

    def parse(self, lines : List[str]) -> List[FailedCuTest]:

        CuTestList : List[FailedCuTest] = []

        # A line is split into 3 parts: name, source, assert result
        for line in lines:
            
            if line[0].isdigit():
                error = self.parse_single_line(line)
                CuTestList.append(error)

        return CuTestList

    def trim_expected_actual_group(self, error_line: str, exp_ass_cutest: FailedCuTest) -> FailedCuTest:
        if "expected pointer <" in error_line[2]:
            error_line[2] = error_line[2].replace("expected pointer <", "")
        else:
            error_line[2] = error_line[2].replace("expected <", "")
        error_line[2] = error_line[2].replace("> but was <", "SplitActualStringThingBading")

        # If there is a newline in the last character of the error_message
        if "\n" in error_line[2][-1]:
            error_line[2] = error_line[2].replace(">\n", "")
        else:
            error_line[2] = error_line[2].replace(">", "")

        error = error_line[2].split("SplitActualStringThingBading")

        exp_ass_cutest.test_name = error_line[0]
        exp_ass_cutest.test_src = error_line[1]
        exp_ass_cutest.expected = error[0]
        exp_ass_cutest.actual = error[1]

        return exp_ass_cutest

    def trim_single_assert_group(self, error_line: str, failed_cutest: FailedCuTest) -> FailedCuTest:
        error_line[2] = error_line[2].replace("\n", "")
        failed_cutest.expected = "true"
        failed_cutest.actual = "false"
        return failed_cutest

    def trim_function_name_group(self, error_line: str) -> str:
        error_line = error_line.split()
        return error_line[1]

    def parse_single_line(self, line: str) -> FailedCuTest:
        error_line = line.split(": ")
        test_name = self.trim_function_name_group(error_line[0])
        test_src = error_line[1]
        test_message = error_line[2]

        # fixes: expected< test: 1hest: > but was < hest : hesst>
        if len(error_line) > 3:
            error_line[2] = ": ".join(error_line[2:])

        # Just a single assert_true
        if "assert " in test_message:
            error = self.trim_single_assert_group(error_line, FailedCuTest(test_name, test_src))
            return error

        # Assert with expected and actual
        if "expected <" in test_message or "expected pointer <" in test_message and "but was <" in test_message:
            error = self.trim_expected_actual_group(error_line, FailedCuTest(test_name, test_src))
            return error
        else:
            return None
