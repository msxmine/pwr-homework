#include "tga.h"
#include "coding.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include "quantfile.h"

int main(int argc, const char* argv[]){
    if (argc != 3){
        printf("Usage: <infile.qtga> <outfile.tga>\n");
        return 1;
    }

    struct quantfile qf = readQuantFile(argv[1]);
    uint64_t numofpix = (qf.tgh.height*qf.tgh.width);
    int bits = qf.databits;
    int numofchans = qf.channels;
    struct image output;
    memcpy(&(output.header), &(qf.tgh), sizeof(struct tgaheader));
    output.r = malloc(sizeof(uint8_t)*(numofpix));
    output.g = malloc(sizeof(uint8_t)*(numofpix));
    output.b = malloc(sizeof(uint8_t)*(numofpix));
    output.good = 1;
    uint8_t* channels[] = {output.r, output.g, output.b};


    for (int chan = 0; chan < numofchans; chan++){
        uint16_t* dec_low_diff = dequantize(qf.quantreps[chan*2], (1<<bits), qf.quantdata[chan*2], (numofpix+1)/2);
        uint16_t* dec_low = dediff(dec_low_diff, (numofpix+1)/2);
        uint16_t* dec_high = dequantize(qf.quantreps[(chan*2)+1], (1<<bits), qf.quantdata[(chan*2)+1], (numofpix+1)/2);

        uint8_t* recons = malloc(sizeof(uint8_t)*(numofpix+8));
        reconstructlowhigh(recons, dec_high, dec_low, (numofpix+1)/2);
        free(dec_low_diff);
        free(dec_low);
        free(dec_high);

        memcpy(channels[chan], recons, (numofpix));
        free(recons);
    }

    writeTga(&output, argv[2]);

}
