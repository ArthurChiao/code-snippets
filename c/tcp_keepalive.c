#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <unistd.h>

#define BUFFER_SIZE 1024
#define on_error(...) { fprintf(stderr, __VA_ARGS__); fflush(stderr); exit(1); }

int main (int argc, char *argv[]) {
    if (argc < 3) on_error("Usage: %s [port] [enable_keepalive_flag]\n", argv[0]);

    int port = atoi(argv[1]);
    int enable_keepalive = atoi(argv[2]);

    int server_fd, client_fd, err;
    struct sockaddr_in server, client;
    char buf[BUFFER_SIZE];

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) on_error("Could not create socket\n");

    server.sin_family = AF_INET;
    server.sin_port = htons(port);
    server.sin_addr.s_addr = htonl(INADDR_ANY);

    int opt_val = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt_val, sizeof opt_val);

    err = bind(server_fd, (struct sockaddr *) &server, sizeof(server));
    if (err < 0) on_error("Could not bind socket\n");

    err = listen(server_fd, 128);
    if (err < 0) on_error("Could not listen on socket\n");

    printf("Server is listening on %d\n", port);
    while (1) {
        int nodelay = 1;
        socklen_t client_len = sizeof(client);
        client_fd = accept(server_fd, (struct sockaddr *) &client, &client_len);

        if (client_fd < 0) on_error("Could not establish new connection\n");
        setsockopt(client_fd, IPPROTO_TCP, TCP_NODELAY, (void*)&nodelay, sizeof(int));

        if (enable_keepalive) { /* TCP Keepalive flags */
            int optval = 1;
            setsockopt(client_fd, SOL_SOCKET, SO_KEEPALIVE, (void*)&optval, sizeof(int));

            int idle = 600;
            setsockopt(client_fd, IPPROTO_TCP, TCP_KEEPIDLE, (void*)&idle, sizeof(int));

            int interval = 30;
            setsockopt(client_fd, IPPROTO_TCP, TCP_KEEPINTVL, (void*)&interval, sizeof(int));

            int count = 5;
            setsockopt(client_fd, IPPROTO_TCP, TCP_KEEPCNT, (void*)&count, sizeof(int));
        }

        printf("Get Client Connected!!!\n");
        while (1) {
            int read = recv(client_fd, buf, BUFFER_SIZE, 0);

            if (!read) break; // done reading
            if (read < 0) on_error("Client read failed\n");

            err = send(client_fd, buf, read, 0);
            if (err < 0) on_error("Client write failed\n");
            buf[read] = 0; // ternimate strings
            printf("GET: %s", buf);
        }
    }

    return 0;
}
