#include <stdio.h>
#include <stdbool.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <sys/ioctl.h>
#include <stdlib.h>
#include <sys/wait.h>

void clean_child(int sig){
    int status;
    int ret = 1;
    while (ret > 0){
        ret = waitpid(-1, &status, WNOHANG);
    }
}


int main(){
    signal(SIGCHLD, clean_child);
    signal(SIGTTOU, SIG_IGN);
    
    bool finished = false;
    while(!finished){
        printf("lsh $ ");
        fflush(stdout);

        char buf[10000];
        int red = read(STDIN_FILENO, buf, 9900);
        if (red <= 0){
            finished = true;
            break;
        }
        else{
            if (buf[red-1] != '\n'){
                finished = true;
                break;
            }
            else{
                buf[red-1] = '\0';
            }
        }
        
        bool background = false;
        if ( red >=2 && buf[red-2] == '&' ){
            background = true;
            buf[red-2] = '\0';
        }
        
        int argcnt = 0;
        
        char *pch;
        char *bufcopy = malloc((strlen(buf)+1) * sizeof(char));
        strcpy(bufcopy, buf);
        
        pch = strtok(bufcopy, " ");
        while (pch != NULL){
            argcnt++;
            pch = strtok(NULL, " ");
        }
        
        char **args;
        args = malloc((argcnt+1) * sizeof(char*));
        args[argcnt] = NULL;
        
        strcpy(bufcopy, buf);
        
        pch = strtok(bufcopy, " ");
        for (int i = 0; i < argcnt; i++){
            args[i] = malloc((strlen(pch)+1)*sizeof(char));
            strcpy(args[i], pch);
            pch = strtok(NULL, " ");
        }
        
        free(bufcopy);

        
        if(strcmp(args[0], "exit") == 0){
            finished = true;
            break;
        }
        
        if(strcmp(args[0], "cd") == 0){
            if (argcnt >= 2){
                chdir(args[1]);
            }
            continue;
        }
        
        
        int cpid = fork();
        
        if (cpid == 0){
            setpgid(0,0);
            execvp(args[0], args);
        }
        
        for (int i = 0; i < argcnt; i++){
            free(args[i]);
        }
        free(args);
        
        setpgid(cpid, 0);
        
        if (!background){
            tcsetpgrp(STDIN_FILENO, cpid);
            int status;
            waitpid(cpid, &status, 0);
            tcsetpgrp(STDIN_FILENO, getpgid(0));
        }
        
        
    }
    return 0;
}
