CC=gcc
TARGET=cjson

CFLAGS= -g -lm

all:
	$(CC) cJSON.c test.c $(CFLAGS) -o $(TARGET)

clean:
	-rm -f *.o core core.* $(TARGET)
