#include "fileio.h"
#include <stdio.h>
#include <stdint.h>

FILE* infile = NULL;
FILE* outfile = NULL;
int readyReadBits = 0;
int readyWriteBits = 0;
uint8_t readByte = 0;
uint8_t writeByte = 0;
int endingBit = 0;

void setEndingBit(int bit){
    endingBit = bit;
}

void setInFile(FILE* f){
    infile = f;
    readyReadBits = 0;
}

void setOutFile(FILE* f){
    outfile = f;
    readyWriteBits = 0;
}

int getBit(){
    if (readyReadBits == 0){
        if (fread(&readByte, 1, 1, infile) == 0){
            return -1;
        }
        readyReadBits = 8;
    }
    int lbit = (readByte & 0x80) > 0 ? 1 : 0;
    readByte <<= 1;
    readyReadBits -= 1;
    return lbit;
}

int peekBit(){
    if (readyReadBits == 0){
        if (fread(&readByte, 1, 1, infile) == 0){
            return -1;
        }
        readyReadBits = 8;
    }
    return (readByte & 0x80) > 0 ? 1 : 0;
}

void pushBit(int bit){
    writeByte <<= 1;
    writeByte |= (bit > 0 ? 1 : 0);
    readyWriteBits += 1;
    if (readyWriteBits == 8){
        fwrite(&writeByte, 1, 1, outfile);
        readyWriteBits = 0;
    }
}

void finalizeWrite(){
    while (readyWriteBits != 0){
        pushBit(endingBit);
    }
}
