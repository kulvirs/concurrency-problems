# This is an implementation of the solution presented in the Little Book of Semaphores.
import threading
import time
import random

MAX_SERVINGS = 5 # Maximum number of servings the pot can hold.
NUM_SAVAGES = 10
MAX_HELPINGS = 4 # Maximum number of times each savage eats.

numServings = 0 # Number of servings remaining in the pot.

def cook(emptyPot, fullPot):
    global numServings
    while True:
        emptyPot.acquire()
        time.sleep(0.001*random.randint(0,100)) # Simulate time to fill up pot.
        numServings = MAX_SERVINGS
        print("Cook refills the pot.", numServings, "servings remaining.")
        fullPot.release()

def savage(i, emptyPot, fullPot, servingsMutex):
    global numServings
    numHelpings = 0
    while numHelpings < MAX_HELPINGS:
        servingsMutex.acquire()
        if numServings == 0:   # Wake up cook to refill pot.
            emptyPot.release()
            fullPot.acquire()
        time.sleep(0.001*random.randint(0,100)) # Simulate time to get a serving from pot.
        numServings -= 1
        print("Savage", i, "takes a serving from the pot.", numServings, "servings remaining.")
        servingsMutex.release()
        time.sleep(0.001*random.randint(0,100)) # Simulate time to eat serving.
        numHelpings += 1

def main():
    emptyPot = threading.Semaphore(0)
    fullPot = threading.Semaphore(0)
    servingsMutex = threading.Lock()

    cookThread = threading.Thread(target=cook, args=(emptyPot, fullPot))
    # Set the cook thread to run in the background so that the main thread can exit even if cook is still running.
    cookThread.daemon = True 
    cookThread.start()

    for i in range(NUM_SAVAGES):
        threading.Thread(target=savage, args=(i, emptyPot, fullPot, servingsMutex)).start()

if __name__ == "__main__":
    main()