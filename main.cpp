#include <cassert>
#include <cstring>
#include <cstdlib>
#include <cstdio>
#include <omp.h>

#define TASK_SIZE 100

unsigned int rand_interval(unsigned int min, unsigned int max) {
    // https://stackoverflow.com/questions/2509679/
    int r;
    const unsigned int range = 1 + max - min;
    const unsigned int buckets = RAND_MAX / range;
    const unsigned int limit = buckets * range;

    do {
        r = rand();
    } while (r >= limit);

    return min + (r / buckets);
}

void fillupRandomly(int *m, int size, unsigned int min, unsigned int max) {
    for (int i = 0; i < size; i++)
        m[i] = rand_interval(min, max);
}

void mergeSortAux(int *X, int n, int *tmp) {
    int i = 0;
    int j = n / 2;
    int ti = 0;

    while (i < n / 2 && j < n) {
        if (X[i] < X[j]) {
            tmp[ti] = X[i];
            ti++;
            i++;
        } else {
            tmp[ti] = X[j];
            ti++;
            j++;
        }
    }
    while (i < n / 2) { /* finish up lower half */
        tmp[ti] = X[i];
        ti++;
        i++;
    }
    while (j < n) { /* finish up upper half */
        tmp[ti] = X[j];
        ti++;
        j++;
    }
    memcpy(X, tmp, n * sizeof(int));
}

void mergeSort(int *X, int n, int *tmp) {
    if (n < 2) return;

#pragma omp task shared(X) if (n > TASK_SIZE)
    mergeSort(X, n / 2, tmp);

#pragma omp task shared(X) if (n > TASK_SIZE)
    mergeSort(X + (n / 2), n - (n / 2), tmp + n / 2);

#pragma omp taskwait
    mergeSortAux(X, n, tmp);
}


int isSorted(int *a, int size) {
    for (int i = 0; i < size - 1; i++)
        if (a[i] > a[i + 1])
            return false;
    return true;
}

void printArray(int *a, int size) {
    for (int i = 0; i < size; i++)
        printf("%d ", a[i]);
    printf("\n");
}

int main(int argc, char *argv[]) {
    srand(123456);
    int N = (argc > 1) ? atoi(argv[1]) : 10;                // array length
    int print = (argc > 2) ? atoi(argv[2]) : 0;             // print array?
    int numThreads = (argc > 3) ? atoi(argv[3]) : 2;        // num threads
//    int *X = static_cast<int *>(malloc(N * sizeof(int)));
    int *X = new int[N];
//    int *tmp = static_cast<int *>(malloc(N * sizeof(int)));
    int *tmp = new int[N];

    omp_set_dynamic(0);              /** Explicitly disable dynamic teams **/
    omp_set_num_threads(numThreads); /** Use N threads for all parallel regions **/

    fillupRandomly(X, N, 0, 5);


    double begin = omp_get_wtime();
#pragma omp parallel
    {
#pragma omp single
        mergeSort(X, N, tmp);
    }
    double end = omp_get_wtime();
    printf("%f", end - begin);

    assert(isSorted(X, N));

    if (print) {
        printArray(X, N);
    }

    free(X);
    free(tmp);
    return (EXIT_SUCCESS);
}