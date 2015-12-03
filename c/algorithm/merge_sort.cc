/**
 * merge sort
 *
 * Author: Yanan Zhao
 * Date  : 2015-12-03
 */
#include <stdio.h>

void merge(int *input, int start, int middle, int end, int *buf)
{
    int i = start;
    int j = middle + 1;
    int k = 0;

    while (i <= middle && j <= end) {
        if (input[i] < input[j]) {
            buf[k++] = input[i++];
        }
        else {
            buf[k++] = input[j++];
        }
    }

    while (i <= middle) {
        buf[k++] = input[i++];
    }
    while (j <= end) {
        buf[k++] = input[j++];
    }

    for (int i = 0; i < k; i++) {
        input[start + i] = buf[i];
    }
}

void merge_sort(int *input, int start, int end, int *buf)
{
    if (start >= end) {
        return;
    }

    int middle = (start + end) / 2;
    merge_sort(input, start, middle, buf);
    merge_sort(input, middle + 1, end, buf);
    merge(input, start, middle, end, buf);
}

int main()
{
    int a[10] = {0, 1, 9, 8, 2, 3, 4, 7, 5, 6};
    int b[10];
    merge_sort(a, 0, 9, b);

    for (int i = 0; i < 10; i++) {
        printf("%d ", a[i]);
    }
    printf("\n");

    return 0;
}
