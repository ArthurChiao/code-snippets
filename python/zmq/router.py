"""
router.py

implement bi-direction peer communication with DEALER/ROUTER

Author: Yanan Zhao <ya_nanzhao@hotmail.com>
Date  : 2015-10-26
"""
import time
from threading import Thread

import zmq

def send_data(context=None):
    """
    thread that needs to send data to peer periodically
    """
    context = zmq.Context() if context is None else context
    sock = context.socket(zmq.REQ)
    sock.connect("inproc://server-backend")

    while True:
        sock.send(b"world")
        sock.recv()
        print("@server_send_data: send & recv finish")
        time.sleep(2)

def dealer(context=None):
    context = zmq.Context() if context is None else context
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://*:5559")

    backend = context.socket(zmq.ROUTER)
    backend.bind("inproc://server-backend")

    poller = zmq.Poller()
    poller.register(frontend, zmq.POLLIN)
    poller.register(backend, zmq.POLLIN)

    while True:
        socks = dict(poller.poll(1000))

        if socks.get(frontend) == zmq.POLLIN:
            msg = frontend.recv_multipart()
            print("recv msg from client: ")
            print(msg)
            backend.send_multipart(msg)
        elif socks.get(backend) == zmq.POLLIN:
            msg = backend.recv_multipart()
            print("send server msg to client: ")
            print(msg)
            frontend.send_multipart(msg)


if __name__ == '__main__':
    context = zmq.Context()

    t1 = Thread(target=dealer, args=(context,))
    t2 = Thread(target=send_data, args=(context,))
    t1.deamon = True
    t2.deamon = True
    t1.start()
    t2.start()

    t1.join()
    t2.join()
