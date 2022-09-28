#include <stdlib.h>
#include <pthread.h>

pthread_mutex_t coordlock;
int curx = 0;
int cury = 0;

int** mat1;
int** mat2;
int** result;

int dim;

void* dowork(void* vargp){
    int myx;
    int myy;
    int cell = 0;
    while (1){
        pthread_mutex_lock(&coordlock);
        myx = curx;
        myy = cury;
        curx++;
        if (curx == dim){
            curx = 0;
            cury++;
        }
        pthread_mutex_unlock(&coordlock);
        if (myy >= dim){
            return NULL;
        }
        cell = 0;
        for (int i = 0; i < dim; i++){
            if (mat1[myy][i] && mat2[i][myx]){
                cell = 1;
                break;
            }
        }
        result[myy][myx] = cell;
    }
}


int main(int argc, char** argv){
    if (argc != 3){
        return 1;
    }
    dim = atoi(argv[1]);
    int threads = atoi(argv[2]);
    
    mat1 = malloc(sizeof(int*)*dim);
    mat2 = malloc(sizeof(int*)*dim);
    result = malloc(sizeof(int*)*dim);
    for (int i = 0; i < dim; i++){
        mat1[i] = malloc(sizeof(int)*dim);
        mat2[i] = malloc(sizeof(int)*dim);
        result[i] = malloc(sizeof(int)*dim);
    }
    
    for (int i = 0; i < dim; i++){
        for (int j = 0; j < dim; j++){
            mat1[i][j] = random() % 2;
            mat2[i][j] = random() % 2;
        }
    }
    
    pthread_mutex_init(&coordlock, NULL);
    
    pthread_t* threadrefs = malloc(sizeof(pthread_t) * threads);
    for (int i = 0; i < threads; i++){
        pthread_create(&threadrefs[i], NULL, dowork, NULL);
    }
    
    for (int i = 0; i < threads; i++){
        pthread_join(threadrefs[i], NULL);
    }
    
    pthread_mutex_destroy(&coordlock);
    free(threadrefs);
    
    for (int i = 0; i < dim; i++){
        free(mat1[i]);
        free(mat2[i]);
        free(result[i]);
    }
    free(mat1);
    free(mat2);
    free(result);
    
    
    return 0;
}
