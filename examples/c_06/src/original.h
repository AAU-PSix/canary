#ifndef ORIGINAL
#define ORIGINAL

#include "Canary.h"

int add(int a, int b) {
    CANARY_TWEET_PRIMITIVE(a);
    CANARY_TWEET_PRIMITIVE(b);
    if (a > b) {
        int sum = b + a;
        return sum;
    }
    int sum = a + b;
    return sum;
}
#endif