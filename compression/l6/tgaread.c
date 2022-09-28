#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "tga.h"

struct image openTga(const char* filename){
    struct image ret;
    ret.good = 0;
    ret.r = NULL;
    ret.g = NULL;
    ret.b = NULL;

    FILE* tfile = fopen(filename, "rb");
    if (tfile == NULL){
        fprintf(stderr, "No such tga file\n");
        return ret;
    }

    fread(&(ret.header.idlength), sizeof(uint8_t), 1, tfile);
    fread(&(ret.header.colormaptype), sizeof(uint8_t), 1, tfile);
    fread(&(ret.header.imgtype), sizeof(uint8_t), 1, tfile);
    fread(&(ret.header.cmapfirstidx), sizeof(uint16_t), 1, tfile);
    fread(&(ret.header.cmaplen), sizeof(uint16_t), 1, tfile);
    fread(&(ret.header.cmapbpp), sizeof(uint8_t), 1, tfile);
    fread(&(ret.header.xorgin), sizeof(uint16_t), 1, tfile);
    fread(&(ret.header.yorgin), sizeof(uint16_t), 1, tfile);
    fread(&(ret.header.width), sizeof(uint16_t), 1, tfile);
    fread(&(ret.header.height), sizeof(uint16_t), 1, tfile);
    fread(&(ret.header.bpp), sizeof(uint8_t), 1, tfile);
    fread(&(ret.header.chanord), sizeof(uint8_t), 1, tfile);

    ret.r = malloc(sizeof(uint8_t)*(ret.header.width)*(ret.header.height));
    ret.g = malloc(sizeof(uint8_t)*(ret.header.width)*(ret.header.height));
    ret.b = malloc(sizeof(uint8_t)*(ret.header.width)*(ret.header.height));
    for (size_t pix = 0; pix < (ret.header.width*ret.header.height); pix++){
        fread(&(ret.r[pix]), sizeof(uint8_t), 1, tfile);
        fread(&(ret.g[pix]), sizeof(uint8_t), 1, tfile);
        fread(&(ret.b[pix]), sizeof(uint8_t), 1, tfile);
    }

    fclose(tfile);

    ret.good = 1;
    return ret;
}

