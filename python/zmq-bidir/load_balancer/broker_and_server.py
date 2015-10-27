"""
broker_and_server.py

implement bi-direction peer communication with DEALER/ROUTER

Author: Yanan Zhao <ya_nanzhao@hotmail.com>
Date  : 2015-10-27
"""
import multiprocessing
import time

import zmq

NBR_WORKERS = 1

def worker_task(ident):
    """Worker task, using a REQ socket to do load-balancing."""
    socket = zmq.Context().socket(zmq.REQ)
    socket.identity = u"Worker-{}".format(ident).encode("ascii")
    socket.connect("ipc://backend.ipc")

    # Tell broker we're ready for work
    socket.send(b"READY")

    while True:
        address, empty, request = socket.recv_multipart()
        print("@server: recvd {}: {}".format(socket.identity.decode("ascii"),
                              request.decode("ascii")))
        socket.send_multipart([address, b"", b"OK"])

def main():
    """Load balancer main loop."""
    # Prepare context and sockets
    context = zmq.Context.instance()
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://*:5559")
    backend = context.socket(zmq.ROUTER)
    backend.bind("ipc://backend.ipc")

    # Start background tasks
    def start(task, *args):
        process = multiprocessing.Process(target=task, args=args)
        process.daemon = True
        process.start()
    for i in range(NBR_WORKERS):
        start(worker_task, i)

    poller = zmq.Poller()
    poller.register(backend, zmq.POLLIN)
    poller.register(frontend, zmq.POLLIN)

    while True:
        sockets = dict(poller.poll())

        if backend in sockets:
            # Handle worker activity on the backend
            request = backend.recv_multipart()
            worker, empty, client = request[:3]
            # if not workers:
            #     # Poll for clients now that a worker is available
            #     poller.register(frontend, zmq.POLLIN)
            # workers.append(worker)
            # if client != b"READY" and len(request) > 3:
            #     # If client reply, send rest back to frontend
            #     empty, reply = request[3:]
            #     frontend.send_multipart([client, b"", reply])

        if frontend in sockets:
            # Get next client request, route to last-used worker
            client, empty, request = frontend.recv_multipart()

            # process request in some routines

            # send confirmation
            frontend.send_multipart([client, b"", b"UL success confirm"])

    # Clean up
    backend.close()
    frontend.close()
    context.term()

if __name__ == "__main__":
    main()
