#include <stdio.h>
#include "ascii_art.h"

int main()
{
#if 0 // read from file
    FILE *fpi = fopen("ascii_art.txt", "r");
    if (!fpi) {
        printf("read file failed\n");
        return 1;
    }

    char buf[100];
    while (fgets(buf, 100, fpi) != NULL) {
        printf("%s", buf);
    }
#else // include from header file, compile into binary
    printf("%s\n", logo);
#endif
}
