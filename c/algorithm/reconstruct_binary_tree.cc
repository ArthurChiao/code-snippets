/**
 * rebuild binary tree from pre-order and in-order traversing results
 *
 * Author: Yanan Zhao
 * Date  : 2015-12-01
 */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

struct Node {
    int value;
    struct Node *left;
    struct Node *right;
};

struct Node*
construct_core(int *pre_start, int *pre_end, int *in_start, int *in_end)
{
    if (pre_start > pre_end || in_start > in_end) {
        return NULL;
    }

    struct Node *root = (struct Node *)malloc(sizeof(struct Node));
    assert(root != NULL);
    root->value = pre_start[0];
    printf("root %d\n", root->value);
    root->left = NULL;
    root->right = NULL;

    int *tmp = in_start;
    while (tmp && tmp <= in_end) {
        if (*tmp == root->value) {
            //printf("found , index %ld\n", tmp-in_start);
            break;
        }
        tmp++;
    }

    if (tmp > in_end) {
        printf("error\n");
        return NULL;
    }

    int left_nodes = tmp - in_start;
    root->left = construct_core(pre_start + 1, pre_start + left_nodes,
            in_start, tmp -1);
    root->right = construct_core(pre_start + left_nodes + 1, pre_end,
            tmp + 1, in_end);

    return root;
}

struct Node* reconstruct_binary_tree(int *preorder, int *inorder, int total_nodes)
{
    if (!preorder || !inorder || total_nodes <= 0) {
        return NULL;
    }

    return construct_core(preorder, preorder + total_nodes -1,
            inorder, inorder + total_nodes - 1);
}

void pre_order_recursive(struct Node *root)
{
    if (root) {
        printf("%d ", root->value);
        pre_order_recursive(root->left);
        pre_order_recursive(root->right);
    }
}

int main()
{
    int preorder[] = {1,2,4,7,3,5,6,8};
    int inorder[]  = {4,7,2,1,5,3,8,6};

    struct Node *root;
    root = reconstruct_binary_tree(preorder, inorder, 8);

    pre_order_recursive(root);
}
