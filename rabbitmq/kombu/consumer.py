from kombu import Connection
import datetime
import time
import sys

if __name__ == '__main__':
    conn = Connection('amqp://guest:guest@192.168.1.1:5672//')
    simple_queue = conn.SimpleQueue('simple_queue')

    while True:
        try:
            message = simple_queue.get(block=False)
            print("received: %s" % message.payload)
            message.ack()
            time.sleep(1)
        except KeyboardInterrupt:
            print("Exit")
            break
        except:
            pass

    simple_queue.close()

