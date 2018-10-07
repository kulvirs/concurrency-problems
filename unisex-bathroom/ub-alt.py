import queue 
import random
import threading
import time

EMPTY = 0
MALE = 1
FEMALE = 2
NUM_EMPLOYEES = 10

mode = EMPTY
femaleCounter = 0
maleCounter = 0
maleWaiting = False
femaleWaiting = True

def maleEmployee(i, maleMultiplex, condition):
    global mode
    global maleCounter
    global maleWaiting
    global femaleWaiting

    print("Male employee", i, "arrives.")
    maleMultiplex.acquire()
    with condition:
        while mode == FEMALE:
            maleWaiting = True
            condition.wait()
        maleWaiting = False
        mode = MALE
        maleCounter += 1

    print("Male employee", i, "enters the bathroom.")
    time.sleep(0.001*random.randint(0,100)) # Simulate time to use the bathroom.

    with condition:
        maleCounter -= 1
        if maleCounter == 0:
            if femaleWaiting:
                mode = FEMALE
                condition.notify_all()
            else:
                mode = EMPTY

    maleMultiplex.release()
    print("Male employee", i, "leaves the bathroom.")

def femaleEmployee(i, femaleMultiplex, condition):
    global mode
    global femaleCounter
    global maleWaiting
    global femaleWaiting

    print("Female employee", i, "arrives.")
    femaleMultiplex.acquire()
    with condition:
        while mode == MALE:
            femaleWaiting = True
            condition.wait()
        femaleWaiting = False
        mode = FEMALE
        femaleCounter += 1

    print("Female employee", i, "enters the bathroom.")
    time.sleep(0.001*random.randint(0,100)) # Simulate time to use the bathroom.

    with condition:
        femaleCounter -= 1
        if femaleCounter == 0:
            if maleWaiting:
                mode = MALE
                condition.notify_all()
            else:
                mode = EMPTY

    femaleMultiplex.release()
    print("Female employee", i, "leaves the bathroom.")

def main():
    femaleMultiplex = threading.Semaphore(3)
    maleMultiplex = threading.Semaphore(3)
    condition = threading.Condition()

    for i in range(NUM_EMPLOYEES):
        time.sleep(0.001*random.randint(0,100)) # Simulate time between employees arriving.
        employeeThread = threading.Thread(target=maleEmployee, args=(i, maleMultiplex, condition)) if random.randint(0,1) == 0 else threading.Thread(target=femaleEmployee, args=(i, femaleMultiplex, condition))
        employeeThread.start()

if __name__ == "__main__":
    main()