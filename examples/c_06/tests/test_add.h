#ifndef TEST_ADD
#define TEST_ADD

#include <stdio.h>
#include <stdlib.h>

#include "CuTest.h"
#include "../src/original.h"

void test_add(CuTest *ct) {
    // Arrange
    int a_0 = 71;
    int b_0 = -102;
    // Act
    int actual = add(a_0, b_0);
    // Assert
}

CuSuite *CreateAddSuite() {
    CuSuite *suite = CuSuiteNew();
    SUITE_ADD_TEST(suite, test_add);
    return suite;
}
#endif