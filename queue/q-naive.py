# Naive implementation of a thread-safe queue.

import threading
import random
import time

ENQUEUES = 20 # Number of items that will be inserted in the queue.

class ThreadSafeQueue:
    def __init__(self):
        self.mutex = threading.Lock()
        self.li = []

    def enqueue(self, item):
        self.mutex.acquire()
        self.li.append(item)
        print(item, "was placed on the queue.")
        self.mutex.release()

    def dequeue(self):
        while True:
            self.mutex.acquire()
            if len(self.li) > 0:
                item = self.li.pop(0)
                print(item, "was removed from the queue.")
                self.mutex.release()
                return item
            else:
                self.mutex.release()

def producer(q, i):
    time.sleep(0.001*random.randint(0,100)) # Simulate time between placing operations on the queue.
    q.enqueue(i)

def consumer(q):
    dequeues = 0
    while dequeues < ENQUEUES:
        q.dequeue() 
        dequeues += 1

def main():
    q = ThreadSafeQueue()

    threading.Thread(target=consumer, args=(q,)).start()

    for i in range(ENQUEUES):
        threading.Thread(target=producer, args=(q,i)).start()

if __name__ == "__main__":
    main()