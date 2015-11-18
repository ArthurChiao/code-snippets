"""
Simple TCP Client
"""
import socket
import tornado.ioloop
import tornado.iostream

class TCPClient(object):
    def __init__(self, host, port, io_loop=None):
        self.host = host
        self.port = port
        self.io_loop = io_loop

        self.shutdown = False
        self.stream = None
        self.sock_fd = None
        self.delimiter = b'\r\n\r\n'

    def connect(self):
        self.sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.stream = tornado.iostream.IOStream(self.sock_fd)
        self.stream.set_close_callback(self.on_close)
        self.stream.connect((self.host, self.port), self.send_message)

    def on_receive(self, data):
        print("received: %s" % data)
        self.stream.close()

    def on_close(self):
        if self.shutdown:
            self.io_loop.stop()

    def send_message(self):
        print("sending request ...")
        self.stream.write(b"Hello Server!" + self.delimiter)
        self.stream.read_until(self.delimiter, self.on_receive)
        print("request finish")

    def set_shutdown(self):
        self.shutdown = True

def main():
    io_loop = tornado.ioloop.IOLoop.current()

    c1 = TCPClient("127.0.0.1", 8001, io_loop)
    c2 = TCPClient("127.0.0.1", 8001, io_loop)
    c1.connect()
    c2.connect()
    c2.set_shutdown()

    io_loop.start()

if __name__ == "__main__":
    main()
