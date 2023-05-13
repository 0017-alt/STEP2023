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
    else if (input[i] == ' ') {}
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
    root = insertNode(root, sort(chr), ch);
  }

  //closing the dictionary
  if (fclose(fp_r) == EOF) {
    perror("file close error(words.txt)\n");
    exit(1);
  }

  //get the input, sort it, and find it in the dictionary
  FILE *fp = fopen("input.txt", "r");
  char input[N];
  char *sorted_input;
  int c = 1;
  while (fgets(input, N, fp) != NULL) {
    sorted_input = sort(input);
    printf("result%d:\n", c);
    searchNode(root, sorted_input);
    printf("------------------\n");
    c++;
  }

  if (fclose(fp) == EOF) {
    perror("file close error(input.txt)\n");
    exit(1);
  }

  return 0;
}
