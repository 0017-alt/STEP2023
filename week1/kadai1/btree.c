#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "btree.h"

#define N 256

struct Node *newNode(char sortedWord[N], char originalWord[N]) {
    struct Node *node = (struct Node *)
        malloc(sizeof(struct Node));
    node->sortedWord = sortedWord;
    node->originalWord[0] = originalWord;
    node->num = 1;
    node->left = NULL;
    node->right = NULL;
    return (node);
}

struct Node *insertNode(struct Node *node, char sortedWord[N], char originalWord[N]) {
    if (node == NULL) {
        struct Node *newnode = newNode(sortedWord, originalWord);
        return(newnode);
    }
    if (strcmp(sortedWord, node->sortedWord) < 0) {
        node->left = insertNode(node->left, sortedWord, originalWord);
    }
    else if (strcmp(sortedWord, node->sortedWord) > 0) {
        node->right = insertNode(node->right, sortedWord, originalWord);
    }
    else if (strcmp(sortedWord, node->sortedWord) == 0) {
        node->originalWord[node->num] = originalWord;
        node->num++;
    }
    return node;
}

int searchNode(struct Node *node, char sortedWord[N]) {
    if (node == NULL) {
        printf("Not found\n");
        return 0;
    }
    if (strcmp(sortedWord, node->sortedWord) == 0) {
        for (int i = 0; i < node->num; i++) {
            printf("%s", node->originalWord[i]);
        }
        return 0;
    }
    else if (strcmp(sortedWord, node->sortedWord) < 0) {
        searchNode(node->left, sortedWord);
    }
    else if (strcmp(sortedWord, node->sortedWord) > 0) {
        searchNode(node->right, sortedWord);
    }
    return 0;
}
