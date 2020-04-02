#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <time.h>
#include <string.h>

void
print_usage(char *prog) {
	printf("Ping-pong a byte between two processes via a pair of pipes.\n");
	printf("Usage: %s [-v]\n", prog);
}

int
main(int argc, char* argv[]) {
    if (argc != 1 && argc != 2) {
		print_usage(argv[0]);
        exit(0);
    }

    int verbose = 0;
    if (argc == 2) {
        if (!strcmp(argv[1], "-h")) {
            print_usage(argv[0]);
            exit(0);
        }

        if (!strcmp(argv[1], "-v")) {
            verbose = 1;
            printf("Verbose output enabled\n");
        } else {
            printf("Invalid argv[1]: %s\n", argv[1]);
            print_usage(argv[0]);
            exit(0);
        }
    }

    char c = 'a';
    int pipe1_fds[2];
    int pipe2_fds[2];

    if (pipe(pipe1_fds) == -1 || pipe(pipe2_fds) == -1) {
        perror("Create pipe failed");
        exit(-1);
    }

    if (fork() == 0) { // Child process
        if (write(pipe2_fds[1], &c, 1) != 1) {
            perror("First time write failed");
            exit(-2);
        }

        printf("Ping-Pong started, Ping out\n");

        int iter = 0;
        time_t start = clock();

        while (read(pipe1_fds[0], &c, 1) == 1) {
            if (write(pipe2_fds[1], &c, 1) != 1) {
                exit(-3);
            }

            if (verbose) {
                printf("Ping out\n");
            }

            iter++;
            if (iter % 10000 == 0) {
                double elapsed = (clock() - start) / 1000000.0; // seconds
                printf("Performance: %.2f round/second\n", iter/elapsed);
            }
        }

        perror("Read from pipe1 failed");
        exit(-4);
    } else { // Parent process
        char c2;
        while (read(pipe2_fds[0], &c2, 1) == 1) {
            if (write(pipe1_fds[1], &c2, 1) != 1) {
                exit(-5);
            }

            if (verbose) {
                printf("Pong out\n");
            }
        }

        perror("Read from pipe2 failed");
        exit(-6);
    }
}
