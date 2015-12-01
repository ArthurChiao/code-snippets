/**
 * string operations
 *
 * Author: Yanan Zhao
 * Date  : 2015-12-01
 */
#include <stdio.h>
#include <string.h>

/**
 * replace blank char with '20%' in the same buffer
 * e.g. "we are happy" -> "we20%are20%happy"
 * the buffer is assumed to be long enough
 */
int replace_blank_inplace(char str[], int buflen)
{
    if (!str || buflen <= 0) {
        return false;
    }

    int num_chars = 0;
    int num_blanks = 0;
    int total_chars = 0;

    char *p = str;
    while (*p != '\0') {
        if (*p == ' ') {
            num_blanks++;
        }

        num_chars++;
        p++;
    }
    total_chars = num_chars + num_blanks;

    int new_len = total_chars + 2 * num_blanks;
    if (new_len > buflen) {
        return false;
    }

    char *p1 = str + total_chars;
    char *p2 = str + total_chars + 2 * num_blanks;
    while (total_chars--) {
        if (*p1 == ' ') {
            *p2-- = '%';
            *p2-- = '0';
            *p2-- = '2';
        }
        else {
            *p2-- = *p1;
        }

        p1--;
    }

    return true;
}

int main()
{
    char str[100];
    const char *s = "we are happy";
    memcpy(str, s, strlen(s) + 1);

    printf("original: %s\n", str);
    replace_blank_inplace(str, 100);
    printf("after replace: %s\n", str);
}
