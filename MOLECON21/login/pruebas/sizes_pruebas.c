#include <stdio.h>
int main() {
// # v1 = randomf();
// # v2 = (unsigned __int8)
// #      (((unsigned __int64)v1 >> 56) + v1)
// #      -
// #      ((unsigned int)(v1 >> 31) >> 24);
   unsigned __int8 x=1;
   printf("%u",x);
   return 0;
}