## PWN_300 HACKDEF 2021 (QUALS)

### PROTECCIONES DEL BINARIO
```
[*] '/home/user-pwn18/Escritorio/Pwn300 (1)/300/pwn_300'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```
### DIRECCIONES DE FUNCIONES
```
FUNCION	        DIRECCION
main	        0x40137F
print_menu	    0x4012C1
read_integer    0x401270
read_text	    0x401216
```

### MAIN
![Main](https://github.com/ivanmedina/CTFs/tree/master/HACKDEF21-QUALS/sender/assets/main.png)

### PRINT_MENU
![Print_Menu](https://github.com/ivanmedina/CTFs/tree/master/HACKDEF21-QUALS/sender/assets/print_menu.png)

### READ_INTEGER
![Read_Integer](https://github.com/ivanmedina/CTFs/tree/master/HACKDEF21-QUALS/sender/assets/read_integer.png)

### READ_TEXT
![Read_Text](https://github.com/ivanmedina/CTFs/tree/master/HACKDEF21-QUALS/sender/assets/read_text.png)

### WIN
![Win](https://github.com/ivanmedina/CTFs/tree/master/HACKDEF21-QUALS/sender/assets/win.png)

### STACK
![Stack](https://github.com/ivanmedina/CTFs/tree/master/HACKDEF21-QUALS/sender/assets/stack.png)

La vulnerabilidad esta en que podemos configurar el tamaño de lineas y este numero se almacena para despues ser usado como longitud del mensaje, por lo que podemos escribir mas de los 0x118 bytes (280) para llegar al rbp y escribir en el con la direccion de win para que cuando haga el lave antes del return de la opcion 4 (salir) mueva el $RBP a $RSP y retorne a ella donde esta una funcion system('/bin/sh'), en este caso le sumamos +8 para que salte la parte en la que acomoda el stack ya que lo desalinearia, y el numero 0x11117fff que se envia como size, es por que la funcion read_integer lee 16 bytes y para el size usa una variable tipo short, la cual llega hasta al maximo de 0x7fff y el 1111 es para rellenar los demas bytes, si ponemos 0x11118000 habria un problema ya que es mas grande de lo que soporta un tipo de dato short.

Finalmente al lanzar el exploit nos regresara la shell.

![Shell](https://github.com/ivanmedina/CTFs/tree/master/HACKDEF21-QUALS/sender/assets/shell.png)