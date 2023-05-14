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

int score(int li[26]);

int comp(int* list1, int* list2);

struct Node *newNode(char sortedWord[N], char originalWord[N]);

struct Node *insertNode(struct Node *node, char sortedWord[N], char originalWord[N]);

void searchNode(struct Node *node, char sortedWord[N], int* sc, struct Node *result);

#endif
