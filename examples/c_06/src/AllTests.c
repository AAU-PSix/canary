#include <stdio.h>

#include "CuTest.h"
#include "original.h"

void addTest(CuTest *ct) {
	int expected = 0;
	int actual = add(0, 0);
	CuAssertIntEquals(ct, expected, actual);
}

CuSuite *AddSuite() {
	CuSuite *suite = CuSuiteNew();
	SUITE_ADD_TEST(suite, addTest);
	return suite;
}

void RunAllTests(void)
{
	CuString *output = CuStringNew();
	CuSuite* suite = CuSuiteNew();

	CuSuiteAddSuite(suite, AddSuite());

	CuSuiteRun(suite);
	CuSuiteSummary(suite, output);
	CuSuiteDetails(suite, output);
	printf("%s\n", output->buffer);
}

int main(void)
{
	RunAllTests();
}
