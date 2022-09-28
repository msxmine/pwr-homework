#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int noiseflip(double prob){
    double gen = ((double)(rand())/(double)(RAND_MAX));
    return (gen < prob ? 1 : 0);
}

int main(int argc, char* argv[]){
    srand(4);
    if (argc != 4){
        printf("Usage: noise <p> <in> <out>\n");
        return 1;
    }
    double flipprob = strtod(argv[1], NULL);
    FILE* infile = fopen(argv[2], "rb");
    if (infile == NULL){
        printf("Cannot open input file\n");
        return 1;
    }
    FILE* outfile = fopen(argv[3], "wb");
    if (outfile == NULL){
        printf("Cannot open output file\n");
        return 1;
    }
    uint8_t rbyt;
    while (fread(&rbyt, 1, 1, infile)){
        uint8_t noise = 0;
        for (int bit = 0; bit < 8; bit++){
            noise |= (noiseflip(flipprob) << bit);
        }

        rbyt ^= noise;
        fwrite(&rbyt, 1, 1, outfile);
    }
    fclose(infile);
    fclose(outfile);
    return 0;
}
