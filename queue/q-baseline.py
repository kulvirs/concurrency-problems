import threading
import random
import time
import queue

ENQUEUES = 100 # Number of items that will be inserted in the queue.
NUM_TRIALS = 100

startTimes = [0]*ENQUEUES
endTimes = [0]*ENQUEUES

def producer(q, i):
    global startTimes
    startTimes[i] = time.time()
    q.put(i)

def consumer(q):
    global endTimes
    dequeues = 0
    while dequeues < ENQUEUES:
        i = q.get() 
        endTimes[i] = time.time()
        dequeues += 1

def main():
    durations = [0]*NUM_TRIALS
    averageWaitTimes = [0]*NUM_TRIALS
    for j in range(NUM_TRIALS):
        q = queue.Queue()

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