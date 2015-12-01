/**
 * merge two ordered linked lists
 *
 * Author: Yanan Zhao
 * Date  : 2015-12-02
 */
#include <stdio.h>
#include <stack>
using namespace std;

struct ListNode {
    int value;
    struct ListNode *next;
};

struct ListNode*
merge_lists(struct ListNode* node0, struct ListNode* node1)
{
    if (!node0) {
        return node1;
    }

    if (!node1) {
        return node0;
    }

    struct ListNode *node = NULL;
    if (node0->value < node1->value) {
        node = node0;
        node->next = merge_lists(node0->next, node1);
    }
    else {
        node = node1;
        node->next = merge_lists(node0, node1->next);
    }

    return node;
}

void print_list(struct ListNode *head)
{
    while (head) {
        printf("%d ", head->value);
        head = head->next;
    }
    printf("\n");
}

int main()
{
    struct ListNode node0 = {0, NULL};
    struct ListNode node1 = {1, NULL};
    struct ListNode node2 = {2, NULL};
    struct ListNode node3 = {3, NULL};
    struct ListNode node4 = {4, NULL};
    struct ListNode node5 = {5, NULL};
    struct ListNode node6 = {6, NULL};
    struct ListNode node7 = {7, NULL};
    node0.next = &node2;
    node2.next = &node4;
    node4.next = &node6;
    node1.next = &node3;
    node3.next = &node5;
    node5.next = &node7;

    struct ListNode *list0 = &node0;
    struct ListNode *list1 = &node1;
    struct ListNode *merged = merge_lists(list0, list1);
    print_list(merged);

    return 0;
}
