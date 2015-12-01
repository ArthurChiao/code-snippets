/**
 * search algorithms
 *
 * Author: Yanan Zhao
 * Date  : 2015-12-01
 */
#include <stdio.h>

/**
 * input matrix
 *
 * 1  2  8  9
 * 2  4  9  12
 * 4  7  10 13
 * 6  8  11 15
 *
 * search from top-right corner each iteration, shrink to left-bottom
 */
bool find_in_partially_sorted_matrix(int *matrix, int cols, int rows, int target)
{
    bool found = false;

    if (matrix && cols > 0 && rows > 0) {
        int c = cols - 1;
        int r = 0;

        while (r < rows && c >= 0) {
            if (matrix[r * cols + c] == target) {
                found = true;
                break;
            }
            else if (matrix[r * cols + c] > target) {
                c--;
            }
            else {
                r++;
            }
        }
    }

    return found;
}
