#ifndef CANARY_CUTEST
#define CANARY_CUTEST

#include "CuTest.h"

#include "./test_add.h"

CuSuite *CanarySuites() {
    CuSuite *suite = CuSuiteNew();
    CuSuiteAddSuite(suite, CreateaddSuite());
    return suite;
}
#endif