#include "channelpredictor.h"
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>

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

double bits(double pa){
    if (pa <= 0.0){
        return 0.0;
    }
    return -log2(pa);
}

int main(int argc, char* argv[]){
    if (argc < 2){
        fprintf(stderr, "bad arguments\n");
        return 1;
    }
    FILE* tgafile = fopen(argv[1], "rb");
    if (tgafile == NULL){
        fprintf(stderr, "Bad file\n");
        return 1;
    }
    struct tgaheader fhead;
    fread(&fhead, 18, 1, tgafile);

    struct bitmap channels[3];

    for (int chanidx = 0; chanidx < 3; chanidx++){
        channels[chanidx].data = malloc(sizeof(uint8_t)*fhead.width*fhead.height);
    }

    for (uint64_t bidx = 0; bidx < fhead.width*fhead.height*3; bidx += 3){
        for (int chanidx = 0; chanidx < 3; chanidx++){
            fread(&(channels[chanidx].data[bidx/3]), 1, 1, tgafile);
        }
    }

    double entropy[9][4];
    memset(entropy, 0, sizeof(double)*9*4);
    for (int algidx = 0; algidx < 9; algidx++){
        decptr decoder = getdecoder(algidx);
        uint64_t occurences[4][256];
        memset(occurences, 0, sizeof(uint64_t)*4*256);
        for (int chanidx = 0; chanidx < 3; chanidx++){
            struct bitmap* bm = &(channels[chanidx]);
            for (uint16_t y = 0; y < fhead.height; y++){
                for (uint16_t x = 0; x < fhead.width; x++){
                    uint8_t bval = (*decoder)(bm, x, y);
                    occurences[chanidx][bval] += 1;
                    occurences[3][bval] += 1;
                }
            }

        }
        for (int chanidx = 0; chanidx < 4; chanidx++){
            for (int bv = 0; bv < 256; bv++){
                double pbv = (double)(occurences[chanidx][bv]) / (double)(fhead.width*fhead.height*(chanidx == 3 ? 3 : 1));
                entropy[algidx][chanidx] += pbv * bits(pbv);
            }
        }
    }

    char* algnames[] = {"Plik wejściowy", "Predyktor 1", "Predyktor 2", "Predyktor 3", "Predyktor 4", "Predyktor 5", "Predyktor 6", "Predyktor 7", "Nowy predyktor"};
    char* channames[] = {"Kanał 1", "Kanał 2", "Kanał 3", "Wszystkie kanały"};

    printf("Entropia\n");
    for (int algidx = 0; algidx < 9; algidx++){
        printf("%s :\n", algnames[algidx]);
        for (int chanidx = 0; chanidx < 4; chanidx++){
            printf("    %s : %f\n", channames[chanidx], entropy[algidx][chanidx]);
        }
    }

    int bestalgos[4] = {0,0,0,0};
    for (int algidx = 1; algidx < 9; algidx++){
        for (int chidx = 0; chidx < 4; chidx++){
            bestalgos[chidx] = (entropy[algidx][chidx] < entropy[bestalgos[chidx]][chidx] ? algidx : bestalgos[chidx]);
        }
    }

    for (int chidx = 0; chidx < 4; chidx++){
        printf("Najlepsza metoda dla %s to %s\n", channames[chidx], algnames[bestalgos[chidx]]);
    }

    for (int chidx = 0; chidx < 3; chidx++){
        free(channels[chidx].data);
    }

    fclose(tgafile);
    return 0;
    
}