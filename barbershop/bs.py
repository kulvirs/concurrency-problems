# This implementation uses a synchronized queue to simulate the waiting room.
import threading
import time
import random
import queue

MAX_CUSTOMERS = 4   # Maximum number of customers that can be in the barbershop at the same time.
TOTAL_CUSTOMERS = 100  # Total number of customers that will arrive throughout the program.
NUM_TRIALS = 100

waitTimes = [0]*TOTAL_CUSTOMERS

def balk(i):
    #print("Customer", i, "balks.")
    return

def getHairCut(i):
    #print("Customer", i, "gets a haircut.")
    #time.sleep(0.001*random.randint(0,100)) # Simulate time to get a haircut.
    return

def cutHair():
    #time.sleep(0.001*random.randint(0,100)) # Simulate time to give a haircut.
    return

def barberThread(customer, barber, customerDone, barberDone):
    while True:
        customer.acquire()
        barber.release()
        cutHair()
        customerDone.acquire()
        barberDone.release()

def customerThread(i, waitingRoom, barberChair, customer, barber, customerDone, barberDone):
    #print("Customer", i, "enters the barbershop.")
    global waitTimes
    start = time.time()
    if not barberChair.acquire(False):
        try:
            waitingRoom.put(i, block=False)
            barberChair.acquire()
            waitingRoom.get()
        except queue.Full:
            balk(i)
            return

    customer.release()
    barber.acquire()
    end = time.time()
    getHairCut(i)
    customerDone.release()
    barberDone.acquire()
    barberChair.release()
    #print("Customer", i, "leaves the barbershop.")
    waitTimes[i] = end-start

def main():
    durations = [0]*NUM_TRIALS
    averageWaitTimes = [0]*NUM_TRIALS
    for j in range(NUM_TRIALS):
        waitingRoom = queue.Queue(MAX_CUSTOMERS-1)
        barberChair = threading.Lock()
        customer = threading.Semaphore(0)
        barber = threading.Semaphore(0)
        customerDone = threading.Semaphore(0)
        barberDone = threading.Semaphore(0)

        start = time.time()
        bThread = threading.Thread(target=barberThread, args=(customer, barber, customerDone, barberDone))
        # Make the barber a background thread so the main thread can exit even if it is still running.
        bThread.daemon = True
        bThread.start()

        customers = []
        for i in range(TOTAL_CUSTOMERS):
            #time.sleep(0.001*random.randint(0,100)) # Simulate random amount of time between customers arriving.
            cThread = threading.Thread(target=customerThread, args=(i, waitingRoom, barberChair, customer, barber, customerDone, barberDone))
            customers.append(cThread)
            cThread.start()
        
        for c in customers:
            c.join()

        end = time.time()
        durations[j] = end-start
        global waitTimes
        waitTimes = [value for value in waitTimes if value != 0]
        averageWaitTimes[j] = sum(waitTimes)/len(waitTimes)
        waitTimes = [0]*TOTAL_CUSTOMERS

    print("Average wait time:", sum(averageWaitTimes)/len(averageWaitTimes), "s")
    print("Average duration:", sum(durations)/len(durations), "s")

if __name__ == "__main__":
    main()