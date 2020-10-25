# #cookiesandcream hackdef20
# #Ivan Medina
# #undefined
from pwn import *
from ctypes import *
libc = cdll.LoadLibrary("libc.so.6")
context.log_level = 'debug'
elf = ELF("./schlage")
# gs = '''

# break main
# '''

def start():
    if args.GDB:
        return gdb.debug(elf.path)
    else:
        return remote("chals.damctf.xyz","31932")
        # return process(elf.path)

def exec():
    p=start()
    # print(p.recvline())
    # p.sendlineafter("*** WELCOME TO THE SCHLAGE 9000 ***\n","3")
    print(p.recvuntil("Which pin would you like to open?\n"))
    p.sendline("3")
    print(p.recvuntil("Give me a number!\n"))
    p.sendline("-845500968")
    print(p.recvuntil("Which pin would you like to open?\n"))
    p.sendline("1")
    print(p.recvuntil("Number please!\n"))
    p.sendline("99")
    print(p.recvuntil("Which pin would you like to open?\n"))
    p.sendline("5")
    print(p.recvuntil("I bet you can't guess my random number!\n"))
    p.sendline("1413036362")
    print(p.recvuntil("Which pin would you like to open?\n"))
    p.sendline("2")
    print(p.recvuntil("I wonder what it means?\n"))
    numberRandom=p.recvline()
    print(numberRandom)

    libc.srand(int(numberRandom))
    r=libc.rand()
    print("[+] ",r)
    print(p.recvuntil("What's your favorite number?\n"))
    print(r)
    p.sendline(str(r))
    print(p.recvuntil("Which pin would you like to open?\n"))
    p.sendline("4")
    print(p.recvuntil("What's your favorite sentence?\n"))
    r=libc.rand()
    # p.sendline("AAAA")    
    letras=[x for x in range(65,123) if not 90<x<97]
    for x in letras:
        print(chr(x),x^r%10+65)
    p.interactive()


exec()

# 3 -845500968
# 1 99
# 5 1413036362
# 2 semilla 1602382420= 1012045404 
# 4 random 1804289383

# local_48 = local_48 +   (
#                             (int)*(char *)  (     (long)&local_38 + (long)local_44) 
#                             ^ 
#                             iVar1 % 10 + 0x41U
#                         );

#  (    (local_38 + (long)local_44)
    # ^     iVar1 % 10 + 0x41U  
#  );   1804289383  % 10 +65


#      (long)local_44) ^ iVar1 % 10 + 0x41U

    
    # 0x123 =291
    #>>> 1804289383 ^ 10 = 1804289389
    #>>> 1804289383 % 10 = 3
    # 0=48: 48 ^ 68
# def rev(a,c):     
#     b=0
#     while(a^b!=c):
#             b=b+1 
#     return(b)    


# def rev2(a,b):
#     print("fuck")
#     c=1
#     while(True):
#         if(a%c == b):
#             return(c)
#         print(c)
#         c=c+1
#     return(c)

# print(rev2(1804289383,5))

#dam{p1ck1NG_l0Ck5_w1TH_gdB}
