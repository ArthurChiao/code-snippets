#include <stddef.h>
#include <stdio.h>
#include <sys/socket.h>
#include <sys/un.h>

/**
 * Advantages of UNIX socket compared with iternet socket
 * - no handling for protocols
 * - no encap/decap for protocol headers
 * - no checksum
 * - no seq, ack
 * in summary, very efficient
 *
 * Disadvantages
 * - could only be used between processes on the same host
 * - not identical implementations between different OS (UNIX V, BSD, linux, etc)
 */

/**
 * example to create and bind unix sock
 *
 * Compile: gcc bind_sock.c
 * Usage: ./a.out
 */
int main()
{
    int fd, size;
    struct sockaddr_un un;

    un.sun_family = AF_UNIX;
    strcpy(un.sun_path, "test.sock");
    if ((fd = socket(AF_UNIX, SOCK_STREAM, 0)) < 0) {
        printf("create socket failed\n");
        return 1;
    }

    size = offsetof(struct sockaddr_un, sun_path) + strlen(un.sun_path);
    if (bind(fd, (struct sockaddr *)&un, size) < 0) {
        printf("bind socket failed\n");
        return 2;
    }

    printf("UNIX domain socket bound\n");
    return 0;
}
