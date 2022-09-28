#include <unistd.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>

int main(){
    int res = kill(1, 9);
    if (res != 0){
        perror("");
    }
    return 0;
}
