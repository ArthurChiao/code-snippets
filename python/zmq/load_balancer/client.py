"""
client.py

implement bi-direction peer communication with DEALER/ROUTER

Author: Yanan Zhao <ya_nanzhao@hotmail.com>
Date  : 2015-10-27
"""
import sys
import time

import zmq

def client_task(ident):
    """Basic request-reply client using REQ socket."""
    socket = zmq.Context().socket(zmq.REQ)
    socket.identity = u"Client-{}".format(ident).encode("ascii")
    socket.connect("tcp://localhost:5559")

    # Send request, get reply
    while True:
        socket.send(b"HELLO")
        reply = socket.recv()
        print("@client: recvd {}: {}".format(socket.identity.decode("ascii"),
                              reply.decode("ascii")))
        time.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client <client id>")
        raise SystemExit

    client_id = int(sys.argv[1])
    client_task(client_id)
