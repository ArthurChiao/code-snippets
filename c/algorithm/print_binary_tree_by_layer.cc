/**
 * print binary tree by layer (up to bottom layers)
 *
 * Author: Yanan Zhao
 * Date  : 2015-12-02
 */
#include <stdio.h>
#include <stack>
#include <deque>
using namespace std;

struct Node {
    int value;
    struct Node *left;
    struct Node *right;
};

void print_tree_by_layer(struct Node *root)
{
    if (!root) {
        return;
    }

    deque<struct Node *> q;
    q.push_back(root);

    struct Node *p;
    while (q.size()) {
        p = q.front();
        q.pop_front();

        printf("%d \n", p->value);
        if (p->left) {
            q.push_back(p->left);
        }
        if (p->right) {
            q.push_back(p->right);
        }
    }
}

//---------------------------------------------------------------
// test
//---------------------------------------------------------------
int main()
{
    /**
     *        0
     *       / \
     *      1   2
     *     /\  /\
     *    3 4  5 6
     */
    struct Node root = {0, NULL, NULL};
    struct Node lchild = {1, NULL, NULL};
    struct Node rchild = {2, NULL, NULL};
    struct Node llchild = {3, NULL, NULL};
    struct Node lrchild = {4, NULL, NULL};
    struct Node rlchild = {5, NULL, NULL};
    struct Node rrchild = {6, NULL, NULL};

    root.left = &lchild;
    root.right = &rchild;
    lchild.left = &llchild;
    lchild.right = &lrchild;
    rchild.left = &rlchild;
    rchild.right = &rrchild;

    printf("----------------\n");
    printf("       0        \n");
    printf("      / \\      \n");
    printf("     1   2      \n");
    printf("    /\\  /\\    \n");
    printf("   3 4  5 6     \n");
    printf("----------------\n");

    print_tree_by_layer(&root);

    return 0;
}
