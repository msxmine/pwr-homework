#include <stdint.h>
#include <stdio.h>
#include "tga.h"
#include "quantfile.h"
#include <stdlib.h>

struct quantfile readQuantFile(const char* filename){
    struct quantfile ret;
    FILE* io = fopen(filename, "rb");
    fread(&(ret.tgh), sizeof(struct tgaheader), 1, io);
    fread(&(ret.databits), sizeof(uint8_t), 1, io);
    fread(&(ret.channels), sizeof(uint8_t), 1, io);
    uint64_t numofpix = (ret.tgh.width)*(ret.tgh.height);
    ret.quantreps = malloc(sizeof(uint16_t*)*(ret.channels)*2);
    ret.quantdata = malloc(sizeof(uint16_t*)*(ret.channels)*2);
    for (int repidx = 0; repidx < (ret.channels*2); repidx++){
        ret.quantreps[repidx] = malloc(sizeof(uint16_t)*((1 << (ret.databits))+1));
        fread(ret.quantreps[repidx], sizeof(uint16_t), (1 << (ret.databits))+1, io);
    }
    for (int repidx = 0; repidx < (ret.channels*2); repidx++){
        ret.quantdata[repidx] = malloc(sizeof(uint16_t)*((numofpix+1)/2));
        readquantarray(io, ret.databits, ret.quantdata[repidx], (numofpix+1)/2);
    }
    fclose(io);
    return ret;
}

void writeQuantFile(struct quantfile* qf, const char* filename){
    FILE* io = fopen(filename, "wb");
    fwrite(&(qf->tgh), sizeof(struct tgaheader), 1, io);
    fwrite(&(qf->databits), sizeof(uint8_t), 1, io);
    fwrite(&(qf->channels), sizeof(uint8_t), 1, io);
    uint64_t numofpix = (qf->tgh.width)*(qf->tgh.height);
    for (int repidx = 0; repidx < (qf->channels*2); repidx++){
        uint16_t* myarr = qf->quantreps[repidx];
        fwrite(myarr, sizeof(uint16_t), (1 << (qf->databits))+1, io);
    }
    for (int repidx = 0; repidx < (qf->channels*2); repidx++){
        uint16_t* myarr = qf->quantdata[repidx];
        writequantarray(io, qf->databits, myarr, (numofpix+1)/2);
    }
    fclose(io);
}

void writequantarray(FILE* io, int bits, uint16_t* data, size_t len){
    uint8_t byte = 0;
    int readybits = 0;
    for (size_t i = 0; i < len; i++){
        for(int b = (bits-1); b >= 0; b--){
            int bit = (data[i] & (1<<b)) ? 1 : 0;
            byte <<= 1;
            byte += bit;
            readybits += 1;
            if (readybits == 8){
                fwrite(&byte, 1, 1, io);
                readybits = 0;
            }
        }
    }
    if (readybits != 0){
        byte <<= (8-readybits);
        fwrite(&byte, 1, 1, io);
    }
}

void readquantarray(FILE* io, int bits, uint16_t* data, size_t len){
    uint8_t byte = 0;
    int readybits = 0;
    for (size_t i = 0; i < len; i++){
        uint16_t var = 0;
        for(int b = (bits-1); b >= 0; b--){
            if (readybits == 0){
                fread(&byte, 1, 1, io);
                readybits = 8;
            }
            int bit = (byte & 0x80) ? 1 : 0;
            byte <<= 1;
            readybits -= 1;
            var <<= 1;
            var += bit;
        }
        data[i] = var;
    }
}
