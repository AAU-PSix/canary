#include "Canary.h"

int add(int a, int b) {
    // CANARY_TWEET_LOCATION("A");
    // CANARY_TWEET_VARIABLE(a, CANARY_INT_FORMAT);
    // CANARY_TWEET_STATE("a", CANARY_TYPECHECK(a), CANARY_INT_FORMAT);
    CANARY_TWEET_PRIMITIVE(a);
    return a + b;
}