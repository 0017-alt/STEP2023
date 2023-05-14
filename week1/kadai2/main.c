#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "btree.h"

#define N 256

//sort the stirng in a word
char* sort(char* input) {
  int li[26];
  for (int i = 0; i < 26; i++) {
    li[i] = 0;
  }

  //countering the number of alphabets
  for (int i = 0; i < strlen(input)-1; i++) {
    if (65 <= input[i] && input[i] <= 90) {
      li[input[i] - 65]++;
    }
    else if (97 <= input[i] && input[i] <= 122) {
      li[input[i] - 97]++;
    }
    else {
      printf("invaild letter '%c'\n", input[i]);
      return "";
    }
  }

  //creating the sored_word
  char *output;
  output = malloc(sizeof(char) * strlen(input));
  int p = 0;
  for (int i = 0; i < 26; i++) {
    while (li[i] > 0) {
      *(output + p) = i + 97;
      p++;
      li[i]--;
    }
  }

  return output;
}

int main() {
  //opening the dictionary
  FILE *fp_r;
  fp_r = fopen("words.txt", "r");
  if (fp_r == NULL) {
    perror("file open error(words.txt)\n");
    exit(1);
  }

  //creating the sorted dictionary
  struct Node *root = NULL;
  char chr[N];
  while (fgets(chr, N, fp_r) != NULL) {
    char *ch = malloc(sizeof(char) * strlen(chr));
    for (int i = 0; i < strlen(chr); i++) {
      *(ch + i) = chr[i];
    }
    char *chr_sorted = malloc(sizeof(char) * strlen(chr));
    chr_sorted = sort(ch);
    root = insertNode(root, chr_sorted, ch);
  }

  //closing the dictionary
  if (fclose(fp_r) == EOF) {
    perror("file close error(words.txt)\n");
    exit(1);
  }

  //get the input, sort it, and find it in the dictionary
  FILE *fp = fopen("small.txt", "r");
  FILE *fp_w = fopen("small_answer.txt", "w");
  char input[N];
  char *sorted_input;
  while (fgets(input, N, fp) != NULL) {
    sorted_input = sort(input);
    struct Node *result = (struct Node *)malloc(sizeof(struct Node));
    int sc = 0;
    searchNode(root, sorted_input, &sc, result);
    fprintf(fp_w, "%s", result->originalWord[0]);
  }
  if (fclose(fp) == EOF) {
    perror("file close error\n");
    exit(1);
  }
  if (fclose(fp_w) == EOF) {
    perror("file close error\n");
    exit(1);
  }

  fp = fopen("medium.txt", "r");
  fp_w = fopen("medium_answer.txt", "w");
  while (fgets(input, N, fp) != NULL) {
    sorted_input = sort(input);
    struct Node *result = (struct Node *)malloc(sizeof(struct Node));
    int sc = 0;
    searchNode(root, sorted_input, &sc, result);
    fprintf(fp_w, "%s", result->originalWord[0]);
  }
  if (fclose(fp) == EOF) {
    perror("file close error\n");
    exit(1);
  }
  if (fclose(fp_w) == EOF) {
    perror("file close error\n");
    exit(1);
  }

  fp = fopen("large.txt", "r");
  fp_w = fopen("large_answer.txt", "w");
  while (fgets(input, N, fp) != NULL) {
    sorted_input = sort(input);
    struct Node *result = (struct Node *)malloc(sizeof(struct Node));
    int sc = 0;
    searchNode(root, sorted_input, &sc, result);
    fprintf(fp_w, "%s", result->originalWord[0]);
  }
  if (fclose(fp) == EOF) {
    perror("file close error\n");
    exit(1);
  }
  if (fclose(fp_w) == EOF) {
    perror("file close error\n");
    exit(1);
  }


  return 0;
}
