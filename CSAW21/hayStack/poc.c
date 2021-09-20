#include <stdio.h>
#include <string.h>

int funcion01(){
    int iterador=0;
    char memoria[20];

    char memoria_addr=&memoria;
    memset(memoria,'\x00',20);
    for (iterador = 0; iterador < 0x100000; iterador = iterador + 1) {
        memoria_addr = iterador+1;
        printf("%p\n",memoria_addr);
        // memoria + ((long)iterador * 4) = 0xb00;
    }
}

int main(){
    funcion01();
}