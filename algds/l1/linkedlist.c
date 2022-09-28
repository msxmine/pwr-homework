#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>

struct entry {
    int val;
    struct entry* next;
};

struct list {
    struct entry* first;
    struct entry* last;
};

struct list createList(){
    struct list new;
    new.first = NULL;
    new.last = NULL;
    return new;
}

void destroyList(struct list target){
    struct entry* node = target.first;
    struct entry* next;
    while(node != NULL){
        next = node->next;
        free(node);
        node = next;
    }
}

bool insertChild(struct list* l, struct entry* after, int val){
    struct entry* new = malloc(sizeof(struct entry));
    if (new == NULL){
        return false;
    }
    new->val = val;
    if (after == NULL){
        new->next = l->first;
        l->first = new;
    }
    else{
        new->next = after->next;
        after->next = new;
    }
    if (new->next == NULL){
        l->last = new;
    }
    return true;
}

bool removeChild(struct list* l, struct entry* parent){
    if (parent == NULL){
        if (l->first != NULL){
            struct entry* toremove = l->first;
            l->first = l->first->next;
            free(toremove);
            if (l->first == NULL){
                l->last = NULL;
            }
            return true;
        }
        else{
            return false;
        }
    }
    else{
        if (parent->next != NULL){
            struct entry* newchild = parent->next->next;
            free(parent->next);
            parent->next = newchild;
            if (newchild == NULL){
                l->last = parent;
            }
            return true;
        }
        else{
            return false;
        }
    }
}

struct entry* findParent(struct list* l, int val){
    if (l->first == NULL || l->first->val == val){
        return NULL;
    }
    struct entry* candidate = l->first;
    while (candidate->next != NULL && candidate->next->val != val){
        candidate = candidate->next;
    }
    return candidate;
}

struct entry* find(struct list* l, int val){
    struct entry* parent = findParent(l, val);
    if (parent == NULL){
        return l->first;
    }
    else{
        return parent->next;
    }
}

bool removeVal(struct list* l, int val){
    struct entry* parent = findParent(l, val);
    struct entry* node;
    if (parent == NULL){
        node = l->first;
    }
    else{
        node = parent->next;
    }
    if (node != NULL){
        removeChild(l, parent);
        return true;
    }
    else{
        return false;
    }
}

void merge(struct list* l1, struct list* l2){
    if (l1->last == NULL){
        l1->first = l2->first;
        l1->last = l2->last;
    }
    else{
        l1->last->next = l2->first;
        l1->last = l2->last;
    }
}
    
void printList(struct list l){
    struct entry* nod = l.first;
    while(nod != NULL){
        printf("%d->", nod->val);
        nod = nod->next;
    }
}
    
    
int main(){
    int used[1000] = {0};
    
    struct list l1 = createList();
    
    int start = rand() % 1000;
    for (int i = (start+1) % 1000; i != start; i = (i+1)%1000){
        if (used[i] == 0){
            used[i] = 1;
            insertChild(&l1, l1.last, i);
            start = rand() % 1000;
            i = (start+1) % 1000;
        }
    }
    
    clock_t starttim,endtim;
    
    for(int tval = 0; tval < 1000; tval += 200){
        starttim = clock();
        for (int i = 0; i < 1000000; i++){
            find(&l1, tval);
        }
        endtim = clock();
        long double acct = (long double)(endtim - starttim)/1000000.0;
        printf("Dostęp do %d : %Lf\n", tval, acct);
    }
    
    int randomnums[1000000];
    for (int i = 0; i < 1000000; i++){
        randomnums[i] = rand() % 1000;
    }
    
    starttim = clock();
    for (int i = 0; i < 1000000; i++){
        find(&l1, randomnums[i]);
    }
    endtim = clock();
    long double acct = (long double)(endtim - starttim)/1000000.0;
    printf("Dostęp do losowych : %Lf\n", acct);
    
    struct list l2 = createList();
    struct list l3 = createList();
    
    insertChild(&l2, l2.last, 1);
    insertChild(&l2, l2.last, 2);
    insertChild(&l2, l2.last, 3);
    insertChild(&l3, NULL, 5);
    insertChild(&l3, l3.first, 6);
    insertChild(&l3, NULL, 4);
    
    merge(&l2, &l3);
    
    printList(l2);
    
    destroyList(l1);
    destroyList(l2);
    
    return 0;
}
