#include <stdint.h>
#include <stdlib.h>

void calclowpass(uint8_t* databuf, uint16_t* resbuf, size_t len);
void calchighpass(uint8_t* databuf, uint16_t* resbuf, size_t len);
void diffcoding(uint16_t* inbuf, uint16_t* resbuf, size_t len);
uint16_t* calcquantreps(uint16_t* samples, size_t len, int bits, uint16_t upperbound);
uint16_t* quantusingreps(uint16_t* reps, uint16_t numofreps, uint16_t* samples, size_t len);
uint16_t* diffusingreps(uint16_t* reps, uint16_t numofreps, uint16_t* rawsamples, size_t len);
uint16_t* dequantize(uint16_t* reps, uint16_t numofreps, uint16_t* data, size_t datalen);
uint16_t* dediff(uint16_t* diffdata, size_t len);
void reconstructlowhigh(uint8_t* resdata, uint16_t* highdouble, uint16_t* lowdouble, size_t len);
