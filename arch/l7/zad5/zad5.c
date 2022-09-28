#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void test(int a, ...){
    char* arg = (char*)&a + sizeof a;
    
    char* jed = (char*)arg;
    arg += 4;
    char* dwa = (char*)arg;
    arg += 4;

    printf("%p %p %p\n",&a, jed, dwa);
}

void addrtest(int a, int b, int c){
    printf("%p %p %p \n", &a, &b , &c);
}

char symbol(int num){
    if (num <= 9){
        return '0' + num;
    }
    else{
        return 'a' + (num - 10);
    }
}

int digit(char in){
    if (in <= '9'){
        return (in - '0');
    }
    else{
        return (in - 'a') + 10;
    }
}

int mystrlen(char* in){
    int ret = 0;
    while(1){
        if (in[ret] == '\0'){
            return ret;
        }
        ret++;
    }
}

char* printbase(int num, int base){
    int maxpow = 1;
    int comp = base;
    while (comp <= num){
        comp *= base;
        maxpow++;
    }
    
    char* result = malloc(sizeof(char) * (maxpow + 1));
    
    result[maxpow] = '\0';
    
    
    int charidx = maxpow-1;
    int lowcmp = 1;
    while (charidx >= 0){
        result[charidx] = symbol( (num/lowcmp)%(base));
        lowcmp *= base;
        charidx--;
    }
    
    return result;
    
    
}

int scanbase(char* str, int base){
    int maxpow = mystrlen(str);
    
    int res = 0;
    int pow = 1;
    for (int i = maxpow-1; i >= 0; i--){
        res += pow*digit(str[i]);
        pow *= base;
    }
    return res;
}

void mystrcpy(char* into, char* from, int offset){
    int copylen = mystrlen(from);
    for (int i = offset; i < offset+copylen; i++){
        into[i] = from[i-offset];
    }
}


void myprintf(char* format, ...){
    //rdi, rsi, rdx, rcx, r8, r9
    
    register long rdi asm ("rdi");
    register long rsi asm ("rsi");
    register long rdx asm ("rdx");
    register long rcx asm ("rcx");
    register long r8 asm ("r8");
    register long r9 asm ("r9");
    register long rbp asm ("rbp");
    long long int rdi_saved = rdi;
    long long int rsi_saved = rsi;
    long long int rdx_saved = rdx;
    long long int rcx_saved = rcx;
    long long int r8_saved = r8;
    long long int r9_saved = r9;
    long long int rbp_saved = rbp;
    
    
    char* arg = (char*)rbp_saved;
    arg += sizeof(void *); //16-byte align (call pushes rip, calee pushes rbp/return address)
    arg += sizeof(void *);
    
    int argnum = 1;
    
    int outsize = sizeof(char) * (mystrlen(format) + 1);
    char* output = malloc(outsize);
    
    int idx = 0;
    int outidx = 0;
    while (1){
        output[outidx] = format[idx];
        if (format[idx] == '\0'){
            break;
        }
        if (format[idx] == '%'){
            idx++;
            if (format[idx] == 's'){
                char* argstr;
                argnum++;
                if (argnum == 1){
                    argstr = (char*)rdi_saved;
                }
                if (argnum == 2){
                    argstr = (char*)rsi_saved;
                }
                if (argnum == 3){
                    argstr = (char*)rdx_saved;
                }
                if (argnum == 4){
                    argstr = (char*)rcx_saved;
                }
                if (argnum == 5){
                    argstr = (char*)r8_saved;
                }
                if (argnum == 6){
                    argstr = (char*)r9_saved;
                }
                if (argnum > 6){
                    argstr = *((char**)arg);
                    arg += sizeof(char*);
                }
                int argstrlen = mystrlen(argstr);
                outsize += argstrlen;
                output = realloc(output, outsize);
                mystrcpy(output, argstr, outidx);
                outidx += (argstrlen-1);
            }
            if (format[idx] == 'd'){
                int argint;
                argnum++;
                if (argnum == 1){
                    argint = (int)rdi_saved;
                }
                if (argnum == 2){
                    argint = (int)rsi_saved;
                }
                if (argnum == 3){
                    argint = (int)rdx_saved;
                }
                if (argnum == 4){
                    argint = (int)rcx_saved;
                }
                if (argnum == 5){
                    argint = (int)r8_saved;
                }
                if (argnum == 6){
                    argint = (int)r9_saved;
                }
                if (argnum > 6){
                    argint = *((int*)arg);
                    arg += sizeof(long long int);
                }
                char* argstr = printbase(argint, 10);
                int argstrlen = mystrlen(argstr);
                outsize += argstrlen;
                output = realloc(output, outsize);
                mystrcpy(output, argstr, outidx);
                outidx += (argstrlen-1);
                free(argstr);
            }
            if (format[idx] == 'x'){
                int argint;
                argnum++;
                if (argnum == 1){
                    argint = (int)rdi_saved;
                }
                if (argnum == 2){
                    argint = (int)rsi_saved;
                }
                if (argnum == 3){
                    argint = (int)rdx_saved;
                }
                if (argnum == 4){
                    argint = (int)rcx_saved;
                }
                if (argnum == 5){
                    argint = (int)r8_saved;
                }
                if (argnum == 6){
                    argint = (int)r9_saved;
                }
                if (argnum > 6){
                    argint = *((int*)arg);
                    arg += sizeof(long long int);
                }
                char* argstr = printbase(argint, 16);
                int argstrlen = mystrlen(argstr);
                outsize += argstrlen;
                output = realloc(output, outsize);
                mystrcpy(output, argstr, outidx);
                outidx += (argstrlen-1);
                free(argstr);
            }
            if (format[idx] == 'b'){
                int argint;
                argnum++;
                if (argnum == 1){
                    argint = (int)rdi_saved;
                }
                if (argnum == 2){
                    argint = (int)rsi_saved;
                }
                if (argnum == 3){
                    argint = (int)rdx_saved;
                }
                if (argnum == 4){
                    argint = (int)rcx_saved;
                }
                if (argnum == 5){
                    argint = (int)r8_saved;
                }
                if (argnum == 6){
                    argint = (int)r9_saved;
                }
                if (argnum > 6){
                    argint = *((int*)arg);
                    arg += sizeof(long long int);
                }
                char* argstr = printbase(argint, 2);
                int argstrlen = mystrlen(argstr);
                outsize += argstrlen;
                output = realloc(output, outsize);
                mystrcpy(output, argstr, outidx);
                outidx += (argstrlen-1);
                free(argstr);
            }
        }
        
        idx++;
        outidx++;
        
    }
    
    write(STDOUT_FILENO, output, mystrlen(output));
    free(output);
}

void myscanf(char* format, ...){
    
    register long rdi asm ("rdi");
    register long rsi asm ("rsi");
    register long rdx asm ("rdx");
    register long rcx asm ("rcx");
    register long r8 asm ("r8");
    register long r9 asm ("r9");
    register long rbp asm ("rbp");
    long long int rdi_saved = rdi;
    long long int rsi_saved = rsi;
    long long int rdx_saved = rdx;
    long long int rcx_saved = rcx;
    long long int r8_saved = r8;
    long long int r9_saved = r9;
    long long int rbp_saved = rbp;
    
    char* arg = (char*)rbp_saved;
    arg += sizeof(void *); //16-byte align (call pushes rip, calee pushes rbp/return address)
    arg += sizeof(void *);
    
    int argnum = 1;
    
    for (int i = 0; i < mystrlen(format); i++){
        if (format[i] == '%'){
            i++;
            if (format[i] == 's'){
                char* target;
                argnum++;
                if (argnum == 1){
                    target = (char*)rdi_saved;
                }
                if (argnum == 2){
                    target = (char*)rsi_saved;
                }
                if (argnum == 3){
                    target = (char*)rdx_saved;
                }
                if (argnum == 4){
                    target = (char*)rcx_saved;
                }
                if (argnum == 5){
                    target = (char*)r8_saved;
                }
                if (argnum == 6){
                    target = (char*)r9_saved;
                }
                if (argnum > 6){
                    target = *((char**)arg);
                    arg += sizeof(char*);
                }
                
                
                int idx = 0;
                
                char red;
                while (read(STDIN_FILENO, &red, 1) > 0){
                    if (red != ' '  && red != '\n'){
                        target[idx] = red;
                        idx++;
                        break;
                    }
                }
                while (read(STDIN_FILENO, &red, 1) > 0){
                    if (red == ' '  || red == '\n'){
                        break;
                    }
                    target[idx] = red;
                    idx++;
                }
                target[idx] = '\0';
            }
            if (format[i] == 'd'){
                int* goal;
                argnum++;
                if (argnum == 1){
                    goal = (int*)rdi_saved;
                }
                if (argnum == 2){
                    goal = (int*)rsi_saved;
                }
                if (argnum == 3){
                    goal = (int*)rdx_saved;
                }
                if (argnum == 4){
                    goal = (int*)rcx_saved;
                }
                if (argnum == 5){
                    goal = (int*)r8_saved;
                }
                if (argnum == 6){
                    goal = (int*)r9_saved;
                }
                if (argnum > 6){
                    goal = *((int**)arg);
                    arg += sizeof(int*);
                }
                
                
                char* target = malloc(sizeof(char) * 10);
                int idx = 0;
                char red;
                while (read(STDIN_FILENO, &red, 1) > 0){
                    if (red != ' '  && red != '\n'){
                        target[idx] = red;
                        idx++;
                        break;
                    }
                }
                while (read(STDIN_FILENO, &red, 1) > 0){
                    if (red == ' '  || red == '\n'){
                        break;
                    }
                    target[idx] = red;
                    idx++;
                    target = realloc(target, sizeof(char) * (10+idx));
                }
                target[idx] = '\0';
                *goal = scanbase(target, 10);
                free(target);
                
            }
            if (format[i] == 'x'){
                int* goal;
                argnum++;
                if (argnum == 1){
                    goal = (int*)rdi_saved;
                }
                if (argnum == 2){
                    goal = (int*)rsi_saved;
                }
                if (argnum == 3){
                    goal = (int*)rdx_saved;
                }
                if (argnum == 4){
                    goal = (int*)rcx_saved;
                }
                if (argnum == 5){
                    goal = (int*)r8_saved;
                }
                if (argnum == 6){
                    goal = (int*)r9_saved;
                }
                if (argnum > 6){
                    goal = *((int**)arg);
                    arg += sizeof(int*);
                }
                
                char* target = malloc(sizeof(char) * 10);
                int idx = 0;
                char red;
                while (read(STDIN_FILENO, &red, 1) > 0){
                    if (red != ' '  && red != '\n'){
                        target[idx] = red;
                        idx++;
                        break;
                    }
                }
                while (read(STDIN_FILENO, &red, 1) > 0){
                    if (red == ' '  || red == '\n'){
                        break;
                    }
                    target[idx] = red;
                    idx++;
                    target = realloc(target, sizeof(char) * (10+idx));
                }
                target[idx] = '\0';
                *goal = scanbase(target, 16);
                free(target);
            }
            if (format[i] == 'b'){
                int* goal;
                argnum++;
                if (argnum == 1){
                    goal = (int*)rdi_saved;
                }
                if (argnum == 2){
                    goal = (int*)rsi_saved;
                }
                if (argnum == 3){
                    goal = (int*)rdx_saved;
                }
                if (argnum == 4){
                    goal = (int*)rcx_saved;
                }
                if (argnum == 5){
                    goal = (int*)r8_saved;
                }
                if (argnum == 6){
                    goal = (int*)r9_saved;
                }
                if (argnum > 6){
                    goal = *((int**)arg);
                    arg += sizeof(int*);
                }
                
                char* target = malloc(sizeof(char) * 10);
                int idx = 0;
                char red;
                while (read(STDIN_FILENO, &red, 1) > 0){
                    if (red != ' '  && red != '\n'){
                        target[idx] = red;
                        idx++;
                        break;
                    }
                }
                while (read(STDIN_FILENO, &red, 1) > 0){
                    if (red == ' '  || red == '\n'){
                        break;
                    }
                    target[idx] = red;
                    idx++;
                    target = realloc(target, sizeof(char) * (10+idx));
                }
                target[idx] = '\0';
                *goal = scanbase(target, 2);
                free(target);
            }
        }
    }
    
}



int main(){
    //addrtest(9,8,6);
    //test(2, 69, 420);
    
    //printf("%s \n", printbase(255, 2));
    //printf("%d \n", scanbase("f3", 16));
    int iarg;
    char* strarg1[100];
    char* strarg2[100];
    myscanf("%s ugu %d bugu %s", strarg1, &iarg, strarg2);
    myprintf("a %d b %s c %d d %d %d %d %s \n", 1, strarg1, 3, iarg, 5, 6, strarg2);
    
    printf("Hello\n");
    return 0;
}
