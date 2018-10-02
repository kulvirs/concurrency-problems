# This is an implementation of the solution presented in the Little Book of Semaphores.
import threading
import time
import random

NUM_SERVINGS = 5 # Number of servings the pot can hold.
NUM_SAVAGES = 10
MAX_EATS = 4 # Maximum number of times each savage eats.

servings = 0 # Number of servings remaining in the pot.

def cook(emptyPot, fullPot):
    global servings
    while True:
        emptyPot.acquire()
        time.sleep(0.001*random.randint(0,300)) # Simulate time to fill up pot.
        servings = NUM_SERVINGS
        print("Cook refilled pot.", servings, "servings remaining.")
        fullPot.release()

def savage(i, emptyPot, fullPot, servingsMutex):
    global servings
    numEats = 0
    while numEats < MAX_EATS:
        servingsMutex.acquire()
        if servings == 0:   # Wake up cook to refill pot.
            emptyPot.release()
            fullPot.acquire()
        time.sleep(0.001*random.randint(0,100)) # Simulate time to get a serving from pot.
        servings -= 1
        print("Savage", i, "got a serving.", servings, "servings remaining.")
        servingsMutex.release()
        time.sleep(0.001*random.randint(0,200)) # Simulate time to eat serving.
        numEats += 1

def main():
    emptyPot = threading.Semaphore(0)
    fullPot = threading.Semaphore(0)
    servingsMutex = threading.Lock()

    cookThread = threading.Thread(target=cook, args=(emptyPot, fullPot))
    # Set the cook thread to run in the background so that main thread can exit even if cook is still running.
    cookThread.daemon = True 
    cookThread.start()

    for i in range(NUM_SAVAGES):
        threading.Thread(target=savage, args=(i, emptyPot, fullPot, servingsMutex)).start()

if __name__ == "__main__":
    main()