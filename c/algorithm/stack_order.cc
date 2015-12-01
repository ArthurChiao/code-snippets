/**
 * decide if given sequence is stack push/pop order
 *
 * Author: Yanan Zhao
 * Date  : 2015-12-01
 */
#include <stdio.h>
#include <stack>
using namespace std;

int is_pop_order(int *push, int *pop, int len)
{
    if (!push || !pop || len <= 0) {
        return false;
    }

    stack<int> s;
    int *nextpop = pop;
    int *nextpush = push;
    while (nextpop - pop < len) {
        while (s.empty() || s.top() != *nextpop) {
            if (nextpush - push == len) {
                break;
            }

            s.push(*nextpush++);
        }

        if (s.top() != *nextpop) {
            return false;
        }

        s.pop();
        nextpop++;
    }

    if (s.empty() && nextpop - pop == len) {
        return true;
    }

    return false;
}

int main()
{
    int push1[] = {1,2,3,4,5};
    int pop1[] = {4,5,3,2,1};
    int pop2[] = {4,3,5,1,2};

    printf("is_pop_order: %d\n", is_pop_order(push1, pop1, 5));
    printf("is_pop_order: %d\n", is_pop_order(push1, pop2, 5));
}
