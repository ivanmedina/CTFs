#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

void leer_input(char arr[], int tam){
    printf("> ");
    if(fgets(arr, tam, stdin) == NULL){
        perror("Error al leer");
        exit(0);
    }
}

void leer_entero(int* addr){
    char buf[0x10];
    leer_input(buf, 0x10);
    if(sscanf(buf, "%d", addr) != 1){
        puts("Error al leer entero");
    }
}

int menu(){
    puts("[*] Menu");
    puts("1. Configurar tamaño del mensaje");
    puts("2. Configurar lineas a usar para mostrar el mensaje");
    puts("3. Escribir mensaje");
    puts("4. Salir");
    int op = -1;
    leer_entero(&op);
    return op;
}

void init_buffers(){
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

void win(){
    system("/bin/sh");
}

int main(){
    init_buffers();

    volatile int tam = 0x10;
    volatile short int lineas = 1;
    volatile int tmp, op = -1;
    volatile char mensaje[0x100];

    while((op = menu()) != 4){
        switch(op){
            case 1:
                puts("Ingresa el tamaño del mensaje");
                leer_entero(&tmp);
                if(tmp > 0x100) tmp = 0x100;
                tam = tmp;
                break;
            case 2:
                puts("Ingresa la cantidad de lineas a usar para el mensaje");
                leer_entero(&lineas);
                if(lineas < 0){
                    puts("No se permiten negativos");
                    exit(0);
                }
                break;
            case 3:
                puts("Ingresa el mensaje");
                leer_input(mensaje, tam);
                if(tam % lineas != 0){
                    puts("Este mensaje no se puede formatear");
                }else{
                    puts("Enviando...");
                }
                puts("[TODO] Enviar el mensaje por red.");
                break;
        }
    }
    return 0;
}
