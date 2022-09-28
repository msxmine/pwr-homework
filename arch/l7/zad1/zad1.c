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
    char* arg = (char*)&format + sizeof format;
    
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
                char* argstr = *((char**)arg);
                arg += sizeof(char*);
                int argstrlen = mystrlen(argstr);
                outsize += argstrlen;
                output = realloc(output, outsize);
                mystrcpy(output, argstr, outidx);
                outidx += (argstrlen-1);
            }
            if (format[idx] == 'd'){
                int argint = *((int*)arg);
                arg += sizeof(int);
                char* argstr = printbase(argint, 10);
                int argstrlen = mystrlen(argstr);
                outsize += argstrlen;
                output = realloc(output, outsize);
                mystrcpy(output, argstr, outidx);
                outidx += (argstrlen-1);
                free(argstr);
            }
            if (format[idx] == 'x'){
                int argint = *((int*)arg);
                arg += sizeof(int);
                char* argstr = printbase(argint, 16);
                int argstrlen = mystrlen(argstr);
                outsize += argstrlen;
                output = realloc(output, outsize);
                mystrcpy(output, argstr, outidx);
                outidx += (argstrlen-1);
                free(argstr);
            }
            if (format[idx] == 'b'){
                int argint = *((int*)arg);
                arg += sizeof(int);
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
    char* arg = (char*)&format + sizeof format;
    
    for (int i = 0; i < mystrlen(format); i++){
        if (format[i] == '%'){
            i++;
            if (format[i] == 's'){
                char* target = *((char**)arg);
                arg += sizeof(char*);
                
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
                int* goal = *((int**)arg);
                arg += sizeof(int*);
                
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
                int* goal = *((int**)arg);
                arg += sizeof(int*);
                
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
                int* goal = *((int**)arg);
                arg += sizeof(int*);
                
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
    myprintf("wow, to jest %s.%d", strarg2, iarg);
    
    printf("Hello\n");
    return 0;
}
