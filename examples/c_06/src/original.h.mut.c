#ifndef ORIGINAL
#define ORIGINAL

#include "Canary.h"

int add(int a, int b) {CANARY_TWEET_BEGIN_UNIT(unit);
    do {CANARY_TWEET_LOCATION(0); a=a;CANARY_TWEET_LOCATION(l); } while(0);

    while(1) {CANARY_TWEET_LOCATION(1); a=a;CANARY_TWEET_LOCATION(l); break; }
    for(;;) {CANARY_TWEET_LOCATION(3);{CANARY_TWEET_LOCATION(2);break;}}

    for (;0;) {CANARY_TWEET_LOCATION(4);a=a;}

    if (a==a) {CANARY_TWEET_LOCATION(5); a=a;CANARY_TWEET_LOCATION(l); }
    else if(b==b) {CANARY_TWEET_LOCATION(6); b=b;CANARY_TWEET_LOCATION(l); }
    else {CANARY_TWEET_LOCATION(7); b<<=b;CANARY_TWEET_LOCATION(l); }

    int sum;CANARY_TWEET_LOCATION(l);
    goto SUM;
SUM:CANARY_TWEET_LOCATION(8);
    sum = a + b;CANARY_TWEET_LOCATION(l);
    CANARY_TWEET_END_UNIT(unit);return sum;
CANARY_TWEET_END_UNIT(unit);}
#endif