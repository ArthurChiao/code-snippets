/**
 * sub binary tree
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

bool has_subtree(struct Node *tree, struct Node *subtree)
{
    if (!subtree) {
        return false;
    }

    if (!tree) {
        return false;
    }

    if (tree->value != subtree->value) {
        return false;
    }

    return has_subtree(tree->left, subtree->left) &&
        has_subtree(tree->right, subtree->right);
}

bool is_sub_tree(struct Node *tree, struct Node *subtree)
{
    if (!tree || !subtree) {
        return false;
    }

    bool b_result = false;
    if (tree->value == subtree->value) {
        b_result = has_subtree(tree, subtree);
    }

    if (!b_result) {
        b_result = is_sub_tree(tree->left, subtree);
    }
    if (!b_result) {
        b_result = is_sub_tree(tree->right, subtree);
    }

    return b_result;
}


//---------------------------------------------------------------
// test
//---------------------------------------------------------------
int main()
{
    /**
     *        8
     *       / \
     *      8   7
     *     /\
     *    9 2
     *     / \
     *    4  7
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

    //TODO
    //construct test case, verify the algorithm

    return 0;
}
