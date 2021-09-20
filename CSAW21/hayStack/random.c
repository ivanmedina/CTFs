#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int get_random(){
    time_t t = time((time_t *)0x0);
    srand((uint)t);
    return rand() % 0x100000 & 0xffffffff;
}

int main(){
    printf("%d",get_random());
}