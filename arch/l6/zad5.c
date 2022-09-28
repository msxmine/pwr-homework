#include <stdio.h>
#include <stdbool.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <sys/ioctl.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <fcntl.h>


typedef struct job
{
    struct job *next;
    char *command;
    int pgid;
    int *procs;
    int numprocs;
    int id;
} job;

job *curjob;
int jobs = 0;

int getJobStatus(job *target){
    int result = 3;
    
    for (int i = 0; i < target->numprocs; i++){
        if (target->procs[(2*i)+1] < result){
            result = target->procs[(2*i)+1];
        }
    }
    
    return result;
}

void removeDeadJobs(){
    job *target;
    job *parent;
    target = curjob;
    while (target != NULL){
        if (getJobStatus(target) == 3){
            curjob = target->next;
            free(target->command);
            free(target->procs);
            free(target);
            target = curjob;
        }
        else{
            parent = target;
            target = parent->next;
            break;
        }
    }
    while (target != NULL){
        if (getJobStatus(target) == 3){
            parent->next = target->next;
            free(target->command);
            free(target->procs);
            free(target);
            target = parent->next;
        }
        else{
            parent = target;
            target = parent->next;
        }
    }
}

void updateStatus(job *target){
    int status;
    int ret = 1;
    while (ret > 0){
        ret = waitpid(-(target->pgid), &status, WNOHANG|WUNTRACED|WCONTINUED);
        if (ret > 0){
            int procidx = -1;
            for (int i = 0; i < target->numprocs; i++){
                if (target->procs[2*i] == ret){
                    procidx = i;
                }
            }
            if (procidx >= 0){
                if ( WIFEXITED(status) || WIFSIGNALED(status) ){
                    target->procs[(2*procidx)+1] = 3;
                }
                if ( WIFSTOPPED(status) ){
                    target->procs[(2*procidx)+1] = 2;
                }
                if ( WIFCONTINUED(status) ){
                    target->procs[(2*procidx)+1] = 1;
                }
            }
        }
    }
}
    
void updateStatusAll(){
    job *target;
    target = curjob;
    while (target != NULL){
        updateStatus(target);
        target = target->next;
    }
}

void clean_child(int sig){
    updateStatusAll();
}


void moveToForeground(job *target){
    tcsetpgrp(STDIN_FILENO, target->pgid);
    int status;
    int retcode = 1;
    while (retcode > 0){
        retcode = waitpid(-(target->pgid), &status, WUNTRACED | WCONTINUED);
        if (retcode > 0){
            int procidx = -1;
            for (int i = 0; i < target->numprocs; i++){
                if (target->procs[2*i] == retcode){
                    procidx = i;
                }
            }
            if (procidx >= 0){
                if ( WIFEXITED(status) || WIFSIGNALED(status) ){
                    target->procs[(2*procidx)+1] = 3;
                }
                if ( WIFSTOPPED(status) ){
                    target->procs[(2*procidx)+1] = 2;
                }
                if ( WIFCONTINUED(status) ){
                    target->procs[(2*procidx)+1] = 1;
                }
            }
            int allended = 1;
            for (int i = 0; i < target->numprocs; i++){
                if (target->procs[(2*i)+1] <= 1){
                    allended = 0;
                }
            }
            if (allended){
                break;
            }
        }
    }
    tcsetpgrp(STDIN_FILENO, getpgid(0));
}


int main(){
    curjob = NULL;
    signal(SIGCHLD, clean_child);
    signal(SIGTTOU, SIG_IGN);
    signal(SIGTSTP, SIG_IGN);
    
    char buf[10000];
    bool finished = false;
    
    
    while(!finished){
        printf("lsh $ ");
        fflush(stdout);

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
        
        signal(SIGCHLD, SIG_DFL);
        removeDeadJobs();
        
        bool background = false;
        if ( red >=2 && buf[red-2] == '&' ){
            background = true;
            buf[red-2] = '\0';
        }
        
        char *bufcopy;
        bufcopy = malloc((strlen(buf)+1) * sizeof(char));
        strcpy(bufcopy, buf);
        
        char ***commandset;
        commandset = malloc(2 * sizeof(char**));
        commandset[0] = malloc(sizeof(char*));
        commandset[0][0] = NULL;
        commandset[1] = NULL;
        int currentcommand = 0;
        int currentword = 0;
        
        
        char *fragment;
        fragment = strsep(&bufcopy, " ");
        while (fragment != NULL){
            if (strcmp(fragment, "|") == 0){
                currentcommand++;
                commandset = realloc(commandset, (currentcommand+2)*sizeof(char**));
                commandset[currentcommand+1] = NULL;
                commandset[currentcommand] = malloc(sizeof(char*));
                commandset[currentcommand][0] = NULL;
                currentword = 0;
                
            }
            else{
                commandset[currentcommand] = realloc(commandset[currentcommand], (currentword+2)*sizeof(char*));
                commandset[currentcommand][currentword] = strdup(fragment);
                currentword++;
                commandset[currentcommand][currentword] = NULL;
            }
            fragment = strsep(&bufcopy, " ");
        }
        
        free(bufcopy);
        
        if(commandset[0][0] != NULL && strcmp(commandset[0][0], "exit") == 0){
            finished = true;
            while (curjob != NULL){
                job *deljob = curjob;
                curjob = curjob->next;
                
                killpg(deljob->pgid, SIGHUP);
                free(deljob->command);
                free(deljob->procs);
                free(deljob);
            }
            
            for (int i = 0; commandset[i] != NULL; i++){
                for (int j = 0; commandset[i][j] != NULL; j++){
                    free(commandset[i][j]);
                }
                free(commandset[i]);
            }
            free(commandset);
            
            break;
        }
        
        if(commandset[0][0] != NULL && strcmp(commandset[0][0], "cd") == 0){
            if (commandset[0][1] != NULL){
                chdir(commandset[0][1]);
            }
            
            for (int i = 0; commandset[i] != NULL; i++){
                for (int j = 0; commandset[i][j] != NULL; j++){
                    free(commandset[i][j]);
                }
                free(commandset[i]);
            }
            free(commandset);
            
            signal(SIGCHLD, clean_child);
            updateStatusAll();
            continue;
        }
        
        if(commandset[0][0] != NULL && strcmp(commandset[0][0], "jobs") == 0){
            job *cur = curjob;
            while(cur != NULL){
                int jobstate = getJobStatus(cur);
                if (jobstate == 0){
                    printf("Zadanie %d, Niewystartowane, %s\n", cur->id, cur->command);
                }
                if (jobstate == 1){
                    printf("Zadanie %d, Działa, %s\n", cur->id, cur->command);
                }
                if (jobstate == 2){
                    printf("Zadanie %d, Zatrzymane, %s\n", cur->id, cur->command);
                }
                if (jobstate == 3){
                    printf("Zadanie %d, Zakończone, %s\n", cur->id, cur->command);
                }
                cur = cur->next;
            }
            
            for (int i = 0; commandset[i] != NULL; i++){
                for (int j = 0; commandset[i][j] != NULL; j++){
                    free(commandset[i][j]);
                }
                free(commandset[i]);
            }
            free(commandset);
            
            signal(SIGCHLD, clean_child);
            updateStatusAll();
            continue;
        }
        
        if(commandset[0][0] != NULL && strcmp(commandset[0][0], "bg") == 0){
            if (curjob != NULL){
                if (commandset[0][1] != NULL){
                    int sid = atoi(commandset[0][1]);
                    
                    if (curjob->id != sid){
                        job *parent = curjob;
                        job *child = curjob->next;
                        
                        while (child != NULL && child->id != sid){
                            parent = child;
                            child = child->next;
                        }
                        
                        if(child != NULL){
                            parent->next = child->next;
                            child->next = curjob;
                            curjob = child;
                        }
                    }
                }
                
                job *targetjob = curjob;
                
                killpg(targetjob->pgid, SIGCONT);
                
                
            
            }
            
            for (int i = 0; commandset[i] != NULL; i++){
                for (int j = 0; commandset[i][j] != NULL; j++){
                    free(commandset[i][j]);
                }
                free(commandset[i]);
            }
            free(commandset);
            
            signal(SIGCHLD, clean_child);
            updateStatusAll();
            continue;
        }
        
        if(commandset[0][0] != NULL && strcmp(commandset[0][0], "fg") == 0){
            if (curjob != NULL){
                if (commandset[0][1] != NULL){
                    int sid = atoi(commandset[0][1]);
                    
                    if (curjob->id != sid){
                        job *parent = curjob;
                        job *child = curjob->next;
                        
                        while (child != NULL && child->id != sid){
                            parent = child;
                            child = child->next;
                        }
                        
                        if(child != NULL){
                            parent->next = child->next;
                            child->next = curjob;
                            curjob = child;
                        }
                    }
                }
                
                job *targetjob = curjob;
                
                killpg(targetjob->pgid, SIGCONT);
                
                
            
            }
            
            for (int i = 0; commandset[i] != NULL; i++){
                for (int j = 0; commandset[i][j] != NULL; j++){
                    free(commandset[i][j]);
                }
                free(commandset[i]);
            }
            free(commandset);
            
            signal(SIGCHLD, clean_child);
            updateStatusAll();
            moveToForeground(curjob);
            continue;
        }
        
        job *newjob = malloc(sizeof(struct job));
        newjob->id = (jobs+1);
        jobs++;
        newjob->command = strdup(buf);
        
        
        int numprocesses = 0;
        for (int i = 0; commandset[i] != NULL; i++){
            numprocesses++;
        }
        newjob->numprocs = numprocesses;
        
        newjob->procs = malloc(sizeof(int)*numprocesses*2);
        memset(newjob->procs, 0, sizeof(int)*numprocesses*2);
        
        int pipefd[2];
        
        for (int cmdidx = 0; commandset[cmdidx] != NULL; cmdidx++){
            if (commandset[cmdidx][0] != NULL){
                int stdinfd = -1;
                int stdoutfd = -1;
                int stderrfd = -1;
                
                if (cmdidx > 0){
                    stdinfd = pipefd[0];
                }
                
                if (cmdidx < (numprocesses-1)){
                    pipe(pipefd);
                    stdoutfd = pipefd[1];
                }
                
                
                int wordcnt = 0;
                for (int wordidx = 0; commandset[cmdidx][wordidx] != NULL; wordidx++){
                    wordcnt++;
                }
                for (int wordidx = wordcnt-1; wordidx >= 0; wordidx--){
                    if (strcmp(commandset[cmdidx][wordidx], ">") == 0 && (wordcnt - wordidx) > 1){
                        free(commandset[cmdidx][wordidx]);
                        commandset[cmdidx][wordidx] = NULL;
                        int newfd = open(commandset[cmdidx][wordidx+1], O_WRONLY | O_CREAT, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);
                        if (newfd >= 0){
                            if (stdoutfd >= 0){
                                close(stdoutfd);
                            }
                            stdoutfd = newfd;
                        }
                        for( int i = wordidx+1; commandset[cmdidx][i] != NULL; i++){
                            free(commandset[cmdidx][i]);
                        }
                        continue;
                    }
                    if (strcmp(commandset[cmdidx][wordidx], "2>") == 0 && (wordcnt - wordidx) > 1){
                        free(commandset[cmdidx][wordidx]);
                        commandset[cmdidx][wordidx] = NULL;
                        int newfd = open(commandset[cmdidx][wordidx+1], O_WRONLY | O_CREAT, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);
                        if (newfd >= 0){
                            if (stderrfd >= 0){
                                close(stderrfd);
                            }
                            stderrfd = newfd;
                        }
                        for( int i = wordidx+1; commandset[cmdidx][i] != NULL; i++){
                            free(commandset[cmdidx][i]);
                        }
                        continue;
                    }
                    if (strcmp(commandset[cmdidx][wordidx], "<") == 0 && (wordcnt - wordidx) > 1){
                        free(commandset[cmdidx][wordidx]);
                        commandset[cmdidx][wordidx] = NULL;
                        int newfd = open(commandset[cmdidx][wordidx+1], O_RDONLY);
                        if (newfd >= 0){
                            if (stdinfd >= 0){
                                close(stdinfd);
                            }
                            stdinfd = newfd;
                        }
                        for( int i = wordidx+1; commandset[cmdidx][i] != NULL; i++){
                            free(commandset[cmdidx][i]);
                        }
                        continue;
                    }
                    
                }
                
                
                
                int cpid = fork();
                
                newjob->procs[2*cmdidx] = cpid;
                newjob->procs[(2*cmdidx)+1] = 1;
                
                
                if (cmdidx == 0){
                    newjob->pgid = cpid;
                }
                
                if (cpid == 0){
                    
                    while (curjob != NULL){
                        job *deljob = curjob;
                        curjob = curjob->next;
                        
                        free(deljob->command);
                        free(deljob->procs);
                        free(deljob);
                    }

                    signal(SIGCHLD, SIG_DFL);
                    signal(SIGTTOU, SIG_DFL);
                    signal(SIGTSTP, SIG_DFL);
                    setpgid(0,newjob->pgid);
                    
                    free(newjob->command);
                    free(newjob->procs);
                    free(newjob);

                    if (stdinfd >= 0){
                        dup2(stdinfd, STDIN_FILENO);
                        close(stdinfd);
                    }
                    if (stdoutfd >= 0){
                        dup2(stdoutfd, STDOUT_FILENO);
                        close(stdoutfd);
                    }
                    if (stderrfd >= 0){
                        dup2(stderrfd, STDERR_FILENO);
                        close(stderrfd);
                    }
                    execvp(commandset[cmdidx][0], commandset[cmdidx]);
                    exit(0);
                } 
                
                if (stdinfd >= 0){
                    close(stdinfd);
                }
                if (stdoutfd >= 0){
                    close(stdoutfd);
                }
                if (stderrfd >= 0){
                    close(stderrfd);
                }
                
                setpgid(cpid, newjob->pgid);
            }
        }
        
        newjob->next = curjob;
        curjob = newjob;
        
        signal(SIGCHLD, clean_child);
        updateStatusAll();
        
        
        for (int i = 0; commandset[i] != NULL; i++){
            for (int j = 0; commandset[i][j] != NULL; j++){
                free(commandset[i][j]);
            }
            free(commandset[i]);
        }
        free(commandset);
        
        
        if (!background){
            moveToForeground(curjob);
        }
        
        
    }
    return 0;
}
