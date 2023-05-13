CC = gcc
LD = gcc
CFLAGS = -Wall

anagram: btree.h btree.c main.c
	$(LD) $(CFLAGS) btree.c main.c -o anagram

.PHONY: clean
clean:
	rm -f anagram