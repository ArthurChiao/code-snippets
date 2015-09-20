
CC=gcc
#CC=~/clang

TARGET=gradient

CFLAGS= -g -std=c99

OBJ= \
	gradient.o \
	main.o

all:$(TARGET)
$(OBJ): %.o : %.c
	$(CC) -c -o $@ $< $(CFLAGS)
$(TARGET):$(OBJ)
	$(CC) $(OBJ) -o $@

clean:
	-rm -rf *.o $(TARGET)
