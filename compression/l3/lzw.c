#include "lzw.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

struct lzwdictentry {
    uint64_t id;
    struct lzwdictentry* prefix;
    uint8_t letter;
    struct lzwdictentry* suffix[256];
};

struct lzwdictpage {
    struct lzwdictentry c[2048];
    struct lzwdictpage* next;
    uint64_t startidx;
};

struct lzwdict {
    struct lzwdictpage first;
    uint64_t size;
};

struct lzwdict words;

struct lzwdictentry* addEntry(struct lzwdictentry* prefix, uint8_t byte){
    uint64_t newid = words.size;
    words.size += 1;
    struct lzwdictpage* goodpage = &(words.first);
    while (goodpage->startidx + 2047 < newid){
        //printf("%d %d\n",goodpage->startidx + 2048, newid);
        if (goodpage->next == NULL){
            goodpage->next = malloc(sizeof(struct lzwdictpage));
            goodpage->next->startidx = goodpage->startidx + 2048;
            goodpage->next->next = NULL;
        }
        goodpage = goodpage->next;
    }
    uint64_t pageidx = newid%2048;
    struct lzwdictentry* result = &(goodpage->c[pageidx]);
    result->id = newid;
    result->prefix = prefix;
    result->letter = byte;
    for (int i = 0; i < 256; i++){
        result->suffix[i] = NULL;
    }
    if (prefix != NULL){
        prefix->suffix[byte] = result;
    }
    return result;
}

struct lzwdictentry* getEbyIdx(uint64_t idx){
    struct lzwdictpage* goodpage = &(words.first);
    while (goodpage->startidx + 2047 < idx){
        goodpage = goodpage->next;
    }
    return &(goodpage->c[idx%2048]);
}

uint8_t printDword(struct lzwdictentry* ending, FILE* fou){
    if (ending->prefix == NULL){
        fwrite(&(ending->letter), 1, 1, fou);
        return ending->letter;
    } else {
        uint8_t resc = printDword(ending->prefix, fou);
        fwrite(&(ending->letter), 1, 1, fou);
        return resc;
    }
}

void initdict(){
    words.size = 0;
    words.first.startidx = 0;
    words.first.next = NULL;
    for (int i = 0; i < 256; i++){
        //printf("adding dentry\n");
        addEntry(NULL, i);
    }
}

void destroydict(){
    words.size = 0;
    struct lzwdictpage* pg = words.first.next;
    while (pg != NULL){
        struct lzwdictpage* nextpg = pg->next;
        free(pg);
        pg = nextpg;
    }
    words.first.next = NULL;
}

void lzwEncode( FILE* infile, void (*pushIdx)(uint64_t)){
    initdict();
    uint8_t nextbyte;
    if (fread(&nextbyte, 1, 1, infile) == 0){
        return;
    }
    struct lzwdictentry* dictword = &(words.first.c[nextbyte]);
    while (fread(&nextbyte, 1, 1, infile)){
        //printf("reading inbyte\n");
        if (dictword->suffix[nextbyte] != NULL){
            dictword = dictword->suffix[nextbyte];
        } else {
            (*pushIdx)(dictword->id + 1);
            addEntry(dictword, nextbyte);
            dictword = &(words.first.c[nextbyte]);
        }
    }
    (*pushIdx)(dictword->id + 1);
    destroydict();
}

void lzwDecode( uint64_t (*getIdx)(), FILE* outfile){
    initdict();
    struct lzwdictentry* lastprinted = NULL;
    uint8_t lastprintedsymbol = 0;
    uint64_t nextsym;
    while((nextsym = (*getIdx)()) != 0){
        nextsym -= 1;
        if (nextsym < words.size){
            struct lzwdictentry* curword = getEbyIdx(nextsym);
            uint8_t fletter = printDword(curword, outfile);
            if (lastprinted != NULL){
                addEntry(lastprinted, fletter);
            }
            lastprinted = curword;
            lastprintedsymbol = fletter;
        } else {
            struct lzwdictentry* newentry = addEntry(lastprinted, lastprintedsymbol);
            lastprintedsymbol = printDword(newentry, outfile);
            lastprinted = newentry;
        }
    }
    destroydict();
}
