#ifndef TEST_ADD
#define TEST_ADD

#include <stdio.h>
#include <stdlib.h>

#include "CuTest.h"
#include "../src/original.h"

void test_add(CuTest *ct) {
    // Arrange
    int a_0 = 116;
    int b_0 = 97;
    // Act
    CANARY_ACT(int actual = add(a_0, b_0););
    // Assert
}

CuSuite *CreateaddSuite() {
    CuSuite *suite = CuSuiteNew();
    SUITE_ADD_TEST(suite, test_add);
    return suite;
}
#endif