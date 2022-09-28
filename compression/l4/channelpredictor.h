#include <stdint.h>

struct bitmap {
    uint8_t* data;
    uint16_t width;
    uint16_t height;
};

typedef uint8_t (*decptr)(struct bitmap*, uint16_t, uint16_t);


decptr getdecoder(int idx);
