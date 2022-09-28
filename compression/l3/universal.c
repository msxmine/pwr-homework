#include "universal.h"
#include <stdint.h>
#include "fileio.h"

int unialgo = 0;

void setunialgo(int aidx){
    unialgo = aidx;
    if (aidx == 2){
        setEndingBit(1);
    } else {
        setEndingBit(0);
    }
}

void ucode(uint64_t num){
    //printf("kod: %lu\n", num);
    if (unialgo == 0){
        eliasgamma(num);
    } else if (unialgo == 1){
        eliasdelta(num);
    } else if (unialgo == 2){
        eliasomega(num);
    } else if (unialgo == 3){
        fibonacci(num);
    }
}

uint64_t udcode(){
    uint64_t token;
    if (unialgo == 0){
        token = deliasgamma();
    } else if (unialgo == 1){
        token = deliasdelta();
    } else if (unialgo == 2){
        token = deliasomega();
    } else if (unialgo == 3){
        token = dfibonacci();
    }
    //printf("dekod: %lu\n", token);
    return token;
}

void eliasgamma(uint64_t num){
    int bits[64];
    int msbidx = 0;
    for (int bidx = 0; bidx < 64; bidx++){
        bits[bidx] = num & 1;
        if (bits[bidx]){
            msbidx = bidx;
        }
        num >>= 1;
        if (num == 0){
            break;
        }
    }
    for (int i = 0; i < msbidx; i++){
        pushBit(0);
    }
    for (int i = msbidx; i >= 0; i--){
        pushBit(bits[i]);
    }
}

uint64_t deliasgamma(){
    int blen = 1;
    while(peekBit() != 1){
        if (getBit() == -1){
            return 0;
        }
        blen += 1;
    }
    uint64_t res = 0;
    for (int i = 0; i < blen; i++){
        res <<= 1;
        int newbit = getBit();
        if (newbit == -1){
            return 0;
        }
        res += newbit;
    }
    return res;
}

void eliasdelta(uint64_t num){
    int bits[64];
    int msbidx = 0;
    for (int bidx = 0; bidx < 64; bidx++){
        bits[bidx] = num & 1;
        if (bits[bidx]){
            msbidx = bidx;
        }
        num >>= 1;
        if (num == 0){
            break;
        }
    }
    eliasgamma(msbidx+1);
    for (int i = msbidx-1; i >= 0; i--){
        pushBit(bits[i]);
    }
}

uint64_t deliasdelta(){
    int blen = deliasgamma();
    if (blen == 0){
        return 0;
    }
    uint64_t res = 1;
    for (int i = 0; i < blen-1; i++){
        res <<= 1;
        int newbit = getBit();
        if (newbit == -1){
            return 0;
        }
        res += newbit;
    }
    return res;
}

void eliasomegainner(uint64_t num){
    if (num > 1){
        int bits[64];
        int msbidx = 0;
        for (int bidx = 0; bidx < 64; bidx++){
            bits[bidx] = num & 1;
            if (bits[bidx]){
                msbidx = bidx;
            }
            num >>= 1;
            if (num == 0){
                break;
            }
        }
        eliasomegainner(msbidx);
        for (int i = msbidx; i >= 0; i--){
            pushBit(bits[i]);
        }
    }
}

void eliasomega(uint64_t num){
    eliasomegainner(num);
    pushBit(0);
}

uint64_t deliasomega(){
    uint64_t n = 1;
    while (peekBit() != 0){
        uint64_t res = 0;
        for (int i = 0; i < n+1; i++){
            res <<= 1;
            int newbit = getBit();
            if (newbit == -1){
                return 0;
            }
            res += newbit;
        }
        n = res;
    }
    if (getBit() == -1){
        return 0;
    }
    return n;
}

uint64_t fibnums[199];
int fibnumsinit = 0;

void initfibnums(){
    if (fibnumsinit == 0){
        fibnumsinit = 1;
        fibnums[0] = 0;
        fibnums[1] = 1;
        fibnums[198] = 0;
        for (int i = 2; i < 198; i++){
            fibnums[i] = fibnums[i-1] + fibnums[i-2];
        }
    }
}

int getleqfibidx(uint64_t num){
    initfibnums();
    int residx = 0;
    for (int i = 1; i < 198; i++){
        if (fibnums[i] > num){
            break;
        }
        residx = i;
    }
    return residx;
}

void fibonacci(uint64_t num){
    initfibnums();
    uint8_t bits[200] = {0};
    int lbitidx = 0;
    while (num > 0){
        int lfidx = getleqfibidx(num);
        num -= fibnums[lfidx];
        bits[lfidx-2] = 1;
        lbitidx = (lfidx-2 > lbitidx ? lfidx-2 : lbitidx);
    }
    for (int i = 0; i <= lbitidx; i++){
        pushBit(bits[i]);
    }
    pushBit(1);
}

uint64_t dfibonacci(){
    initfibnums();
    int fibcnt = 2;
    int lastbit = 0;
    uint64_t result = 0;
    while (1){
        int curbit = getBit();
        if (curbit == -1){
            return 0;
        }
        if (curbit == 1){
            if (curbit == lastbit){
                break;
            }
            result += fibnums[fibcnt];
        }
        fibcnt += 1;
        lastbit = curbit;
    }
    return result;
}
