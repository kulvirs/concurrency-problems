# This implementation uses Python's syncronized queue.

from threading import Thread
import queue
import time
import random

BUF_LEN = 5
NUM_PRODUCERS = 50
NUM_CONSUMERS = 2
NUM_TRIALS = 100

startTimes = [0]*NUM_PRODUCERS
endTimes = [0]*NUM_PRODUCERS

def produceEvent(event):
    time.sleep(0.001*random.randint(0,100)) # Simulate producing event.

def consumeEvent(event):
    time.sleep(0.001*random.randint(0,100)) # Simulate consuming event.

def producer(event, buffer):
    global startTimes
    if event is not None:
        #produceEvent(event)
        startTimes[event] = time.time()
    buffer.put(event)
    # if event is not None:
    #     print("Event", event, "placed on buffer.")

def consumer(buffer):
    global endTimes
    while True:
        event = buffer.get()
        if event is None:
            break
        # print("Event", event, "removed from buffer.")
        endTimes[event] = time.time()
        # consumeEvent(event)
        
def main():
    averageDurations = [0]*NUM_TRIALS
    averageWaitTimes = [0]*NUM_TRIALS
    for j in range(NUM_TRIALS):
        buffer = queue.Queue(BUF_LEN) # Finite-sized buffer.

        start = time.time()
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
        end = time.time()

        global startTimes
        global endTimes
        waitTimes = [endTimes[i] - startTimes[i] for i in range(NUM_PRODUCERS)]
        averageWaitTimes[j] = sum(waitTimes)/len(waitTimes)
        averageDurations[j] = end-start

    print("Average wait time:", sum(averageWaitTimes)/len(averageWaitTimes), "s")
    print("Average duration:", sum(averageDurations)/len(averageDurations), "s")


if __name__ == "__main__":
    main()


