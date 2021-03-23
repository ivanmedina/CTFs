 #!/usr/bin/env python
from pwn import *

binf = ELF("./bad_grades")

#for key, address in binf.symbols.iteritems():
#    print key, hex(address)
# 0x400ef9    mov    edi, 0x7f

binf.asm(binf.symbols['alarm'],'ret')
binf.save('./badgrades_patched')
