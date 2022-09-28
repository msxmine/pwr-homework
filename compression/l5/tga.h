#include "stdint.h"

struct color {
    uint8_t r;
    uint8_t g;
    uint8_t b;
};

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
    struct color* data;
    uint8_t good;
};


struct image openTga(const char* filename);
void writeTga(struct image* ret, const char outfname[]);
