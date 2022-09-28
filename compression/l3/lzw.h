#include <stdint.h>
#include <stdio.h>

void lzwEncode( FILE* infile, void (*pushIdx)(uint64_t));
void lzwDecode( uint64_t (*getIdx)(), FILE* outfile);
