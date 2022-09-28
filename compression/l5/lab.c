#include "tga.h"
#include "lbgcluster.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

int main(int argc, const char* argv[]){
    if (argc != 4){
        printf("Usage: <infile.tga> <outfile.tga> <bits per pixel>\n");
        return 1;
    }
    uint64_t bpc = strtol(argv[3], NULL, 0);
    bpc = (1 << bpc);

    struct image intga = openTga(argv[1]);
    if (intga.good == 0){
        printf("Could not open tga\n");
        return 1;
    }
    struct lbgdata runner = initLbg(&intga, bpc);
    runLbg(&runner);

    double mse = 0.0;
    double snr = 0.0;

    for (int x = 0; x < (runner.img->header.width); x++){
        for (int y = 0; y < (runner.img->header.height); y++){
            uint64_t cdist = colorDist(runner.img->data[(y*(runner.img->header.width))+x], runner.centers[runner.assignment[(y*(runner.img->header.width))+x]]);
            uint64_t ampl = runner.img->data[(y*(runner.img->header.width))+x].r + runner.img->data[(y*(runner.img->header.width))+x].g + runner.img->data[(y*(runner.img->header.width))+x].b;
            runner.img->data[(y*(runner.img->header.width))+x].r = runner.centers[runner.assignment[(y*(runner.img->header.width))+x]].r;
            runner.img->data[(y*(runner.img->header.width))+x].g = runner.centers[runner.assignment[(y*(runner.img->header.width))+x]].g;
            runner.img->data[(y*(runner.img->header.width))+x].b = runner.centers[runner.assignment[(y*(runner.img->header.width))+x]].b;
            snr += ((double)(ampl*ampl)/(double)((runner.img->header.width)*(runner.img->header.height)));
            mse += ((double)(cdist*cdist)/(double)((runner.img->header.width)*(runner.img->header.height)));
        }
    }
    snr /= mse;
    printf("MSE: %f\n", mse);
    printf("SNR: %f dB\n", 10.0*log10(snr));

    writeTga(&intga, argv[2]);
    destroyLbg(&runner);
}
