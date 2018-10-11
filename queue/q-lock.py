# Naive implementation of a thread-safe queue.

import threading
import random
import time

ENQUEUES = 100 # Number of items that will be inserted in the queue.
NUM_TRIALS = 100

startTimes = [0]*ENQUEUES
endTimes = [0]*ENQUEUES

class ThreadSafeQueue:
    def __init__(self):
        self.mutex = threading.Lock()
        self.li = []

    def enqueue(self, item):
        global startTimes
        startTimes[item] = time.time()
        self.mutex.acquire()
        self.li.append(item)
        #print(item, "was placed on the queue.")
        self.mutex.release()

    def dequeue(self):
        global endTimes
        while True:
            self.mutex.acquire()
            if len(self.li) > 0:
                item = self.li.pop(0)
                endTimes[item] = time.time()
                #print(item, "was removed from the queue.")
                self.mutex.release()
                return item
            else:
                self.mutex.release()

def producer(q, i):
    #time.sleep(0.001*random.randint(0,100)) # Simulate time between placing operations on the queue.
    q.enqueue(i)

def consumer(q):
    dequeues = 0
    while dequeues < ENQUEUES:
        q.dequeue() 
        dequeues += 1

def main():
    durations = [0]*NUM_TRIALS
    averageWaitTimes = [0]*NUM_TRIALS
    for j in range(NUM_TRIALS):
        q = ThreadSafeQueue()

        start = time.time()
        threads = []
        consumerThread = threading.Thread(target=consumer, args=(q,))
        threads.append(consumerThread)
        consumerThread.start()

        for i in range(ENQUEUES):
            producerThread = threading.Thread(target=producer, args=(q,i))
            threads.append(producerThread)
            producerThread.start()

        for thread in threads:
            thread.join()
        end = time.time()

        durations[j] = end-start
        global startTimes, endTimes
        waitTimes = [endTimes[j] - startTimes[j] for j in range(ENQUEUES)]
        averageWaitTimes[j] = sum(waitTimes)/len(waitTimes)
    
    print("Average wait time:", sum(averageWaitTimes)/len(averageWaitTimes), "s")
    print("Average duration:", sum(durations)/len(durations), "s")

if __name__ == "__main__":
    main()