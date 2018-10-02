# This is an implementation of the solution from the Little Book of Semaphores using semaphores and mutices. 

import threading
import time
import random

NUM_CONSUMERS = 1
NUM_PRODUCERS = 10
BUF_LEN = 2

def produceEvent(event):
    time.sleep(0.001*random.randint(0,100)) # Simulate producing event.
    print("Produced event", event)

def consumeEvent(event):
    time.sleep(0.001*random.randint(0,100)) # Simulate consuming event.
    print("Consumed event", event)

def producer(event, buffer, mutex, items, spaces):
    if event is not None:
        produceEvent(event)
    spaces.acquire()
    mutex.acquire() 
    buffer.append(event)
    mutex.release()
    items.release()

def consumer(buffer, mutex, items, spaces):
    while True:
        items.acquire()
        mutex.acquire()
        event = buffer.pop(0)
        mutex.release()
        spaces.release()
        if event is None:
            break
        consumeEvent(event)

def main():
    buffer = []
    mutex = threading.Lock() # Provides exclusive access to buffer.
    items = threading.Semaphore(0) # Indicates whether there are items in the buffer.
    spaces = threading.Semaphore(BUF_LEN) # Indicates number of available spaces in the buffer.

    consumerThreads = []
    for i in range(NUM_CONSUMERS):
        consumerThread = threading.Thread(target=consumer, args=(buffer, mutex, items, spaces))
        consumerThreads.append(consumerThread)
        consumerThread.start()

    producerThreads = []
    for i in range(NUM_PRODUCERS):
        producerThread = threading.Thread(target=producer, args=(i, buffer, mutex, items, spaces))
        producerThreads.append(producerThread)
        producerThread.start()

    for thread in producerThreads:
        thread.join()
    
    for i in range(NUM_CONSUMERS):
        threading.Thread(target=producer, args=(None, buffer, mutex, items, spaces)).start()

    for thread in consumerThreads:
        thread.join()

if __name__ == "__main__":
    main()