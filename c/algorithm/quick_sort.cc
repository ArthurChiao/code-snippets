/**
 * quick sort
 *
 * Author: Yanan Zhao
 * Date  : 2015-12-03
 */
#include <stdio.h>

int swap(int *array, int i, int j)
{
    int tmp = array[i];
    array[i] = array[j];
    array[j] = tmp;
}

int partition(int *array, int start, int end)
{
    int pivot = array[start];
    int i = start;

    for (int j = start+1; j <= end; j++) {
        if (array[j] <= pivot) {
            i++;
            swap(array, i, j);
        }
    }

    swap(array, i, start);
    return i;
}

void _quick_sort(int *array, int start, int end)
{
    if (start >= end) {
        return;
    }

    int pivot = partition(array, start, end);
    _quick_sort(array, 0, pivot - 1);
    _quick_sort(array, pivot + 1, end);
}

void quick_sort(int *array, int size)
{
    if (!array || size <= 0) {
        return;
    }

    _quick_sort(array, 0, size - 1);
}

int main()
{
    int a[10] = {0, 1, 9, 8, 2, 3, 4, 7, 5, 6};
    quick_sort(a, 10);

    for (int i = 0; i < 10; i++) {
        printf("%d ", a[i]);
    }
    printf("\n");

    return 0;
}
