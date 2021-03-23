#!/usr/bin/python3
from pwn import *
#context.log_level='debug'
#context.terminal = ["terminator", "-e"]
context.terminal = ["tmux", "splitw", "-h"]
#context.terminal = ['terminator', '--tew-tab', '-x']

import time
import struct
elf = context.binary = ELF("./housebuilder")
libc = elf.libc
# =============================================================================
gs = '''
break *0x404dd6
'''
# =============================================================================

def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path)

exp=""

# =============================================================================

io = start()
#io=remote("172.19.0.2", 10102)

# =============================================================================

io.interactive()
