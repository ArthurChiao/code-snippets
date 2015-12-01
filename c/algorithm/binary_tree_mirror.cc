/**
 * mirror of a binary tree
 *
 * Author: Yanan Zhao
 * Date  : 2015-12-02
 */
#include <stdio.h>
#include <stack>
using namespace std;

struct Node {
    int value;
    struct Node *left;
    struct Node *right;
};

struct Node*
mirror_tree(struct Node *root)
{
    if (!root) {
        return NULL;
    }

    struct Node *left  = mirror_tree(root->right);
    struct Node *right = mirror_tree(root->left);
    root->left  = left;
    root->right = right;
    return root;
}

void pre_order_recursive(struct Node *root)
{
    if (root) {
        printf("%d ", root->value);
        pre_order_recursive(root->left);
        pre_order_recursive(root->right);
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

    printf("pre-oder recursive: ");
    pre_order_recursive(&root);
    printf("\n");

    printf("pre-oder recursive (mirror tree): ");
    struct Node *mirror = mirror_tree(&root);
    pre_order_recursive(mirror);
    printf("\n");

    return 0;
}
