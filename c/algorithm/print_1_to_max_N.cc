/**
 * given N, print numbers from 1 to 99...9, where N is the number of 9s
 *
 * Note that N may be a very large number, e.g. N=200
 *
 * Author: Yanan Zhao
 * Date  : 2015-12-02
 */
#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
using namespace std;

/**
 * As N may be very large, we use char array to mocking big numbers
 */
void print_core(char *num_array, int array_len, int curr_index)
{
    if (curr_index == array_len - 1) {
        for (int i = 0; i < array_len; i++) {
            printf("%c", num_array[i]);
        }
        printf("\n");
        return;
    }

    for (int i = 0; i < 10; i++) {
        num_array[curr_index + 1] = '0' + i;
        print_core(num_array, array_len, curr_index + 1);
    }
}

void print_1_to_N(int N)
{
    if (N <= 0) {
        printf("invalid N: %d\n", N);
        return;
    }

    char *num = (char *)malloc(N * sizeof(char));
    if (!num) {
        printf("malloc failed\n");
    }
    memset(num, '0', N * sizeof(char));

    for (int i = 0; i < 10; i++) {
        num[0] = '0' + i;
        print_core(num, N, 0);
    }
}

int main(int argc, char *argv[])
{
    if (argc != 2) {
        printf("Usage: ./a.out <N>\n");
        return 0;
    }

    int N = atoi(argv[1]);
    print_1_to_N(N);

    return 0;
}
