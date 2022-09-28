#include <stdint.h>

struct bigcolor {
    int64_t r;
    int64_t g;
    int64_t b;
};

struct lbgdata {
    struct bigcolor* centers; //Centers of clusters
    struct image* img;
    uint64_t* assignment;  //Assigned cluster id for each pixel
    uint64_t* numassigned; //Num of assigned pixels for each cluster
    uint64_t maxclust;     //Max cluster limit
    uint64_t curclust;
    double prevdistortion;
    double distortion;
    double* clusterdist;
    uint64_t* distidxsrt;
};

struct lbgdata initLbg(struct image* img, uint64_t maxclust);
void runLbg(struct lbgdata* lbg);
void destroyLbg(struct lbgdata* todes);
uint64_t colorDist(struct color a, struct bigcolor b);
