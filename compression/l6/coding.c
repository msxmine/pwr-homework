#include <stdint.h>
#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

//0 to 510
void calclowpass(uint8_t* databuf, uint16_t* resbuf, size_t len){
    for (size_t i = 1; i <= len; i+=2){
        uint8_t high = 0;
        if (i < len){
            high = databuf[i];
        }
        resbuf[i/2] = high + databuf[i-1];
    }
}

//0 to 510
void calchighpass(uint8_t* databuf, uint16_t* resbuf, size_t len){
    for (size_t i = 1; i <= len; i+=2){
        uint8_t high = 0;
        if (i < len){
            high = databuf[i];
        }
        resbuf[i/2] = ((255+high) - databuf[i-1]);
    }
}

void reconstructlowhigh(uint8_t* resdata, uint16_t* highdouble, uint16_t* lowdouble, size_t len){
    for (size_t i = 0; i < len; i++){
        int16_t par = ((lowdouble[i] + highdouble[i])-255);
        int16_t odd = (((lowdouble[i]+255) - highdouble[i]));
        if (par < 0){
            par = 0;
        }
        if (odd < 0){
            odd = 0;
        }
        if (par > 255*2){
            par = 255*2;
        }
        if (odd > 255*2){
            odd = 255*2;
        }
        
        resdata[i*2] = odd/2;
        resdata[(i*2)+1] = par/2;
    }
}

//0 to 1020
void diffcoding(uint16_t* inbuf, uint16_t* resbuf, size_t len){
    resbuf[0] = inbuf[0];
    for (size_t i = 1; i < len; i++){
        resbuf[i] = 510 + (inbuf[i]-inbuf[i-1]);
    }
}

uint16_t* calcquantreps(uint16_t* samples, size_t len, int bits, uint16_t upperbound){
    size_t* buckets = malloc(sizeof(size_t)*upperbound);
    memset(buckets, 0, sizeof(size_t)*upperbound);
    int bracknum = (1<<bits);
    uint16_t* boundries = malloc(sizeof(uint16_t)*(bracknum+1));
    double* reps = malloc(sizeof(double)*(bracknum));
    uint16_t* intreps = malloc(sizeof(uint16_t)*(bracknum+1));
    
    for (size_t i = 0; i < len; i++){
        int16_t curelem = samples[i];
        buckets[curelem] += 1;
    }

    for (size_t i = 0; i < upperbound; i++){
        buckets[i] += 1;
    }

    int bunilen = upperbound / bracknum;
    for (int i = 0; i < bracknum; i++){
        boundries[i] = (i*bunilen);
    }
    boundries[bracknum] = upperbound;

    //Lloyd-max
    for (int runi = 0; runi < 1000; runi++){

        for (int i = 0; i < bracknum; i++){
            uint64_t upper = 0;
            uint64_t lower = 0;
            for (int coord = boundries[i]; coord < boundries[i+1]; coord++){
                upper += (buckets[coord]*coord);
                lower += buckets[coord];
            }
            reps[i] = (double)upper/(double)lower;
            reps[i] = reps[i] > 0.0 ? reps[i] : 0.0;
            reps[i] = reps[i] < (double)upperbound ? reps[i] : (double)upperbound;
        }

        for (int i = 0; i < bracknum; i++){
            intreps[i] = lrint(reps[i]);
        }

        for (int i = 1; i < bracknum; i++){
            if (intreps[i] <= intreps[i-1]){
                intreps[i] = (intreps[i-1]+1);
            }
            if (intreps[i] > upperbound){
                intreps[i] = upperbound;
            }
            boundries[i] = (intreps[i-1] + intreps[i] + 1)/2;
        }

    }

    intreps[bracknum] = upperbound;

    free(boundries);
    free(buckets);
    free(reps);
    return intreps;
}

uint16_t* quantusingreps(uint16_t* reps, uint16_t numofreps, uint16_t* samples, size_t len){
    uint16_t upperbound = reps[numofreps];
    uint16_t* buckets = malloc(sizeof(uint16_t)*upperbound);
    uint16_t* boundries = malloc(sizeof(uint16_t)*(numofreps+1));
    boundries[0] = 0;
    boundries[numofreps] = upperbound;
    for (int i = 1; i < numofreps; i++){
        boundries[i] = (reps[i-1] + reps[i] + 1)/2;
    }

    uint16_t curbracket = 0;
    for (uint16_t curval = 0; curval < upperbound; curval++){
        if ((curbracket+1) < numofreps){
            if (curval >= boundries[curbracket+1]){
                curbracket += 1;
            }
        }
        buckets[curval] = curbracket;
    }

    uint16_t* result = malloc(sizeof(uint16_t)*len);
    for (size_t idx = 0; idx < len; idx++){
        result[idx] = buckets[samples[idx]];
    }

    free(boundries);
    free(buckets);
    return result;
}

uint16_t* diffusingreps(uint16_t* reps, uint16_t numofreps, uint16_t* rawsamples, size_t len){
    uint16_t upperbound = reps[numofreps];
    uint16_t* buckets = malloc(sizeof(uint16_t)*upperbound);
    uint16_t* boundries = malloc(sizeof(uint16_t)*(numofreps+1));
    boundries[0] = 0;
    boundries[numofreps] = upperbound;
    for (int i = 1; i < numofreps; i++){
        boundries[i] = (reps[i-1] + reps[i] + 1)/2;
    }

    uint16_t curbracket = 0;
    for (uint16_t curval = 0; curval < upperbound; curval++){
        if ((curbracket+1) < numofreps){
            if (curval >= boundries[curbracket+1]){
                curbracket += 1;
            }
        }
        buckets[curval] = curbracket;
    }

    uint16_t* result = malloc(sizeof(uint16_t)*len);
    uint16_t prevcodedval = 0;
    for (size_t idx = 0; idx < len; idx++){
        uint16_t realdelta = 510+(rawsamples[idx] - prevcodedval);
        result[idx] = buckets[realdelta];
        uint16_t deltarep = reps[buckets[realdelta]];
        prevcodedval += deltarep;
        if (prevcodedval < 510){
            prevcodedval = 510;
        }
        prevcodedval -= 510;
        if (prevcodedval > 510){
            prevcodedval = 510;
        }
    }

    free(boundries);
    free(buckets);
    return result;
}

uint16_t* dequantize(uint16_t* reps, uint16_t numofreps, uint16_t* data, size_t datalen){
    uint16_t* res = malloc(sizeof(uint16_t)*datalen);
    for (size_t i = 0; i < datalen; i++){
        res[i] = reps[data[i]];
    }
    return res;
}

uint16_t* dediff(uint16_t* diffdata, size_t len){
    uint16_t* res = malloc(sizeof(uint16_t)*len);
    uint16_t prev = 0;
    for (size_t i = 0; i < len; i++){
        uint16_t cand = diffdata[i];

        cand += prev;
        if (cand < 510){
            cand = 510;
        }
        cand -= 510;
        if (cand > 510){
            cand = 510;
        }

        prev = cand;
        res[i] = cand;
    }
    return res;
}
