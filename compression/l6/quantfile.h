#include <stdint.h>
#include "tga.h"

struct quantfile {
    struct tgaheader tgh;
    uint8_t databits;
    uint8_t channels;
    uint16_t** quantreps;
    uint16_t** quantdata;
};

void writeQuantFile(struct quantfile* qf, const char* filename);
void writequantarray(FILE* io, int bits, uint16_t* data, size_t len);
struct quantfile readQuantFile(const char* filename);
void readquantarray(FILE* io, int bits, uint16_t* data, size_t len);
