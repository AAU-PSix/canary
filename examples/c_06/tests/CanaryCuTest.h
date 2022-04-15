#ifndef CANARY_CUTEST
#define CANARY_CUTEST

#include "CuTest.h"

CuSuite *CanarySuites() {
    CuSuite *suite = CuSuiteNew();
    return suite;
}
#endif