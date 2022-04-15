#ifndef ORIGINAL
#define ORIGINAL

#include "Canary.h"

int add(int a, int b) {
    do { a=a; } while(0);

    while(1) { a=a; break; }
    for(;;) break;

    for (;0;) a=a;

    if (a==a) { a=a; }
    else if(b==b) { b=b; }
    else { b=b; }

    int sum;
    goto SUM;
SUM:
    sum = a + b;
    return sum;
}
#endif