# This is an implementation of Tanenbaum's solution to the Dining Philosophers problem from the Little Book of Semaphores.
import threading
import time
import random

NUM_TRIALS = 100
NUM_PHILOSOPHERS = 5
MAX_HELPINGS = 100 # Maximum number of times each philosopher eats.

waitingTime = [0]*NUM_PHILOSOPHERS

def rightNeighbour(i):
    return (i-1) % NUM_PHILOSOPHERS

def leftNeighbour(i):
    return (i+1) % NUM_PHILOSOPHERS

def getForks(i, state, sem, mutex):
    mutex.acquire()
    state[i] = "hungry"
    #print("Philosopher", i, "is hungry.")
    test(i, state, sem)
    mutex.release()
    sem[i].acquire()

def putForks(i, state, sem, mutex):
    mutex.acquire()
    state[i] = "thinking"
    #print("Philosopher", i, "is thinking.")
    test(leftNeighbour(i), state, sem)
    test(rightNeighbour(i), state, sem)
    mutex.release()

def test(i, state, sem):
    if state[i] == "hungry" and state[leftNeighbour(i)] != "eating" and state[rightNeighbour(i)] != "eating":
        state[i] = "eating"
        #print("Philosopher", i, "is eating.")
        sem[i].release()

def philosopher(i, state, sem, mutex):
    global waitingTime
    numHelpings = 0
    while numHelpings < MAX_HELPINGS:
        #time.sleep(0.001*random.randint(0,100)) # Simulate thinking.
        startWaiting = time.time()
        getForks(i, state, sem, mutex)
        doneWaiting = time.time()
        #time.sleep(0.001*random.randint(0,100)) # Simulate eating.
        putForks(i, state, sem, mutex)
        numHelpings += 1
        waitingTime[i] += doneWaiting-startWaiting

def main():
    durations = [0]*NUM_TRIALS
    averageWaitingTime = [0]*NUM_TRIALS
    for j in range(NUM_TRIALS):
        state = ["thinking"]*NUM_PHILOSOPHERS
        sem = [threading.Semaphore(0) for i in range(NUM_PHILOSOPHERS)]
        mutex = threading.Lock()
        philosophers = []
        start = time.time()
        for i in range(NUM_PHILOSOPHERS):
                philosopherThread = threading.Thread(target=philosopher, args=(i, state, sem, mutex))
                philosophers.append(philosopherThread)
                philosopherThread.start()

        for philosopherThread in philosophers:
                philosopherThread.join()

        end = time.time()
        global waitingTime
        durations[j] = end-start
        averageWaitingTime[j] = sum(waitingTime)/len(waitingTime)
        waitingTime = [0]*NUM_TRIALS

    print("Average waiting time:", sum(averageWaitingTime)/len(averageWaitingTime), "s")
    print("Average duration:", sum(durations)/len(durations), "s")    

if __name__ == "__main__":
    main()
