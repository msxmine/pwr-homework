#include <stdio.h>
#include <stdint.h>

int main(int argc, char* argv[]){
    if (argc != 3){
        printf("Usage: check <ina> <inb>\n");
        return 1;
    }
    FILE* filea = fopen(argv[1], "rb");
    FILE* fileb = fopen(argv[2], "rb");
    if (filea == NULL || fileb == NULL){
        printf("Cannot open input file\n");
        return 1;
    }

    uint8_t byta;
    uint8_t bytb;
    uint64_t diffs = 0;
    while (fread(&byta, 1, 1, filea) && fread(&bytb, 1, 1, fileb)){
        uint8_t diffbyt = (byta ^ bytb);
        diffs += ((diffbyt & 0b11110000) ? 1 : 0);
        diffs += ((diffbyt & 0b00001111) ? 1 : 0);
    }
    fclose(filea);
    fclose(fileb);
    printf("Differences found in %lu 4-bit packets\n", diffs);
    return 0;
}
