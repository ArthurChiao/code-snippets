/**
 * linked list operations
 *
 * Author: Yanan Zhao
 * Date  : 2015-12-01
 */
#include <stdio.h>
#include <stack>
using namespace std;

struct ListNode {
    int value;
    struct ListNode *next;
};

void print_list_reverse_order_recursive(struct ListNode *node)
{
    if (!node) {
        return;
    }

    print_list_reverse_order_recursive(node->next);
    printf("%d ", node->value);
}

void print_list_reverse_order_iterative(struct ListNode *head)
{
    if (!head) {
        return;
    }

    stack <struct ListNode *> s;

    struct ListNode *p = head;
    while (p) {
        s.push(p);
        p = p->next;
    }

    while (!s.empty()) {
        p = s.top();
        printf("%d ", p->value);
        s.pop();
    }
}

int main()
{
    struct ListNode node0 = {0, NULL};
    struct ListNode node1 = {1, NULL};
    struct ListNode node2 = {2, NULL};
    struct ListNode node3 = {3, NULL};
    struct ListNode node4 = {4, NULL};
    node0.next = &node1;
    node1.next = &node2;
    node2.next = &node3;
    node3.next = &node4;

    print_list_reverse_order_recursive(&node0);
    print_list_reverse_order_iterative(&node0);
}
