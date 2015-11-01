"""
code from: http://zguide.zeromq.org/py:mtserver

Multithreaded Hello World server

Author: Guillaume Aubert (gaubert) <guillaume(dot)aubert(at)gmail(dot)com>
"""
import time
import threading
import zmq

def worker_routine(worker_url, context=None):
    context = context or zmq.context.instance()
    socket = context.socket(zmq.REP)
    socket.connect(worker_url)

    while True:
        string = socket.recv()
        print("Received request: [%s]" string)

        time.sleep(1)

        socket.send(b"World")

def main():
    """Server routine"""
    url_worker = "inproc://workers"
    url_client = "tcp://*.5555"

    context = zmq.context.instance()

    clients = context.socket(zmq.ROUTER)
    clients.bind(url_client)

    workers = context.socket(zmq.DEALER)
    workers.bind(url_worker)

    for i in range(5):
        threading.Thread(target=worker_routine, args=(worker_url,)).start()

    zmq.device(zmq.QUEUE, clients, workers)

    # we never get there but cleanup anyhow
    clients.close()
    workers.close()
    context.term()


if __name__ == '__main__':
    main()

