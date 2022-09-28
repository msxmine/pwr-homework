#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

int fifosize = 5;
int lifosize = 5;

int* FIFO;
int* LIFO;

int fifofront = 0;
int fifoback = 0;

int lifoslot = 0;

void initqueues(){
    FIFO = malloc(sizeof(int)*fifosize);
    LIFO = malloc(sizeof(int)*lifosize);
}

void destroyqueues(){
    free(FIFO);
    free(LIFO);
}

bool insertFIFO(int elem){
    FIFO[fifoback] = elem;
    
    if ( (fifoback+1)%fifosize == fifofront){
        int* newaddr = realloc(FIFO, sizeof(int)*fifosize*2);
        if (newaddr == NULL){
            return false;
        }
        else{
            FIFO = newaddr;
            if (fifoback < fifofront){
                memcpy(FIFO+fifosize, FIFO, fifoback);
                fifoback = fifosize + fifoback;
            }
            fifosize = fifosize*2;
        }
    }

    fifoback = (fifoback+1)%fifosize;
    return true;

}

int getFIFO(){
    if (fifofront == fifoback){
        return -1;
    }
    else{
        return FIFO[fifofront];
    }
}

bool popFIFO(){
    if (fifofront == fifoback){
        return false;
    }
    else{
        fifofront = (fifofront+1)%fifosize;
        return true;
    }
}


bool insertLIFO(int elem){
    LIFO[lifoslot++] = elem;
    if (lifoslot == lifosize){
        int* newaddr = realloc(LIFO, sizeof(int)*lifosize*2);
        if (newaddr == NULL){
            return false;
        }
        else{
            LIFO = newaddr;
            lifosize = lifosize * 2;
        }
    }
    return true;
}

int getLIFO(){
    if (lifoslot == 0){
        return -1;
    }
    else{
        return LIFO[lifoslot-1];
    }
}

bool popLIFO(){
    if (lifoslot == 0){
        return false;
    }
    else{
        lifoslot--;
        return true;
    }
}


int main(){
    initqueues();
    for(int i = 0; i < 100; i++){
        printf("Dodaje %d do kolejek...", i);
        if (insertFIFO(i) && insertLIFO(i)){
            printf("[OK]\n");
        }
        else{
            return -1;
        }
    }
    
    for(int val = getFIFO(); val >= 0; val = getFIFO()){
        popFIFO();
        printf("FIFO odczytano %d\n", val);
    }
    
    for(int val = getLIFO(); val >= 0; val = getLIFO()){
        popLIFO();
        printf("LIFO odczytano %d\n", val);
    }
    
    
    destroyqueues();
    return 0;
}
