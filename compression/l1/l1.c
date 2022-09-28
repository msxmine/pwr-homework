#include <stdio.h>
#include <math.h>

unsigned long long stand[256] = {0};
unsigned long long preced[256] = {0};
unsigned long long depend[256][256] = {0};
double prob[256] = {0.0};
double probcond[256][256] = {{0.0}};

double log2(double x){
    return log(x) / log(2);
}

double bits(double pa){
    if (pa <= 0.0){
        return 0.0;
    }
    return -log2(pa);
}

int main(int argc, char* argv[]){
    if (argc < 2){
        printf("Usage: ./z1 plik\n");
        return 1;
    }

    FILE* dataf = fopen(argv[1], "rb");

    if (dataf){
        unsigned char curbyt;
        unsigned char lastbyt = 0;
        unsigned long long size = 0;
        while (fread(&curbyt, 1, 1, dataf)){
            stand[curbyt]++;
            depend[lastbyt][curbyt]++;
            preced[lastbyt]++;
            size++;
            lastbyt = curbyt;
        }
        if (size == 0){
            printf("File was empty\n");
            return 1;
        }

        for (int fbyt = 0; fbyt < 256; fbyt++){
            prob[fbyt] = (double)(stand[fbyt]) / (double)(size);
            for (int sbyt = 0; sbyt < 256; sbyt++ ){
                if (preced[fbyt] > 0){
                    probcond[fbyt][sbyt] = (double)(depend[fbyt][sbyt]) / (double)(preced[fbyt]);
                } else {
                    probcond[fbyt][sbyt] = 0.0;
                }
            }
        }

        double totalcondentropy = 0.0;
        double totalentropy = 0.0;
        for (int fbyt = 0; fbyt < 256; fbyt++){
            double thispref = 0.0;
            for (int sbyt = 0; sbyt < 256; sbyt++){
                thispref += (probcond[fbyt][sbyt] * bits(probcond[fbyt][sbyt]));
            }
            totalcondentropy += thispref * prob[fbyt];
            totalentropy += prob[fbyt] * bits(prob[fbyt]);
        }

        fprintf(stderr, "Entropia:\n");
        printf("%lf\n", totalentropy);
        fprintf(stderr, "Entropia warunkowa:\n");
        printf("%lf\n", totalcondentropy);
        fprintf(stderr, "Roznica:\n");
        printf("%lf\n", totalentropy - totalcondentropy);
        return 0;

    } else {
        printf("Could not open target file\n");
        return 1;
    }
}
