#ifndef _RPCALC_MY_HEAD
#define _RPCALC_MY_HEAD
static const int modn = 1234577;

struct BigInt {
    mpz_t i;
    int depth;
    int reftorpn;
};
#endif
