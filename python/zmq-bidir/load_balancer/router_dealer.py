# code from: http://zguide.zeromq.org/py:rtreq
#
# encoding: utf-8
#
#   Custom routing Router to Mama (ROUTER to REQ)
#
#   Author: Jeremy Avnet (brainsik) <spork(dash)zmq(at)theory(dot)org>
#

import time
import random
from threading import Thread

import zmq

import zhelpers

NBR_WORKERS = 10

def worker_thread(context=None):
    context = context or zmq.Context.instance()
    worker = context.socket(zmq.DEALER)

    zhelpers.set_id(worker)
    worker.connect("tcp://localhost:5671")

    total = 0
    while True:
        worker.send(b"ready")

        workload = worker.recv()
        finished = workload == b"END"
        if finished:
            print("Processing: %d tasks" % total)
            break
        total += 1

        time.sleep(0.1 * random.random())

context = zmq.Context.instance()
client = context.socket(zmq.ROUTER)
client.bind("tcp://*.5671")

for _ in range(NBR_WORKERS):
    Thread(target=worker_thread).start()

for _ in range(NBR_WORKERS * 10):
    address, empty, ready = client.recv_multipart()

    client.send_multipart([address, b'', b'This is workload'])

for _ in range(NBR_WORKERS):
    address, empty, ready = client.recv_multipart()
    client.send_multipart([address, b'', b'END'])
