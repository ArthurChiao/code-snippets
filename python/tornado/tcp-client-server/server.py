"""
Simple TCP Server
"""
from tornado import ioloop
from tornado.tcpserver import TCPServer

class Server(TCPServer):
    def __init__(self, io_loop=None, **kwargs):
        TCPServer.__init__(self, io_loop=io_loop, **kwargs)

    def handle_stream(self, stream, address):
        """
        handle a new `.IOStream` from an incoming connection.

        Any subclass of TCPServer needs to implement this method
        """
        TCPConnection(stream, address, io_loop=self.io_loop)

class TCPConnection(object):
    def __init__(self, stream, address, io_loop):
        print("stream/address/ip_loop: ", stream, address, io_loop)
        self.io_loop = io_loop
        self.stream  = stream
        self.address = address
        self.delimiter = b'\r\n\r\n'
        self.stream.read_until(self.delimiter, self._on_message)

    def _on_message(self, data):
        def on_timeout():
            print("sending reply ...")
            self.write(b"Hello client!" + self.delimiter)
            print("reply finish")

        timeout = 2
        data = data.decode('latin1')
        print("received request: %s" % data)
        self.io_loop.add_timeout(self.io_loop.time() + timeout, on_timeout)

    def write(self, chunk, callback=None):
        if not self.stream.closed():
            self.stream.write(chunk)


def main():
    server = Server()
    server.listen(8001)
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
