#include <unistd.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]){
    for (int i = 0; i < 10; i++){
        int res = kill(atoi(argv[1]), 10);
        if (res != 0){
            perror("");
        }
        usleep(1000);
    }
    return 0;
}
