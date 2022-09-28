#include <stdio.h>
#include <stdlib.h>
#include "universal.h"
#include "lzw.h"
#include "fileio.h"

int main(int argc, char* argv[]){
    if (argc < 3){
        printf("Usage: ./decompress <infile> <outfile> [CmodeIdx]\n");
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
    setInFile(infile);
    lzwDecode(udcode, outfile);
    return 0;
}