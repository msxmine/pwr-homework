#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "tga.h"
#include "lbgcluster.h"
#include <stdio.h>

uint64_t colorDist(struct color a, struct bigcolor b){
    return abs(a.r - b.r) + abs(a.g - b.g) + abs(a.b - b.b);
}

double* distpointcmp;
int cmpdist (const void* a, const void* b){
    return ( distpointcmp[*(uint64_t*)a] > distpointcmp[*(uint64_t*)b] ? -1 : 1);
}

int updateAssignments(struct lbgdata* lbg){
    uint64_t emptyclust = 0;
    lbg->prevdistortion = lbg->distortion;
    lbg->distortion = 0.0;

    for (uint64_t c = 0; c < lbg->curclust; c++){
        lbg->numassigned[c] = 0;
        lbg->clusterdist[c] = 0.0;
        lbg->distidxsrt[c] = c;
    }

    for (int x = 0; x < (lbg->img->header.width); x++){
        for (int y = 0; y < (lbg->img->header.height); y++){
            uint64_t pixnum = (y*(lbg->img->header.width))+x;
            uint64_t bestcid = lbg->assignment[pixnum];
            uint64_t mindist = colorDist(lbg->img->data[pixnum], lbg->centers[bestcid]);

            if (mindist != 0){
                for (uint64_t c = 0; c < lbg->curclust; c++){
                    uint64_t dist = colorDist(lbg->img->data[pixnum], lbg->centers[c]);
                    if (dist < mindist){
                        mindist = dist;
                        bestcid = c;
                    }
                }
            }

            lbg->assignment[pixnum] = bestcid;
            lbg->numassigned[bestcid] += 1;
            lbg->distortion += (mindist*mindist) / (double)((lbg->img->header.width)*(lbg->img->header.height));;
            lbg->clusterdist[bestcid] += (mindist*mindist);
        }
    }

    for (uint64_t c = 0; c < lbg->curclust; c++){
        if (lbg->numassigned[c] != 0){
            lbg->clusterdist[c] /= lbg->numassigned[c];
        }
        else {
            emptyclust++;
        }
    }

    distpointcmp = lbg->clusterdist;
    qsort(lbg->distidxsrt,lbg->curclust, sizeof(uint64_t), cmpdist);

    uint64_t firstbeeg = 0;
    for (uint64_t c = 0; c < lbg->curclust && emptyclust > 0; c++){
        if (lbg->numassigned[c] == 0){
            int found = 0;

            for (uint64_t ncsi = firstbeeg; ncsi < lbg->curclust; ncsi++){
                uint64_t nc = lbg->distidxsrt[ncsi];
                if (lbg->numassigned[nc] > 1){
                    firstbeeg = ncsi;
                    found = 1;
                    break;
                }
            }

            if (!found){
                firstbeeg = lbg->curclust;
                return 1;
            }

            int broken = 0;
            uint64_t point = 0;
            uint64_t targetclust = lbg->distidxsrt[firstbeeg];
            for (int x = 0; x < (lbg->img->header.width); x++){
                for (int y = 0; y < (lbg->img->header.height); y++){
                    point = (y*(lbg->img->header.width))+x;
                    uint64_t mycluster = lbg->assignment[point];
                    if (mycluster == targetclust){
                        lbg->numassigned[mycluster] -= 1;
                        lbg->assignment[point] = c;
                        lbg->numassigned[c] = 1;
                        emptyclust -= 1;
                        broken = 1;
                        break;
                    }
                }
                if (broken){
                    break;
                }
            }


            lbg->centers[c].r = lbg->img->data[point].r;
            lbg->centers[c].g = lbg->img->data[point].g;
            lbg->centers[c].b = lbg->img->data[point].b;

        }
    }

    return 0;

}

void updateCenters(struct lbgdata* lbg){
    for (uint64_t c = 0; c < lbg->curclust; c++){
        lbg->centers[c].r = 0;
        lbg->centers[c].g = 0;
        lbg->centers[c].b = 0;
    }

    for (int x = 0; x < (lbg->img->header.width); x++){
        for (int y = 0; y < (lbg->img->header.height); y++){
            uint64_t pixnum = (y*(lbg->img->header.width))+x;
            uint64_t mycluster = lbg->assignment[pixnum];
            lbg->centers[mycluster].r += lbg->img->data[pixnum].r;
            lbg->centers[mycluster].g += lbg->img->data[pixnum].g;
            lbg->centers[mycluster].b += lbg->img->data[pixnum].b;
        }
    }

    for (uint64_t c = 0; c < lbg->curclust; c++){
        if (lbg->numassigned[c] > 0){
            lbg->centers[c].r /= lbg->numassigned[c];
            lbg->centers[c].g /= lbg->numassigned[c];
            lbg->centers[c].b /= lbg->numassigned[c];
        }
    }
}

void runLbg(struct lbgdata* lbg){
    while (lbg->curclust < lbg->maxclust){
        for (uint64_t curc = 0; curc < lbg->curclust; curc++){
            lbg->centers[curc+(lbg->curclust)] = lbg->centers[curc];
            lbg->centers[curc+(lbg->curclust)].r += (rand()%5)-2;
            lbg->centers[curc+(lbg->curclust)].g += (rand()%5)-2;
            lbg->centers[curc+(lbg->curclust)].b += (rand()%5)-2;
            //lbg->centers[curc+(lbg->curclust)].r %= 256;
            //lbg->centers[curc+(lbg->curclust)].g %= 256;
            //lbg->centers[curc+(lbg->curclust)].b %= 256;
        }
        lbg->curclust *= 2;
        printf("Starting iteration for %ld clusters\n", lbg->curclust);

        lbg->distortion = 0.0;
        int runClustering = 1;
        while (runClustering){
            if (updateAssignments(lbg) == 1){
                printf("All pixels assigned. Too many clusters!\n");
                updateCenters(lbg);
                return;
            }
            if (lbg->distortion == 0.0){
                if (lbg->curclust < lbg->maxclust){
                    printf("All colors assigned. Too many clusters!\n");
                } else {
                    printf("All colors assigned.\n");
                }
                return;
            }
            if ( ((lbg->distortion) - (lbg->prevdistortion))/(lbg->distortion) < 0.01){
                break;
            }
            updateCenters(lbg);
        }
    }
}

struct lbgdata initLbg(struct image* img, uint64_t maxclust){
    srand(4); //RFC1149.5
    struct lbgdata ret;
    ret.centers = malloc(sizeof(struct bigcolor)*maxclust);
    ret.img = img;
    ret.assignment = malloc(sizeof(uint64_t)*(img->header.width)*(img->header.height));
    ret.numassigned = malloc(sizeof(uint64_t)*maxclust);
    ret.maxclust = maxclust;
    ret.curclust = 1;
    ret.clusterdist = malloc(sizeof(double)*maxclust);
    ret.distidxsrt = malloc(sizeof(uint64_t)*maxclust);
    memset(ret.assignment, 0, sizeof(uint64_t)*(img->header.width)*(img->header.height));
    ret.numassigned[0] = ((img->header.width)*(img->header.height));
    updateCenters(&ret);
    ret.distortion = 0.0;
    return ret;
}

void destroyLbg(struct lbgdata* todes){
    free(todes->centers);
    free(todes->img->data);
    free(todes->assignment);
    free(todes->numassigned);
    free(todes->clusterdist);
    free(todes->distidxsrt);
}
