#include "hamming.h"
//#include <stdio.h>

uint8_t codeQuad(uint8_t inquad){
    const uint8_t poly = 13;
    uint8_t result = 0;
    inquad %= 16;
    for (int bshift = 0; bshift < 4; bshift++){
        if ((inquad >> bshift)&1){
            result ^= (poly << bshift);
        }
    }
    int parity = 0;
    for (int bit = 0; bit < 7; bit++){
        parity ^= ((result >> bit)&1);
    }
    if (parity){
        result |= 0b10000000;
    }
    return result;
}

uint8_t decodeQuad(uint8_t codeword){
    int parity = 0;
    for (int bit = 0; bit < 8; bit++){
        parity ^= ((codeword >> bit)&1);
    }
    codeword &= 0b01111111;

    const uint8_t parpoly = 23;
    int syn = 0;
    for (int bs = 0; bs < 3; bs++){
        syn <<= 1;
        for (int bit = 7; bit > 0; bit--){
            syn ^= (((codeword >> (bit-1)) & 1) & (((parpoly << bs) >> (bit-1)) & 1));
        }
    }
    int badbit = 0;
    for (int testbit = 6; testbit >= 0; testbit--){
        int allcorrect = 1;
        for (int parbit = 0; parbit < 3; parbit++){
            if (((syn >> (2-parbit)) & 1) != (((parpoly << parbit) >> testbit ) & 1)){
                allcorrect = 0;
                break;
            }
        }
        if (!allcorrect){
            continue;
        }
        badbit = testbit + 1;
    }

    int flags = 0;
    if (badbit != 0){
        if (parity){
            //printf("Correcting bit %d\n", badbit);
            codeword ^= (1 << (badbit-1));
            flags = 1;
        } else {
            //printf("Double error!\n");
            flags = 2;
        }
    }


    const uint8_t poly = 13;
    const uint8_t plen = 4;
    uint8_t result = 0;
    uint8_t divider = (poly << (7-plen));
    for (int bit = 6; bit >= (plen-1); bit--){
        result <<= 1;
        if (codeword & (1<<bit)){
            codeword ^= divider;
            result += 1;
        }
        divider >>= 1;
    }

    result &= 0b00001111;
    result |= (flags << 4);

    return result;
}

uint8_t codelookup[16];
uint8_t decodelookup[256];
int lookupsetup = 0;

void initLookups(){
    for (int i = 0; i < 16; i++){
        codelookup[i] = codeQuad(i);
    }
    for (int i = 0; i < 256; i++){
        decodelookup[i] = decodeQuad(i);
    }
}

uint8_t hencode(uint8_t inquad){
    if (!lookupsetup){
        initLookups();
        lookupsetup = 1;
    }
    return codelookup[inquad & 0b1111];
}

uint8_t hdecode(uint8_t codepoint){
    if (!lookupsetup){
        initLookups();
        lookupsetup = 1;
    }
    return decodelookup[codepoint];
}
