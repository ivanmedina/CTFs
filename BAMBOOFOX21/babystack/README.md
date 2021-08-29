# BABYSTACK (Bamboofox CTF 2021)

## Files
<pre><font><b>babystack/</b></font>
├── <font><b>docker-compose.yml</b></font>
├── <font><b>Dockerfile</b></font>
├── how_to_run.txt
├── <font><b>share</b></font>
│   ├── <font><b>babystack</b></font>
│   ├── <font><b>docker-entrypoint.sh</b></font>
│   ├── exploit.py
│   ├── <font><b>flag</b></font>
│   └── run.sh
└── xinetd</pre>

## Analysis

### Checksec
<pre>(venv) root@72528c045753:/home/babystack# pwn checksec babystack
[<font><b>*</b></font>] &apos;/home/babystack/babystack&apos;
    Arch:     amd64-64-little
    RELRO:    <font>No RELRO</font>
    Stack:    <font>Canary found</font>
    NX:       <font>NX enabled</font>
    PIE:      <font>No PIE (0x400000)</font>
</pre>

### File analysis
<pre>babystack: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=dadffa47239c398fb82c5cf5d3740ab7f2029846, for GNU/Linux 3.2.0, stripped</pre>

### Libc version
(venv) root@72528c045753:/home/babystack# strings /lib/x86_64-linux-gnu/libc.so.6 | grep ubuntu
GNU C Library (Ubuntu GLIBC 2.29-0ubuntu2) stable release **version 2.29.**


## How run

https://github.com/ivanmedina/Pwning/blob/master/docker_suites/ubuntu20-pwndbg/README.md

## Explotation

### Introduction
I didnt solve this challange, the vulnerability consists in overwriting RBP for overwrite the \_read@PLT with a limited buffer space and the canary, besides uses strlen function to reserve memory in the stack, which also help to get leak, so... i have canary leak, some other leaks, and i controlled $rbp for return any address i wanted, why i didnt solved it?... Well, didn't know where to jump, -System, yes, but the binary is dynamically linked and i just have a few directions in PLT, so I waited for the writeups to see what found, and I found two types of solutions, one involves bruteforce and other didnt not, basically the latter took advantage of the stack leaks, some binary gadgets to get a leak from the libc base and I liked it more... so the report i studied (especially this part of rop to leak the libc address) is next: (https://katolik-xixon.tistory.com/272), well, so let's get started.

### Functions
![Functions](https://raw.githubusercontent.com/ivanmedina/CTFs/master/BAMBOOFOX21/babystack/assets/functions.png)

### Main
![Main](https://raw.githubusercontent.com/ivanmedina/CTFs/master/BAMBOOFOX21/babystack/assets/main.png)

### Read name
The vulnerability is not here, but something interesting is that you can notice, that from the name you can overwrite the token, or you can just put the token you're asking for, which is deadbeef.

![read_name_token](https://raw.githubusercontent.com/ivanmedina/CTFs/master/BAMBOOFOX21/babystack/assets/read_name.png)

### Read token

![read_token](https://raw.githubusercontent.com/ivanmedina/CTFs/master/BAMBOOFOX21/babystack/assets/read_token.png)

### Name and token in the stack

![token_stack](https://raw.githubusercontent.com/ivanmedina/CTFs/master/BAMBOOFOX21/babystack/assets/name_tkn_enviado.png)

### Read strings

![read_strings](https://github.com/ivanmedina/CTFs/blob/master/BAMBOOFOX21/babystack/assets/decompiled_read_strs.png)
 
 ### ROUND 1 
 
 This is where most interesting things happen, because if we send information without cutting the line with pwntools sendline, strlen will give me the amount of bytes that it has as a parameter, from here that spits out so many leaks, and the first of them is the canary and a nice stack leak, which will serve us move in the stack...
 
 ![leaking_canary](https://raw.githubusercontent.com/ivanmedina/CTFs/master/BAMBOOFOX21/babystack/assets/how_leaked_1.png)
 
 ![leaked_canary](https://raw.githubusercontent.com/ivanmedina/CTFs/master/BAMBOOFOX21/babystack/assets/leaks_1.png)
 
### ROUND 2

![round2](https://raw.githubusercontent.com/ivanmedina/CTFs/master/BAMBOOFOX21/babystack/assets/round2.png)

![round2stack](https://raw.githubusercontent.com/ivanmedina/CTFs/master/BAMBOOFOX21/babystack/assets/reallycanarytooverwriteread.png)

![round2overwrite](https://raw.githubusercontent.com/ivanmedina/CTFs/master/BAMBOOFOX21/babystack/assets/overwriteRBP1.png)

### ROUND 3 (starting get libc leak)

Here the rop used is crafted with the binaries gadgets and some additions and subtractions from the stack leaks, with puts function we can know the libc base and use one_gadget.

![round3](https://raw.githubusercontent.com/ivanmedina/CTFs/master/BAMBOOFOX21/babystack/assets/leak_libc.png)

### FINAL ROUND

And send the last payload with the master gadget and get shell...

![win](https://raw.githubusercontent.com/ivanmedina/CTFs/master/BAMBOOFOX21/babystack/assets/win.png)




