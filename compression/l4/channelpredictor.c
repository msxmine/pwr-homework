#include <stdint.h>
#include "channelpredictor.h"

uint8_t acc(struct bitmap* bm, uint16_t x, uint16_t y){
    return bm->data[y*bm->width + x];
}

uint8_t jpegls1(struct bitmap* orginal, uint16_t x, uint16_t y){
    uint8_t pixa = 0;
    if (x > 0){
        pixa = acc(orginal, x-1, y);
    }
    return pixa;
}

uint8_t jpegls2(struct bitmap* orginal, uint16_t x, uint16_t y){
    uint8_t pixb = 0;
    if (y > 0){
        pixb = acc(orginal, x, y-1);
    }
    return pixb;
}

uint8_t jpegls3(struct bitmap* orginal, uint16_t x, uint16_t y){
    uint8_t pixc = 0;
    if (x > 0 && y > 0){
        pixc = acc(orginal, x-1, y-1);
    }
    return pixc;
}

uint8_t jpegls4(struct bitmap* orginal, uint16_t x, uint16_t y){
    uint8_t pixa = 0;
    if (x > 0){
        pixa = acc(orginal, x-1, y);
    }
    uint8_t pixb = 0;
    if (y > 0){
        pixb = acc(orginal, x, y-1);
    }
    uint8_t pixc = 0;
    if (x > 0 && y > 0){
        pixc = acc(orginal, x-1, y-1);
    }
    return pixa + pixb - pixc;
}

uint8_t jpegls5(struct bitmap* orginal, uint16_t x, uint16_t y){
    uint8_t pixa = 0;
    if (x > 0){
        pixa = acc(orginal, x-1, y);
    }
    uint8_t pixb = 0;
    if (y > 0){
        pixb = acc(orginal, x, y-1);
    }
    uint8_t pixc = 0;
    if (x > 0 && y > 0){
        pixc = acc(orginal, x-1, y-1);
    }
    return pixa + ((pixb - pixc)/2);
}

uint8_t jpegls6(struct bitmap* orginal, uint16_t x, uint16_t y){
    uint8_t pixa = 0;
    if (x > 0){
        pixa = acc(orginal, x-1, y);
    }
    uint8_t pixb = 0;
    if (y > 0){
        pixb = acc(orginal, x, y-1);
    }
    uint8_t pixc = 0;
    if (x > 0 && y > 0){
        pixc = acc(orginal, x-1, y-1);
    }
    return pixb + ((pixa - pixc)/2);
}

uint8_t jpegls7(struct bitmap* orginal, uint16_t x, uint16_t y){
    uint8_t pixa = 0;
    if (x > 0){
        pixa = acc(orginal, x-1, y);
    }
    uint8_t pixb = 0;
    if (y > 0){
        pixb = acc(orginal, x, y-1);
    }
    return (pixa + pixb)/2;
}

uint8_t jpegls8(struct bitmap* orginal, uint16_t x, uint16_t y){
    uint8_t pixa = 0;
    if (x > 0){
        pixa = acc(orginal, x-1, y);
    }
    uint8_t pixb = 0;
    if (y > 0){
        pixb = acc(orginal, x, y-1);
    }
    uint8_t pixc = 0;
    if (x > 0 && y > 0){
        pixc = acc(orginal, x-1, y-1);
    }
    
    uint8_t maxab = (pixa > pixb ? pixa : pixb);
    uint8_t minab = (pixa < pixb ? pixa : pixb);

    if (pixc >= maxab){
        return maxab;
    }
    if (pixc <= minab){
        return minab;
    }
    return pixa + pixb - pixc;
}


decptr getdecoder(int idx){
    static decptr knownalgos[] = {acc, jpegls1, jpegls2, jpegls3, jpegls4, jpegls5, jpegls6, jpegls7, jpegls8};
    return knownalgos[idx];
}
