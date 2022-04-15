#ifndef ORIGINAL
#define ORIGINAL

#include "Canary.h"

int add(int a, int b) {TWEET(0);
    do {TWEET(2); a=a; TWEET(1);} while(0);TWEET(3);

    while(1) {TWEET(4); a=a; break; TWEET(3);}TWEET(5);
    for(;;) {TWEET(8);{TWEET(6);break;TWEET(9);TWEET(7);}TWEET(7);TWEET(5);}

    for (;0;) {TWEET(11);a=a;TWEET(9);}TWEET(10);

    if (a==a) {TWEET(12); a=a; }
    else if(b==b) {TWEET(14); b=b; }
    else {TWEET(15); b=b; }TWEET(13);

    int sum;
    TWEET(16);goto SUM;
SUM:TWEET(17);
    sum = a + b;
    return sum;
}
#endif