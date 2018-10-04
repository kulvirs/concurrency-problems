# This is an implementation of the solution described in the Little Book of Semaphores.
import threading
import time
import random

MAX_CUSTOMERS = 4   # Maximum number of customers that can be in the barbershop at the same time.
TOTAL_CUSTOMERS = 10  # Total number of customers that will arrive throughout the program.

numCustomers = 0 # Keeps track of how many customers are currently in the barbershop.

def balk(i):
    print("Customer", i, "balks.")

def getHairCut(i):
    print("Customer", i, "gets a haircut.")
    time.sleep(0.001*random.randint(0,100)) # Simulate time to get a haircut.

def barberThread(customer, barber, customerDone, barberDone):
    while True:
        customer.acquire()
        barber.release()
        # cutHair() Time simulation is done by getHairCut()
        customerDone.acquire()
        barberDone.release()

def customerThread(i, mutex, customer, barber, customerDone, barberDone):
    global numCustomers
    mutex.acquire()
    if numCustomers == MAX_CUSTOMERS:
        mutex.release()
        balk(i)
        return
    numCustomers += 1
    print("Customer", i, "enters the barbershop.")
    mutex.release()

    customer.release()
    barber.acquire()
    getHairCut(i)
    customerDone.release()
    barberDone.acquire()

    mutex.acquire()
    numCustomers -= 1
    print("Customer", i, "leaves the barbershop.")
    mutex.release()

def main():
    mutex = threading.Lock()
    customer = threading.Semaphore(0)
    barber = threading.Semaphore(0)
    customerDone = threading.Semaphore(0)
    barberDone = threading.Semaphore(0)

    bThread = threading.Thread(target=barberThread, args=(customer, barber, customerDone, barberDone))
    # Make the barber a background thread so the main thread can exit even if it is still running.
    bThread.daemon = True
    bThread.start()

    for i in range(TOTAL_CUSTOMERS):
        time.sleep(0.001*random.randint(0,100)) # Simulate random amount of time between customers arriving.
        threading.Thread(target=customerThread, args=(i, mutex, customer, barber, customerDone, barberDone)).start()

if __name__ == "__main__":
    main()
