import queue 
import random
import threading
import time

# Constants to keep track of the current mode.
EMPTY = 0
MALE = 1
FEMALE = 2

NUM_EMPLOYEES = 100 # Maximum number of employees that will arrive.
NUM_TRIALS = 100

mode = EMPTY
counter = 0
maleWaiting = False
femaleWaiting = False
waitingTimes = [0]*NUM_EMPLOYEES

def maleEmployee(i, maleMultiplex, condition):
    global mode, counter, maleWaiting, femaleWaiting, waitingTimes

    #time.sleep(0.001*random.randint(0,100)) # Simulate time between employees arriving.
    #print("Male employee", i, "arrives.")
    start = time.time()
    maleMultiplex.acquire()
    with condition:
        if mode == MALE and femaleWaiting:
            maleWaiting = True
            condition.wait()
        while mode == FEMALE:
            maleWaiting = True
            condition.wait()
        maleWaiting = False
        mode = MALE
        counter += 1

    end = time.time()
    #print("Male employee", i, "enters the bathroom.")
    #time.sleep(0.001*random.randint(0,100)) # Simulate time to use the bathroom.

    with condition:
        counter -= 1
        if counter == 0:
            if femaleWaiting:
                mode = FEMALE
                condition.notify_all()
            else:
                mode = EMPTY

    maleMultiplex.release()
    #print("Male employee", i, "leaves the bathroom.")
    waitingTimes[i] = end-start

def femaleEmployee(i, femaleMultiplex, condition):
    global mode, counter, maleWaiting, femaleWaiting, waitingTimes

    #time.sleep(0.001*random.randint(0,100)) # Simulate time between employees arriving.
    #print("Female employee", i, "arrives.")
    start = time.time()
    femaleMultiplex.acquire()
    with condition:
        if mode == FEMALE and maleWaiting:
            femaleWaiting = True
            condition.wait()
        while mode == MALE:
            femaleWaiting = True
            condition.wait()
        femaleWaiting = False
        mode = FEMALE
        counter += 1

    end = time.time()
    #print("Female employee", i, "enters the bathroom.")
    #time.sleep(0.001*random.randint(0,100)) # Simulate time to use the bathroom.

    with condition:
        counter -= 1
        if counter == 0:
            if maleWaiting:
                mode = MALE
                condition.notify_all()
            else:
                mode = EMPTY

    femaleMultiplex.release()
    #print("Female employee", i, "leaves the bathroom.")
    waitingTimes[i] = end-start

def main():
    durations = [0]*NUM_TRIALS
    averageWaitingTimes = [0]*NUM_TRIALS
    for j in range(NUM_TRIALS):
        femaleMultiplex = threading.Semaphore(3)
        maleMultiplex = threading.Semaphore(3)
        condition = threading.Condition()

        start = time.time()
        employees = []
        for i in range(0, NUM_EMPLOYEES, 2):
            mEmployee = threading.Thread(target=maleEmployee, args=(i, maleMultiplex, condition))
            employees.append(mEmployee)
            mEmployee.start()
            fEmployee = threading.Thread(target=femaleEmployee, args=(i+1, femaleMultiplex, condition))
            employees.append(fEmployee)
            fEmployee.start()
        
        for thread in employees:
            thread.join()
        end = time.time()
        durations[j] = end-start
        global mode, counter, maleWaiting, femaleWaiting, waitingTimes
        averageWaitingTimes[j] = sum(waitingTimes)/len(waitingTimes)
        waitingTimes = [0]*NUM_EMPLOYEES
        mode = EMPTY
        counter = 0
        maleWaiting = False
        femaleWaiting = False

    print("Average wait time:", sum(averageWaitingTimes)/len(averageWaitingTimes), "s")
    print("Average duration:", sum(durations)/len(durations), "s")

if __name__ == "__main__":
    main()