#include <stdio.h>
#include <string.h>

struct fbuf {
    FILE* file;
    unsigned char byte;
    int bitsready;
};

struct fbuf readyBuf(const char filename[]){
    struct fbuf newbuf;
    newbuf.file = fopen(filename, "rb");
    newbuf.byte = 0;
    newbuf.bitsready = 0;
    return newbuf;
}

int popbit(struct fbuf* buf){
    const unsigned char firstbit = (__UINT8_MAX__ >> 1) + 1;
    if (buf->bitsready == 0){
        if (fread(&(buf->byte), 1, 1, buf->file)){
            buf->bitsready = 8;
        }
    }
    if (buf->bitsready == 0){
        printf("trash\n");
        return -1;
    }
    int retbit = (((buf->byte) & firstbit) >> 7);
    (buf->byte) <<= 1;
    (buf->bitsready) -= 1;
    return retbit;
}

unsigned long loadbuf(struct fbuf* buf){
    unsigned long startval = 0;
    for (int i = 0; i < 64; i++){
        startval <<= 1;
        int rbit = popbit(buf);
        if (rbit != -1){
            startval += rbit;
        }
    }
    return startval;
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
    for (int i = 0; i < 256; i++){
        prob[i] = ((ub-lb)/alloccur)*occurences[i];
        lower[0] = lb;
        lower[i+1] = lower[i] + prob[i];
    }
}

int main(int argc, const char* argv[]){
    if (argc != 3){
        printf("Usage: ./decompress <infile> <outfile>\n");
        return 1;
    }

    const char* infilename = argv[1];
    const char* outfilename = argv[2];

    struct fbuf inf = readyBuf(infilename);
    if (inf.file == NULL){
        printf("Couldn't open input file\n");
        return 1;
    }

    FILE* outfile = fopen(outfilename, "wb");

    unsigned long textlen = 0;
    fread(&textlen, sizeof(textlen), 1, inf.file);

    for (int i = 0; i < 256; i++){
        occurences[i] = 1;
    }
    updatebounds();

    unsigned long curval = loadbuf(&inf);

    for (int bidx = 0; bidx < textlen; bidx++){

        int gchar = 0;
        while (curval >= lower[gchar]){
            gchar += 1;
        }
        gchar -= 1;

        fwrite(&gchar, 1, 1, outfile);

        lb = lower[gchar];
        ub = lower[gchar+1];

        while (((ub&half) == (lb&half)) || (lb >= oneforth && ub <= threeforth)){
            ub <<= 1;
            lb <<= 1;
            curval <<= 1;
            curval += popbit(&inf);
            if (lb >= oneforth && ub <= threeforth){
                ub -= half;
                lb -= half;
                curval -= half;
            }
        }

        alloccur += 1;
        occurences[gchar] += 1;
        updatebounds();
    }

    fclose(inf.file);
    fclose(outfile);

    return 0;
}