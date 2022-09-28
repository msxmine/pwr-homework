#include "tga.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

int main(int argc, const char* argv[]){
    if (argc != 3){
        printf("Usage: <orginal.tga> <new.tga>\n");
        return 1;
    }

    struct image intgaorg = openTga(argv[1]);
    if (intgaorg.good == 0){
        printf("Could not open tga\n");
        return 1;
    }

    struct image intganew = openTga(argv[2]);
    if (intganew.good == 0){
        printf("Could not open tga\n");
        return 1;
    }

    uint8_t* orgchannels[] = {intgaorg.r, intgaorg.g, intgaorg.b};
    uint8_t* newchannels[] = {intganew.r, intganew.g, intganew.b};

    double mse = 0.0;
    double snr = 0.0;
    for (int x = 0; x < (intgaorg.header.width); x++){
        for (int y = 0; y < (intgaorg.header.height); y++){
            uint64_t pixnum = (y*(intgaorg.header.width))+x;
            uint64_t cdist = 0;
            for (int i = 0; i < 3; i++){
                cdist += abs((int)(orgchannels[i][pixnum])-(int)(newchannels[i][pixnum]));
            }
            uint64_t ampl = 0;
            for (int i = 0; i < 3; i++){
                ampl += abs((int)(newchannels[i][pixnum]));
            }
            snr += ((double)(ampl*ampl)/(double)((intgaorg.header.width)*(intgaorg.header.height)));
            mse += ((double)(cdist*cdist)/(double)((intgaorg.header.width)*(intgaorg.header.height)));
        }
    }
    snr /= mse;
    printf("MSE: %f\n", mse);
    printf("SNR: %f dB\n", 10.0*log10(snr));

    for (int chan = 0; chan < 3; chan++){
        mse = 0.0;
        snr = 0.0;
        for (int x = 0; x < (intgaorg.header.width); x++){
            for (int y = 0; y < (intgaorg.header.height); y++){
                uint64_t pixnum = (y*(intgaorg.header.width))+x;
                uint64_t cdist = 0;
                cdist += abs((int)(orgchannels[chan][pixnum])-(int)(newchannels[chan][pixnum]));
                uint64_t ampl = 0;
                ampl += abs((int)(newchannels[chan][pixnum]));

                snr += ((double)(ampl*ampl)/(double)((intgaorg.header.width)*(intgaorg.header.height)));
                mse += ((double)(cdist*cdist)/(double)((intgaorg.header.width)*(intgaorg.header.height)));
            }
        }
        snr /= mse;
        printf("[chan %d] MSE: %f\n", chan, mse);
        printf("[chan %d] SNR: %f dB\n", chan, 10.0*log10(snr));
    }

}
