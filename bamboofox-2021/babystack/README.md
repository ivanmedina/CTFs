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
![Functions](https://raw.githubusercontent.com/ivanmedina/CTFs/master/bamboofox-2021/babystack/assets/functions.png)

### Read name and token
The vulnerability is not here, but something interesting is that you can notice, that from the name you can overwrite the token, or you can just put the token you're asking for, which is deadbeef.

