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

char *bruteforce_wrong(int leng_arg)
{
    // char goal[22]="7759406485255323229225";
    // char goal[7]="4073446";
    int leng=leng_arg;
    char start[22]="7000000000000000000000";
    int j;    // bruteforcer
   
    int l =leng-1;    // elemento inicio
    int i=0;          // i while

    int c=leng-1; // elemento acutal
    int d=c-1; // elemento maximo

    // cuando el ultimo es tocado 10 veces se aumenta
    while(1)
    {   
        if((char)start[c]=='9'){

            start[c]='0';
            c--;
        }
        else{
            start[c]=(char)(start[c]+1);
            c=l;

        }
        
        char *crypted=second_question(start,leng_arg);
        printf("%s -> %s\n",start,crypted);
        if(strncmp(crypted,"7759406485255323229225",leng_arg)==0)
        {
            printf("FOUNDED %s\n",start);
            break;
        }
    }    
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