#include <stdio.h>

#include "CuTest.h"
#include "CanaryCuTest.h"
#include "../src/original.h"

void addTest(CuTest *ct) {
	int a = 0;
	int b = 1;
	
	int actual = add(a, b);
	int expected = 1;

	CuAssertIntEquals(ct, expected, actual);
}

void addTest_1_1(CuTest *ct) {
	int a = 3;
	int b = 9;
	
	int actual = add(a, b);
	int expected = 12;

	CuAssertIntEquals(ct, expected, actual);
}

CuSuite *AddSuite() {
	CuSuite *suite = CuSuiteNew();
	SUITE_ADD_TEST(suite, addTest);
	SUITE_ADD_TEST(suite, addTest_1_1);
	return suite;
}

void RunAllTests(void) {
	CuString *output = CuStringNew();
	CuSuite* suite = CuSuiteNew();

	CuSuiteAddSuite(suite, AddSuite());
	CuSuiteAddSuite(suite, CanarySuites());

	CuSuiteRun(suite);
	CuSuiteSummary(suite, output);
	CuSuiteDetails(suite, output);
	printf("%s\n", output->buffer);
}

int main(void) {
	RunAllTests();
}
