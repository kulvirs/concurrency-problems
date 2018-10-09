import threading
import random
import time

ENQUEUES = 20 # Number of items that will be inserted in the queue.

class ThreadSafeQueue():
    def __init__(self):
        self.li = []
        self.mutex = threading.Condition()

    def enqueue(self, item):
        with self.mutex:
            self.li.append(item)
            print(item, "was placed on the queue.")
            self.mutex.notify()

    def dequeue(self):
        with self.mutex:
            while len(self.li) == 0:
                self.mutex.wait()
            item = self.li.pop(0)
            print(item, "was removed from the queue.")
        return item

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