CC=gcc
CFLAGS=-O2
all: search2 search3 coldesc colclimb transclimb
%: %.c
	$(CC) $(CFLAGS) -o $@ $< -lm
clean:
	rm -f search2 search3 coldesc colclimb transclimb
