#include "hamming.h"
#include <stdio.h>

int main(int argc, char* argv[]){
    if (argc != 3){
        printf("Usage: decoder <in> <out>\n");
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
    uint64_t doubleerr = 0;
    uint64_t singleerr = 0;

    uint8_t codes[2];
    while (fread(codes, 1, 2, infile)){
        uint8_t quada = hdecode(codes[0]);
        uint8_t quadb = hdecode(codes[1]);
        doubleerr += (((quada >> 5)&1) + ((quadb >> 5)&1));
        singleerr += (((quada >> 4)&1) + ((quadb >> 4)&1));
        uint8_t rbyt = ((quadb & 0b1111) << 4) | (quada & 0b1111);
        fwrite(&rbyt, 1, 1, outfile);
    }
    fclose(infile);
    fclose(outfile);
    printf("Double errors: %ld\n", doubleerr);
    printf("Single errors: %ld\n", singleerr);
    return 0;
}
