#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>

struct node {
    int val;
    struct node* next;
    struct node* prev;
};

struct list {
    struct node* first;
};

struct list createList(){
    struct list new;
    new.first = NULL;
    return new;
}

void destroyList(struct list target){
    struct node* cur;
    struct node* next;
    cur = target.first;
    if (cur == NULL){
        return;
    }
    cur->prev->next = cur->prev;
    while(cur != cur->next){
        next = cur->next;
        free(cur);
        cur = next;
    }
}

struct node* insertChild(struct list* l, struct node* parent, int val){
    struct node* newnode = malloc(sizeof(struct node));
    if (newnode == NULL){
        return NULL;
    }
    newnode->val = val;
    
    if (l->first == NULL){
        if (parent == NULL){
            l->first = newnode;
            newnode->next = newnode;
            newnode->prev = newnode;
            return newnode;
        }
        else{
            return NULL;
        }
    }
    else{
        if (parent == NULL){
            return NULL;
        }
        else{
            newnode->next = parent->next;
            newnode->prev = parent;
            newnode->next->prev = newnode;
            newnode->prev->next = newnode;
            return newnode;
        }
    }
}

bool removeNode(struct list* l, struct node* target){
    if (target == NULL){
        return false;
    }
    if (target->next == target){
        free(target);
        l->first = NULL;
        return true;
    }
    target->prev->next = target->next;
    target->next->prev = target->prev;
    free(target);
    return true;
}

struct node* find(struct list* l, int val){
    if (l->first == NULL){
        return NULL;
    }
    else{
        struct node* tocheck = l->first;
        do {
            if (tocheck->val == val){
                return tocheck;
            }
            tocheck = tocheck->next;
        } while (tocheck != l->first);
        return NULL;
    }
}

void merge(struct list* l1, struct list* l2){
    if (l2->first == NULL){
        return;
    }
    if (l1->first == NULL){
        l1->first = l2->first;
        return;
    }
    l1->first->prev->next = l2->first;
    l2->first->prev->next = l1->first;
    struct node* lastelem = l2->first->prev;
    l2->first->prev = l1->first->prev;
    l1->first->prev = lastelem;
    return;
}

void printList(struct list l){
    if (l.first != NULL){
        struct node* cur = l.first;
        do {
            printf("-> %d <-", cur->val);
            cur = cur->next;
        }
        while(cur != l.first);
    }
}

int main(){
    int used[1000] = {0};
    
    struct list l1 = createList();
    
    int start = rand() % 1000;
    for (int i = (start+1) % 1000; i != start; i = (i+1)%1000){
        if (used[i] == 0){
            used[i] = 1;
            insertChild(&l1, (l1.first == NULL ? NULL : l1.first->prev), i);
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
    
    insertChild(&l2, l2.first, 1);
    insertChild(&l2, l2.first->prev, 2);
    insertChild(&l2, l2.first->prev, 3);
    insertChild(&l3, l3.first, 4);
    insertChild(&l3, l3.first->prev, 5);
    insertChild(&l3, l3.first->prev, 6);
    
    merge(&l2, &l3);
    
    printList(l2);
    
    destroyList(l1);
    destroyList(l2);
    
    return 0;
}
