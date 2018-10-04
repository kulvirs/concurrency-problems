# This implementation uses Python's synchronized queue. 
import queue
import threading
import time
import random

MAX_CUSTOMERS = 4   # Maximum number of customers that can be in the barbershop at the same time.
TOTAL_CUSTOMERS = 10  # Total number of customers that will arrive throughout the program.

def balk(i):
    print("Customer", i, "balks.")

def getHairCut(i):
    print("Customer", i, "gets a haircut.")
    time.sleep(0.001*random.randint(0,100)) # Simulate time to get a haircut.

def barberThread(q, barber, barberDone):
    while True:
        customer, customerDone = q.get()
        customer.release()
        barber.release()
        # cutHair() time simulation is done by getHairCut()
        customerDone.acquire()
        barberDone.release()

def customerThread(i, q, barber, barberDone):
    try:
        customer = threading.Semaphore(0)
        customerDone = threading.Semaphore(0)
        q.put((customer, customerDone), block=False)
        print("Customer", i, "enters the barbershop.")
        customer.acquire()
        barber.acquire()
        getHairCut(i)
        customerDone.release()
        barberDone.acquire()
    except queue.Full:
        balk(i)
        return

def main():
    q = queue.Queue(MAX_CUSTOMERS-1)
    barber = threading.Semaphore(0)
    barberDone = threading.Semaphore(0)

    bThread = threading.Thread(target=barberThread, args=(q, barber, barberDone))
    # Make the barber a background thread so the main thread can exit even if it is still running.
    bThread.daemon = True
    bThread.start()

    for i in range(TOTAL_CUSTOMERS):
        time.sleep(0.001*random.randint(0,100)) # Simulate random amount of time between customers arriving.
        threading.Thread(target=customerThread, args=(i, q, barber, barberDone)).start()


if __name__ == "__main__":
    main()