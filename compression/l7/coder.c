#include "hamming.h"
#include <stdio.h>

int main(int argc, char* argv[]){
    if (argc != 3){
        printf("Usage: coder <in> <out>\n");
        return 1;
    }
    FILE* infile = fopen(argv[1], "rb");
    if (infile == NULL){
        printf("Cannot open input file\n");
        return 1;
    }
    FILE* outfile = fopen(argv[2], "wb");
    if (outfile == NULL){
        printf("Cannot open output file\n");
        return 1;
    }
    uint8_t rbyt;
    while (fread(&rbyt, 1, 1, infile)){
        uint8_t codea = hencode((rbyt) & 0b1111);
        uint8_t codeb = hencode((rbyt >> 4) & 0b1111);
        fwrite(&codea, 1, 1, outfile);
        fwrite(&codeb, 1, 1, outfile);
    }
    fclose(infile);
    fclose(outfile);
    return 0;
}
