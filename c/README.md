C Code Snippets
================

1. [TCP Keepalive](tcp_keepalive.c)

  Test [TCP Keepalive](http://www.tldp.org/HOWTO/html_single/TCP-Keepalive-HOWTO/) property.

  ```shell
  $ gcc -o keepalive tcp_keepalive.c

  # start server
  $ ./keepalive 8000 1 # use keepalive
  $ ./keepalive 8000 0 # do not use keepalive

  # connect to server
  $ telnet <server ip> 8000
  ```
