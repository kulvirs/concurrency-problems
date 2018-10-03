# This is an implementation of Tanenbaum's solution to the Dining Philosophers problem from the Little Book of Semaphores.
import threading
import time
import random

NUM_PHILOSOPHERS = 5
MAX_HELPINGS = 2 # Maximum number of times each philosopher eats.

def rightNeighbour(i):
    return (i-1) % NUM_PHILOSOPHERS

def leftNeighbour(i):
    return (i+1) % NUM_PHILOSOPHERS

def getForks(i, state, sem, mutex):
    mutex.acquire()
    state[i] = "hungry"
    print("Philosopher", i, "is hungry.")
    test(i, state, sem)
    mutex.release()
    sem[i].acquire()

def putForks(i, state, sem, mutex):
    mutex.acquire()
    state[i] = "thinking"
    print("Philosopher", i, "is thinking.")
    test(leftNeighbour(i), state, sem)
    test(rightNeighbour(i), state, sem)
    mutex.release()

def test(i, state, sem):
    if state[i] == "hungry" and state[leftNeighbour(i)] != "eating" and state[rightNeighbour(i)] != "eating":
        state[i] = "eating"
        print("Philosopher", i, "is eating.")
        sem[i].release()

def philosopher(i, state, sem, mutex):
    numHelpings = 0
    while numHelpings < MAX_HELPINGS:
        time.sleep(0.001*random.randint(0,100)) # Simulate thinking.
        getForks(i, state, sem, mutex)
        time.sleep(0.001*random.randint(0,100)) # Simulate eating.
        putForks(i, state, sem, mutex)
        numHelpings += 1

def main():
    state = ["thinking"]*NUM_PHILOSOPHERS
    sem = [threading.Semaphore(0) for i in range(NUM_PHILOSOPHERS)]
    mutex = threading.Lock()

    for i in range(NUM_PHILOSOPHERS):
        threading.Thread(target=philosopher, args=(i, state, sem, mutex)).start()

if __name__ == "__main__":
    main()
