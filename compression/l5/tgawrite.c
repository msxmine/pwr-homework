#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "tga.h"

void writeTga(struct image* ret, const char outfname[]){
    FILE* tfile = fopen(outfname, "wb");

    fwrite(&(ret->header.idlength), sizeof(uint8_t), 1, tfile);
    fwrite(&(ret->header.colormaptype), sizeof(uint8_t), 1, tfile);
    fwrite(&(ret->header.imgtype), sizeof(uint8_t), 1, tfile);
    fwrite(&(ret->header.cmapfirstidx), sizeof(uint16_t), 1, tfile);
    fwrite(&(ret->header.cmaplen), sizeof(uint16_t), 1, tfile);
    fwrite(&(ret->header.cmapbpp), sizeof(uint8_t), 1, tfile);
    fwrite(&(ret->header.xorgin), sizeof(uint16_t), 1, tfile);
    fwrite(&(ret->header.yorgin), sizeof(uint16_t), 1, tfile);
    fwrite(&(ret->header.width), sizeof(uint16_t), 1, tfile);
    fwrite(&(ret->header.height), sizeof(uint16_t), 1, tfile);
    fwrite(&(ret->header.bpp), sizeof(uint8_t), 1, tfile);
    fwrite(&(ret->header.chanord), sizeof(uint8_t), 1, tfile);

    fwrite(ret->data, sizeof(struct color), (ret->header.width*ret->header.height), tfile);
    fclose(tfile);
}
