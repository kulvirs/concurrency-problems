# This is an implementation of the solution from the Little Book of Semaphores.
import threading
import random
import time

NUM_EMPLOYEES = 10 # Total number of employees that will arrive.

class LightSwitch:
    def __init__(self):
        self.counter = 0
        self.mutex = threading.Lock()

    def lock(self, semaphore):
        self.mutex.acquire()
        self.counter += 1
        if self.counter == 1:
            semaphore.acquire()
        self.mutex.release()

    def unlock(self, semaphore):
        self.mutex.acquire()
        self.counter -= 1
        if self.counter == 0:
            semaphore.release()
        self.mutex.release()

def maleEmployee(i, empty, maleSwitch, maleMultiplex):
    print("Male employee", i, "arrives.")
    maleSwitch.lock(empty)
    maleMultiplex.acquire()
    print("Male employee", i, "enters the bathroom.")
    time.sleep(0.001*random.randint(0,100)) # Simulate time to use the bathroom.
    print("Male employee", i, "leaves the bathroom.")
    maleMultiplex.release()
    maleSwitch.unlock(empty)

def femaleEmployee(i, empty, femaleSwitch, femaleMultiplex):
    print("Female employee", i, "arrives.")
    femaleSwitch.lock(empty)
    femaleMultiplex.acquire()
    print("Female employee", i, "enters the bathroom.")
    time.sleep(0.001*random.randint(0,100)) # Simulate time to use the bathroom.
    print("Female employee", i, "leaves the bathroom.")
    femaleMultiplex.release()
    femaleSwitch.unlock(empty)

def main():
    empty = threading.Lock()
    maleSwitch = LightSwitch()
    femaleSwitch = LightSwitch()
    maleMultiplex = threading.Semaphore(3)
    femaleMultiplex = threading.Semaphore(3)

    for i in range(NUM_EMPLOYEES):
        time.sleep(0.001*random.randint(0,100)) # Simulate time between employees arriving.
        employeeThread = threading.Thread(target=maleEmployee, args=(i, empty, maleSwitch, maleMultiplex)) if random.randint(0,1) == 0 else threading.Thread(target=femaleEmployee, args=(i, empty, femaleSwitch, femaleMultiplex))
        employeeThread.start()

if __name__ == "__main__":
    main()

