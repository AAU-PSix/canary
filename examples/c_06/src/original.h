#include "Canary.h"

int add(int a, int b) {
    CANARY_TWEET_PRIMITIVE(a);
    CANARY_TWEET_PRIMITIVE(b);
    return a + b;
}