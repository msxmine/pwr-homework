#include <stdio.h>
#include <string.h>
#include <math.h>

struct fbuf {
    FILE* file;
    unsigned char byte;
    int bitsready;
};

unsigned long allbyteswritten = 0;

struct fbuf readyBuf(const char filename[]){
    struct fbuf newbuf;
    newbuf.bitsready = 0;
    newbuf.byte = 0;
    newbuf.file = fopen(filename, "wb");
    return newbuf;
}

unsigned long codedbits = 0;
int countcodebits = 1;
void pushbit(struct fbuf* buf, const int bit){
    if (countcodebits){
        codedbits += 1;
    }

    buf->byte <<= 1;
    if (bit){
        buf->byte += 1;
    }
    buf->bitsready += 1;

    if (buf->bitsready == 8){
        allbyteswritten += 1;
        fwrite(&(buf->byte), 1, 1, buf->file);
        buf->bitsready = 0;
    }
}

void finalizebuf(struct fbuf* buf, unsigned long last, unsigned long counter){
    const unsigned long lastbit = (__UINT64_MAX__ >> 1) + 1;
    for (int i = 0; i < 64; i++){
        int curbit = ((last&lastbit) ? 1 : 0);
        pushbit(buf, curbit);
        while (counter > 0){
            pushbit(buf, !curbit);
            counter -= 1;
        }
        last <<= 1;
    }
    countcodebits = 0;
    while(buf->bitsready != 0){
        pushbit(buf, 0);
    }
    fclose(buf->file);
}

const unsigned long half = (__UINT64_MAX__ >> 1) + 1;
const unsigned long oneforth = half >> 1;
const unsigned long threeforth = half + oneforth;

unsigned long alloccur = 256;
unsigned long occurences[256];
unsigned long prob[256];
unsigned long lower[257] = {0};

unsigned long lb = 0;
unsigned long ub = __UINT64_MAX__;

void updatebounds(){
    lower[0] = lb;
    for (int i = 0; i < 256; i++){
        prob[i] = ((ub-lb)/alloccur)*occurences[i];
        lower[i+1] = lower[i] + prob[i];
    }
}

int main(int argc, char* argv[]){

    if (argc != 3){
        printf("Usage: ./compress <infile> <outfile>\n");
        return 1;
    }

    const char* infilename = argv[1];
    const char* outfilename = argv[2];

    FILE* infile = fopen(infilename, "rb");
    if (infile == NULL){
        printf("Couldn't open input file\n");
        return 1;
    }
    fseek(infile, 0, SEEK_END);
    long infilesize = ftell(infile);
    fseek(infile, 0, SEEK_SET);

    struct fbuf outf = readyBuf(outfilename);
    allbyteswritten += sizeof(infilesize);
    fwrite(&infilesize, sizeof(infilesize), 1, outf.file);

    for (int i = 0; i < 256; i++){
        occurences[i] = 1;
    }
    updatebounds();

    unsigned long counter = 0;
    unsigned char curch = 0;
    while (fread(&curch, 1, 1, infile)){
        lb = lower[curch];
        ub = lower[curch+1];

        while (((ub&half) == (lb&half)) || (lb >= oneforth && ub <= threeforth)){
            if ((ub&half) == (lb&half)){
                int bittopush = ((ub&half) ? 1 : 0);
                pushbit(&outf, bittopush);
                for (int i = 0; i < counter; i++){
                    pushbit(&outf, !bittopush);
                }
                ub <<= 1;
                lb <<= 1;
                counter = 0;
            } else {
                ub <<= 1;
                lb <<= 1;
                ub -= half;
                lb -= half;
                counter += 1;
            }
        }

        alloccur += 1;
        occurences[curch] += 1;
        updatebounds();
    }

    fclose(infile);
    finalizebuf(&outf, (lb/2)+(ub/2), counter);

    if (alloccur > 256){
        double totalentropy = 0.0;
        for (int fbyt = 0; fbyt < 256; fbyt++){
            double sprob = ((double)(occurences[fbyt]-1) / (double)(alloccur-256));
            if (sprob > 0.0){
                totalentropy += (sprob * (-log2(sprob)));
            }
        }
        printf("Entropia: %f\n", totalentropy);
        printf("Srednia dlugosc kodu: %f\n", (double)(codedbits)/(double)(alloccur-256));
        printf("Stopien kompresji %f%%\n", (((double)(allbyteswritten)/(double)(infilesize))-1.0)*(-100.0));
    }

    return 0;
}
