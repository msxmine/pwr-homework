#include <unistd.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>

void handler(int snum, siginfo_t *info, void *ptr){
    printf("sygnal %d \n", snum);
}

int main(){
    static struct sigaction sa;
    memset(&sa, 0, sizeof(sa));
    sa.sa_sigaction = handler;
    sa.sa_flags = SA_SIGINFO;
    
    for (int i = 1; i <= 64; i++){
        int ret = sigaction(i, &sa, NULL);
        if (ret == 0){
            printf("Zarejestrowano handler sygnalu %d\n", i);
        }
        else{
            printf("Nie udalo sie zarejestrowac handlera sygnalu %d\n", i);
            perror("");
        }
    }
    
    while (1){
        sleep(999999999);
    }
    
    return 0;
}
