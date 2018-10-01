# This is an implementation of Tanenbaum's solution to the Dining Philosophers problem from the Little Book of Semaphores.
import threading
import time
import random

NUM_PHILOSOPHERS = 5
MAX_EATS = [2]*NUM_PHILOSOPHERS

def right(i):
    return i

def left(i):
    return (i+1) % NUM_PHILOSOPHERS

def get_forks(i, state, sem, mutex):
    mutex.acquire()
    state[i] = 'hungry'
    print("Philosopher", i, "is hungry.")
    test(i, state, sem)
    mutex.release()
    sem[i].acquire()

def put_forks(i, state, sem, mutex):
    mutex.acquire()
    state[i] = 'thinking'
    print("Philosopher", i, "is thinking.")
    test(left(i), state, sem)
    test(right(i), state, sem)
    mutex.release()

def test(i, state, sem):
    if state[i] == 'hungry' and state[left(i)] != 'eating' and state[right(i)] != 'eating':
        state[i] = 'eating'
        print("Philosopher", i, "is eating.")
        sem[i].release()

def philosopher(i, state, sem, mutex):
    numEats = 0
    while numEats < MAX_EATS[i]:
        time.sleep(0.001*random.randint(0,100)) # Simulate thinking.
        get_forks(i, state, sem, mutex)
        time.sleep(0.001*random.randint(0,100)) # Simulate eating.
        put_forks(i, state, sem, mutex)
        numEats += 1

def main():
    state = ['thinking']*NUM_PHILOSOPHERS
    sem = [threading.Semaphore(0) for i in range(NUM_PHILOSOPHERS)]
    mutex = threading.Lock()

    for i in range(NUM_PHILOSOPHERS):
        threading.Thread(target=philosopher, args=(i, state, sem, mutex)).start()

if __name__ == "__main__":
    main()
