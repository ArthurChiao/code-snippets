/**
 * find the k-th node in list, couting backward
 *
 * Author: Yanan Zhao
 * Date  : 2015-12-02
 */
#include <stdio.h>

struct Node {
    int value;
    struct Node *next;
};

struct Node*
find_kth_node_backward(struct Node* root, int K)
{
    if (K < 1 || !root) {
        return NULL;
    }

    struct Node *front = root;
    struct Node *back = root;
    int count = K;
    while (count--) {
        front = front->next;
        if (!front) {
            return (count == 0)? back : NULL;
        }
    }

    while (front) {
        /* printf("front %d\n", front->value); */
        /* printf("back %d\n", back->value); */
        front = front->next;
        back = back->next;
    }
    return back;
}

int main()
{
    struct Node node0 = {0, NULL};
    struct Node node1 = {1, NULL};
    struct Node node2 = {2, NULL};
    struct Node node3 = {3, NULL};
    struct Node node4 = {4, NULL};
    struct Node node5 = {5, NULL};
    struct Node node6 = {6, NULL};
    struct Node node7 = {7, NULL};
    node0.next = &node1;
    node1.next = &node2;
    node2.next = &node3;
    node3.next = &node4;
    node4.next = &node5;
    node5.next = &node6;
    node6.next = &node7;

    for (int i = -1; i < 10; i++) {
        struct Node *node = find_kth_node_backward(&node0, i);
        printf("K=%d, node %d\n", i, !node? -1 : node->value);
    }

    return 0;
}
