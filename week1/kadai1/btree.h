#ifndef _BTREE_H_INCLUDED
#define _BTREE_H_INCLUDED

#define N 256

#include <stdlib.h>
#include <stdio.h>

struct Node {
    char *sortedWord;
    char *originalWord[N];
    int num;
    struct Node *left;
    struct Node *right;
};

struct Node *newNode(char sortedWord[N], char originalWord[N]);

struct Node *insertNode(struct Node *node, char sortedWord[N], char originalWord[N]);

int searchNode(struct Node *node, char sortedWord[N]);

#endif