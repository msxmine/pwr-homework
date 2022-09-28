#include "tga.h"
#include "coding.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include "quantfile.h"

int main(int argc, const char* argv[]){
    if (argc != 4){
        printf("Usage: <infile.tga> <outfile.qtga> <bits per pixel>\n");
        return 1;
    }
    int bits = strtol(argv[3], NULL, 0);

    struct image intga = openTga(argv[1]);
    if (intga.good == 0){
        printf("Could not open tga\n");
        return 1;
    }

    uint64_t numofpix = (intga.header.width)*(intga.header.height);
    uint8_t* channels[] = {intga.r, intga.g, intga.b};
    int numofchans = 3;

    struct quantfile qf;
    memcpy(&(qf.tgh), &(intga.header), sizeof(struct tgaheader));
    qf.databits = bits;
    qf.channels = 3;
    qf.quantreps = malloc(sizeof(uint16_t*)*numofchans*2);
    qf.quantdata = malloc(sizeof(uint16_t*)*numofchans*2);

    for (int chan = 0; chan < numofchans; chan++){
        uint16_t* lowpass = malloc(sizeof(uint16_t)*numofpix);
        uint16_t* highpass = malloc(sizeof(uint16_t)*numofpix);

        calclowpass(channels[chan], lowpass, numofpix);
        calchighpass(channels[chan], highpass, numofpix);

        uint16_t* highreps = calcquantreps(highpass, (numofpix+1)/2, bits, 512);
        uint16_t* highquant = quantusingreps(highreps, (1<<bits), highpass, (numofpix+1)/2);
        free(highpass);

        uint16_t* lowrawdiff = malloc(sizeof(uint16_t)*((numofpix+1)/2));
        diffcoding(lowpass, lowrawdiff, ((numofpix+1)/2));
        uint16_t* lowreps = calcquantreps(lowrawdiff, ((numofpix+1)/2), bits, 1024);
        free(lowrawdiff);
        uint16_t* lowquant = diffusingreps(lowreps, (1<<bits), lowpass, (numofpix+1)/2);

        qf.quantreps[chan*2] = lowreps;
        qf.quantreps[(chan*2)+1] = highreps;
        qf.quantdata[chan*2] = lowquant;
        qf.quantdata[(chan*2)+1] = highquant;
    }

    writeQuantFile(&qf, argv[2]);

}
