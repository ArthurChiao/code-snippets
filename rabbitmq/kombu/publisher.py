from kombu import Connection
import datetime
import time

if __name__ == '__main__':
    conn = Connection('amqp://guest:guest@192.168.1.1:5672//')
    simple_queue = conn.SimpleQueue('simple_queue')

    # send an test message
    warm_up_time = 100
    while warm_up_time > 0:
        message = 'hello, sent at %s' % datetime.datetime.today()
        simple_queue.put(message)
        print("sent: %s" % message)

        time.sleep(1)
        warm_up_time = warm_up_time - 1

    # sleep some time, no message out
    print("\n")
    sleep_time = 90 * 60  # half an hour
    while sleep_time > 0:
        print("will send message in %d seconds later..." % sleep_time)
        time.sleep(1)
        sleep_time = sleep_time - 1

    # back to sending again
    print("\n")
    while True:
        message = 'hello, sent at %s' % datetime.datetime.today()
        simple_queue.put(message)
        print("sent: %s" % message)
        time.sleep(2)

    simple_queue.close()

