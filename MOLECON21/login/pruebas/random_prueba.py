#! /usr/bin/python3
from pwn import *
from ctypes import *

leak = 1
srand_init = leak

# srand_init = u32(p64(leak)[4:])
print(">>>>>>>>>> srand_init >>>>>>>>>>>")
print(hex(srand_init))
print("<<<<<<<<<<<<<< srand_init <<<<<<")

libc = CDLL("libc.so.6")
libc.srand(srand_init)

def rand():
    return libc.rand()


print(rand())
print(rand())
