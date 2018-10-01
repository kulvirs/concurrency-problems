# This implementation uses Python's syncronized queue.

from threading import Thread
import queue
import time
import random

BUF_LEN = 5
NUM_PRODUCERS = 10
NUM_CONSUMERS = 1

def produceEvent(event):
    time.sleep(0.001*random.randint(0,100)) # Simulate producing event.
    print("Produced event", event)

def consumeEvent(event):
    time.sleep(0.001*random.randint(0,100)) # Simulate consuming event.
    print("Consumed event", event)

def producer(event, buffer):
    if event is not None:
        produceEvent(event)
    buffer.put(event)

def consumer(buffer):
    while True:
        event = buffer.get()
        if event is None:
            break
        consumeEvent(event)
        
def main():
    buffer = queue.Queue(BUF_LEN) # Finite-sized buffer.
    
    consumerThreads = []
    for i in range(NUM_CONSUMERS):
        consumerThread = Thread(target=consumer, args=(buffer,))
        consumerThreads.append(consumerThread)
        consumerThread.start()

    producerThreads = []
    for i in range(NUM_PRODUCERS):
        producerThread = Thread(target=producer, args=(i,buffer))
        producerThreads.append(producerThread)
        producerThread.start()

    for thread in producerThreads:
        thread.join()
    
    for i in range(NUM_CONSUMERS):
        Thread(target=producer, args=(None,buffer)).start()

    for thread in consumerThreads:
        thread.join()

if __name__ == "__main__":
    main()


