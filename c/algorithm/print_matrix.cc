/**
 * print matrix in circular
 *
 * Author: Yanan Zhao
 * Date  : 2015-12-02
 */
#include <stdio.h>
#include <stack>
using namespace std;

void print_circle(int *matrix, int cols, int rows, int offset)
{
    int x_end = cols - offset - 1;
    int y_end = rows - offset - 1;

    // print above row
    for (int i = offset; i <= x_end; i++) {
        printf("%d ", matrix[offset * cols + i]);
    }

    // print right column
    for (int i = offset+1; i <= y_end; i++) {
        printf("%d ", matrix[i * cols + x_end]);
    }

    // print bottom row
    for (int i = x_end-1; i >= offset; i--) {
        printf("%d ", matrix[y_end * cols + i]);
    }

    // print right column
    for (int i = y_end-1; i >= offset+1; i--) {
        printf("%d ", matrix[i * cols + offset]);
    }
}

void print_maxtri_circularly(int *matrix, int cols, int rows)
{
    if (!matrix || !(*matrix) || cols <= 0 || rows <= 0) {
        return;
    }

    int offset = 0;
    while (cols > offset * 2 && rows > offset * 2) {
        print_circle(matrix, cols, rows, offset++);
    }
}

int main()
{
    // TODO: change API to be (int **matrix, int cols, int rows)
    int matrix[] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};

    print_maxtri_circularly(matrix, 4, 4);
}
