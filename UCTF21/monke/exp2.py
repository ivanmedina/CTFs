#!/usr/bin/env python
from pwn import *
# context.terminal = ["tmux", "splitw", "-h"]
#p = process("/media/sf_UBUNTU-18/PWNING/bamboofox/babystackbabystack")
binf = ELF("./smol")
#libc=ELF("./libc-2.29.so")

#libc = ELF("libc-2.29.so")
#p = remote("chall.ctf.bamboofox.tw", 10102)
p=process('smol')

gs = '''
continue
'''

def start():
    if args.GDB:
        return gdb.debug(binf.path, gdbscript=gs)
    else:
        return process(binf.path)

context.log_level = "DEBUG"

#*******************************************************************************

syscall=0x000000000040100a

p=start()
pause()
p.sendline("A"*8+"B"*8+"C"*8+"D"*8)
p.interactive()
