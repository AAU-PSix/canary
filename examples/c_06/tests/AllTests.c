#include <stdio.h>
#include <stdlib.h>

#include "CuTest.h"
#include "CanaryCuTest.h"
#include "../src/original.h"

void addTest(CuTest *ct) {
	int a = 0;
	int b = 0;
	
	int actual = add(a, b);
	int expected = 0;

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

void Test_CuAssertIntEquals(CuTest *ct) {
	int expected = 0;
	int actual = 2;
	CuAssertIntEquals(ct, expected, actual);
}

void Test_CuAssertDblEquals(CuTest *ct) {
	double expected = 0.0f;
	double actual = 0.2f;
	double delta = 0.1f;
	CuAssertDblEquals(ct, expected, actual, delta);
}

void Test_CuAssertTrue(CuTest *ct) {
	CuAssertTrue(ct, 0);
}

void Test_CuAssertPtrEquals(CuTest *ct) {
	void *expected = malloc(1);
	void *actual = malloc(1);
	CuAssertPtrEquals(ct, expected, actual);
}

void Test_CuAssertStrEquals(CuTest *ct) {
	char *str1 = "123";
	char *str2 = "32";
	CuAssertStrEquals(ct, str1, str2);
}

CuSuite *CuTestSuite() {
	CuSuite *suite = CuSuiteNew();
	SUITE_ADD_TEST(suite, Test_CuAssertIntEquals);
	SUITE_ADD_TEST(suite, Test_CuAssertDblEquals);
	SUITE_ADD_TEST(suite, Test_CuAssertTrue);
	SUITE_ADD_TEST(suite, Test_CuAssertPtrEquals);
	SUITE_ADD_TEST(suite, Test_CuAssertStrEquals);
	return suite;
}

void RunAllTests(void) {
	CuString *output = CuStringNew();
	CuSuite* suite = CuSuiteNew();

	CuSuiteAddSuite(suite, AddSuite());
	// CuSuiteAddSuite(suite, CuTestSuite());
	CuSuiteAddSuite(suite, CanarySuites());

	CuSuiteRun(suite);
	CuSuiteSummary(suite, output);
	CuSuiteDetails(suite, output);
	printf("%s\n", output->buffer);
}

int main(void) {
	RunAllTests();
}
