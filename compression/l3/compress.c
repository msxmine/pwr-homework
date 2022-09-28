#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "universal.h"
#include "lzw.h"
#include "fileio.h"
#include "entropystats.h"



int main(int argc, char* argv[]){
    if (argc < 3){
        printf("Usage: ./compress <infile> <outfile> [CmodeIdx]\n");
        return 1;
    }
    const char* infilename = argv[1];
    const char* outfilename = argv[2];
    int cmodeidx = 2;
    if (argc > 3){
        cmodeidx = strtol(argv[3], NULL, 10);
    }
    setunialgo(cmodeidx);

    FILE* infile = fopen(infilename, "rb");
    if (infile == NULL){
        printf("Could not open input file\n");
        return 1;
    }

    FILE* outfile = fopen(outfilename, "wb");
    setOutFile(outfile);
    lzwEncode(infile, ucode);
    finalizeWrite();
    fclose(infile);
    fclose(outfile);

    infile = fopen(infilename, "rb");
    outfile = fopen(outfilename, "rb");
    loadEntropyFile(infile);
    uint64_t inlen = getSize();
    double inentro = getEntropy();
    loadEntropyFile(outfile);
    uint64_t outlen = getSize();
    double outentro = getEntropy();
    fclose(infile);
    fclose(outfile);

    printf("Długość pliku wejściowego: %lu\n", inlen);
    printf("Długość pliku wyjściowego: %lu\n", outlen);
    printf("Stopień kompresji: %lf%%\n", (((double)(outlen) / (double)(inlen)) - 1.0) * (-100.0));
    printf("Entropia pliku wejściowego: %lf\n", inentro);
    printf("Entropia pliku wyjściowego: %lf\n", outentro);

    return 0;
}