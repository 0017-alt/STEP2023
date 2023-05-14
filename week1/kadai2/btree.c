#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "btree.h"

#define N 256

int scores[26] = {1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4};

int score(int li[26]) {
  int output = 0;

  for (int i = 0; i < 26; i++) {
    output += scores[i] * li[i];
  }

  return output;
}

int comp(int* list1, int* list2) {
  for (int i = 0; i < 26; i++) {
    if (list1[i] > list2[i]) {
      return 1;
    }
  }
  return 0;
}

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
        node->num += 1;
    }
    return node;
}

void searchNode(struct Node *node, char sortedWord[N], int* sc, struct Node *result) {
    if (node == NULL) {
        return;
    }

    searchNode(node->left, sortedWord, sc, result);

    //countering the number of node word
    int *li1 = malloc(sizeof(int) * 26);
    for (int i = 0; i < 26; i++) {
      li1[i] = 0;
    }
    for (int i = 0; i < strlen(node->sortedWord); i++) {
      if (65 <= node->sortedWord[i] && node->sortedWord[i] <= 90) {
        li1[node->sortedWord[i] - 65]++;
      }
      else if (97 <= node->sortedWord[i] && node->sortedWord[i] <= 122) {
        li1[node->sortedWord[i] - 97]++;
      }
      else {
        printf("invaild letter '%c'\n", node->sortedWord[i]);
        return;
      }
    }

    //countering the number of sortedWord
    int *li2 = malloc(sizeof(int) * 26);
    for (int i = 0; i < 26; i++) {
      li2[i] = 0;
    }
    for (int i = 0; i < strlen(sortedWord); i++) {
      if (65 <= sortedWord[i] && sortedWord[i] <= 90) {
        li2[sortedWord[i] - 65]++;
      }
      else if (97 <= sortedWord[i] && sortedWord[i] <= 122) {
        li2[sortedWord[i] - 97]++;
      }
      else {
        printf("invaild letter '%c'\n", sortedWord[i]);
        return;
      }
    }

    if (comp(li1, li2) == 0) {
      int tmp_score = score(li1);
      if (tmp_score > *sc) {
        *sc = tmp_score;
        *result = *node;
      }
    }

    free(li1);
    free(li2);

    searchNode(node->right, sortedWord, sc, result);

    return;
}
