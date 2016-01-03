#include <stdio.h>
#include <error.h>
#include <string.h>
#include <pthread.h>

/**
 * print system error number in string format with `strerror()`
 */
int main()
{
    pthread_t mutex;

    pthread_mutex_init(&mutex, NULL);

    int ret = pthread_mutex_lock(&mutex);                                    
    printf("errno: %s\n", strerror(ret)); 
}
