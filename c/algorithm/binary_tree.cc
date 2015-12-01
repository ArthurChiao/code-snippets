/**
 * binary tree traversing
 *
 * Author: Yanan Zhao
 * Date  : 2015-12-01
 */
#include <stdio.h>
#include <stack>
using namespace std;

struct Node {
    int value;
    struct Node *left;
    struct Node *right;
};

//---------------------------------------------------------------
// pre-order traverse
//---------------------------------------------------------------
void pre_order_recursive(struct Node *root)
{
    if (root) {
        printf("%d ", root->value);
        pre_order_recursive(root->left);
        pre_order_recursive(root->right);
    }
}

void pre_order_iterative(struct Node *root)
{
    stack<struct Node *> s;

    struct Node *p = root;
    while (p || !s.empty()) {
        while (p) {
            printf("%d ", p->value);
            s.push(p);
            p = p->left;
        }

        if (!s.empty()) {
            p = s.top();
            s.pop();
            p = p->right;
        }
    }
}


//---------------------------------------------------------------
// in-order traverse
//---------------------------------------------------------------
void in_order_recursive(struct Node *root)
{
    if (root) {
        in_order_recursive(root->left);
        printf("%d ", root->value);
        in_order_recursive(root->right);
    }
}

void in_order_iterative(struct Node *root)
{
    stack <struct Node*> s;

    struct Node *p = root;
    while (p || !s.empty()) {
        while (p) {
            s.push(p);
            p = p->left;
        }

        if (!s.empty()) {
            p = s.top();
            s.pop();
            printf("%d ", p->value);
            p = p->right;
        }
    }
}

//---------------------------------------------------------------
// post-order traverse
//---------------------------------------------------------------
void post_order_recursive(struct Node *root)
{
    if (root) {
        post_order_recursive(root->left);
        post_order_recursive(root->right);
        printf("%d ", root->value);
    }
}

void post_order_iterative(struct Node *root)
{
    stack <struct Node*> s;
    s.push(root);

    struct Node *prev = NULL;
    struct Node *curr = NULL;
    while (!s.empty()) {
        curr = s.top();
        if ((!curr->left && !curr->right) || 
                (prev && (prev == curr->left || prev == curr->right))) {
            printf("%d ", curr->value);
            s.pop();
            prev = curr;
        }
        else {
            if (curr->right) {
                s.push(curr->right);                
            }
            if (curr->left) {
                s.push(curr->left);                
            }
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

    printf("pre-oder recursive: ");
    pre_order_recursive(&root);
    printf("\n");
    printf("pre-oder iterative: ");
    pre_order_iterative(&root);
    printf("\n");

    printf("in-oder recursive: ");
    in_order_recursive(&root);
    printf("\n");
    printf("in-oder iterative: ");
    in_order_iterative(&root);
    printf("\n");

    printf("post-oder recursive: ");
    post_order_recursive(&root);
    printf("\n");
    printf("post-oder iterative: ");
    post_order_iterative(&root);
    printf("\n");

    return 0;
}
