#include <unistd.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>

int signalstotal = 0;

void handler(int snum, siginfo_t *info, void *ptr){
    signalstotal++;
    printf("sygnal %d , numer %d\n", snum, signalstotal);
    sleep(2);
    
}

int main(){
    static struct sigaction sa;
    memset(&sa, 0, sizeof(sa));
    sa.sa_sigaction = handler;
    sa.sa_flags = SA_SIGINFO;

    int ret = sigaction(SIGUSR1, &sa, NULL);

    
    while (1){
        sleep(999999999);
    }
    
    return 0;
}
