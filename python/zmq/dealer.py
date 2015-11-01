"""
dealer.py

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
    sock.connect("inproc://client-backend")

    while True:
        sock.send(b"hello")
        sock.recv()
        print("@client_send_data: send & recv finish")
        time.sleep(1)

def dealer(context=None):
    context = zmq.Context() if context is None else context
    frontend = context.socket(zmq.DEALER)
    frontend.connect("tcp://localhost:5559")

    backend = context.socket(zmq.ROUTER)
    backend.bind("inproc://client-backend")

    poller = zmq.Poller()
    poller.register(frontend, zmq.POLLIN)
    poller.register(backend, zmq.POLLIN)

    while True:
        socks = dict(poller.poll(1000))

        if socks.get(frontend) == zmq.POLLIN:
            msg = frontend.recv_multipart()
            print("recv msg from server: ")
            print(msg)
            backend.send_multipart(msg)
        elif socks.get(backend) == zmq.POLLIN:
            msg = backend.recv_multipart()
            print("send client msg to server: ")
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
