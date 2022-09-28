#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "tga.h"

struct image openTga(const char* filename){
    struct image ret;
    ret.good = 0;
    ret.data = NULL;

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

    ret.data = malloc(sizeof(struct color)*(ret.header.width)*(ret.header.height));
    fread(ret.data, sizeof(struct color), (ret.header.width*ret.header.height), tfile);

    fclose(tfile);

    ret.good = 1;
    return ret;
}

