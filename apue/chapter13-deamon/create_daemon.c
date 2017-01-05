#include<stdio.h>
#include<stdlib.h>
#include<syslog.h>
#include<sys/resource.h>
#include<sys/types.h>
#include<sys/stat.h>
#include <unistd.h>
#include <signal.h>
#include <fcntl.h>

/**
 * create a deamon process
 *
 * 6 steps need to be taken to initialize a deamon process.
 * See comments in code. More info see APUE chapter 13.
 *
 * Deamon has no TTY, so the TTY column in `ps -efj` will be `?`
 *
 * Kernel space deamons with parent process ID 0.
 * User space deamon process is launched by `init` process, so their parent
 * process ID is 1.
 *
 * Compile: gcc bind_sock.c
 * Usage: ./a.out
 *         ps -efj | grep "a.out"
 */

void
daemonize(const char *cmd)
{
    int i, fd0, fd1, fd2;
    pid_t pid;
    struct rlimit rl;
    struct sigaction sa;

    /* clear file creation mask */
    umask(0);

    /* get max number of file descriptors */
    if (getrlimit(RLIMIT_NOFILE, &rl) < 0) {
        printf("%s: can not get file limit\n", cmd);
        return;
    }

    /* become a session leader to lose controlling TTY */
    if ((pid = fork()) < 0) {
        printf("%s: can not fork\n", cmd);
        return;
    }
    else if (pid != 0) { // parent process
        exit(0);
    }
    setsid();

    /* ensure future opens won't allocate controlling TTYs */
    sa.sa_handler = SIG_IGN;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    if (sigaction(SIGHUP, &sa, NULL) < 0) {
        printf("%s: can not ignore SIGHUP\n", cmd);
        return;
    }
    if ((pid = fork()) < 0) {
        printf("%s: can not fork 2\n", cmd);
        return;
    }
    else if (pid != 0) { // parent process
        exit(0);
    }

    /* change current working dir to root, so we won't prevent file systems
     * from being unmounted */
    if (chdir("/") < 0) {
        printf("%s: can not change dir to /\n", cmd);
        return;
    }

    /* close all open file descriptors */
    if (rl.rlim_max == RLIM_INFINITY) {
        rl.rlim_max = 1024;
    }
    for (i = 0; i < rl.rlim_max; i++) {
        close(i);
    }

    /* attach file descriptors 0, 1, 2 to /dev/null */
    fd0 = open("/dev/null", O_RDWR);
    fd1 = dup(fd0);
    fd2 = dup(fd0);

    /* initialize the log file */
    if (fd0 != 0 || fd1 != 1 || fd2 != 2) {
        syslog(LOG_ERR, "unexpected file descriptors %d %d %d\n",
                fd0, fd1, fd2);
        exit(1);
    }
}

int main(int argc, char *argv[])
{
    daemonize("test-deamon");

    sleep(10000);
}
