#include "entropystats.h"
#include <stdio.h>
#include <math.h>
#include <stdint.h>
#include <string.h>

uint64_t occur[256];
uint64_t fsize;
double entropy;

double bits(double pa){
    if (pa <= 0.0){
        return 0.0;
    }
    return -log2(pa);
}

void loadEntropyFile(FILE* entropyfile){
    memset(occur, 0, sizeof(uint64_t)*256);
    fsize = 0;
    entropy = 0.0;

    uint8_t byt;
    while(fread(&byt, 1, 1, entropyfile)){
        fsize += 1;
        occur[byt] += 1;
    }

    for (int bv = 0; bv < 256; bv++){
        double pbv = (double)(occur[bv]) / (double)(fsize);
        entropy += pbv * bits(pbv);
    }
}

double getEntropy(){
    return entropy;
}

uint64_t getSize(){
    return fsize;
}

