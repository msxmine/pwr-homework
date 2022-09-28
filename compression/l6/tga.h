#pragma once
#include "stdint.h"

struct tgaheader {
    uint8_t idlength;
    uint8_t colormaptype;
    uint8_t imgtype;
    uint16_t cmapfirstidx;
    uint16_t cmaplen;
    uint8_t cmapbpp;
    uint16_t xorgin;
    uint16_t yorgin;
    uint16_t width;
    uint16_t height;
    uint8_t bpp;
    uint8_t chanord;
};

struct image {
    struct tgaheader header;
    uint8_t* r;
    uint8_t* g;
    uint8_t* b;
    uint8_t good;
};


struct image openTga(const char* filename);
void writeTga(struct image* ret, const char outfname[]);
