# This is an implementation of the solution from the Little Book of Semaphores.
import threading
import random
import time

NUM_EMPLOYEES = 100 # Total number of employees that will arrive.
NUM_TRIALS = 100

waitingTimes = [0]*NUM_EMPLOYEES

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
    #time.sleep(0.001*random.randint(0,100)) # Simulate time between employees arriving.
    #print("Male employee", i, "arrives.")
    global waitingTimes
    start = time.time()
    maleSwitch.lock(empty)
    maleMultiplex.acquire()
    end = time.time()
    #print("Male employee", i, "enters the bathroom.")
    #time.sleep(0.001*random.randint(0,100)) # Simulate time to use the bathroom.
    #print("Male employee", i, "leaves the bathroom.")
    maleMultiplex.release()
    maleSwitch.unlock(empty)
    waitingTimes[i] = end-start

def femaleEmployee(i, empty, femaleSwitch, femaleMultiplex):
    global waitingTimes
    #time.sleep(0.001*random.randint(0,100)) # Simulate time between employees arriving.
    #print("Female employee", i, "arrives.")
    start = time.time()
    femaleSwitch.lock(empty)
    femaleMultiplex.acquire()
    end = time.time()
    #print("Female employee", i, "enters the bathroom.")
    #time.sleep(0.001*random.randint(0,100)) # Simulate time to use the bathroom.
    #print("Female employee", i, "leaves the bathroom.")
    femaleMultiplex.release()
    femaleSwitch.unlock(empty)
    waitingTimes[i] = end-start

def main():
    durations = [0]*NUM_TRIALS
    averageWaitingTimes = [0]*NUM_TRIALS

    for j in range(NUM_TRIALS):
        empty = threading.Lock()
        maleSwitch = LightSwitch()
        femaleSwitch = LightSwitch()
        maleMultiplex = threading.Semaphore(3)
        femaleMultiplex = threading.Semaphore(3)

        start = time.time()
        employees = []
        for i in range(0, NUM_EMPLOYEES, 2):
            mEmployee = threading.Thread(target=maleEmployee, args=(i, empty, maleSwitch, maleMultiplex))
            employees.append(mEmployee)
            mEmployee.start()
            fEmployee = threading.Thread(target=femaleEmployee, args=(i+1, empty, femaleSwitch, femaleMultiplex))
            employees.append(fEmployee)
            fEmployee.start()

        for thread in employees:
            thread.join()
        end = time.time()

        global waitingTimes
        durations[j] = end - start
        averageWaitingTimes[j] = sum(waitingTimes)/len(waitingTimes)
        waitingTimes = [0]*NUM_EMPLOYEES
    
    print("Average wait time:", sum(averageWaitingTimes)/len(averageWaitingTimes), "s")
    print("Average duration:", sum(durations)/len(durations), "s")
        

if __name__ == "__main__":
    main()

