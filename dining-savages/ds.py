# This is an implementation of the solution presented in the Little Book of Semaphores.
import threading
import time
import random

MAX_SERVINGS = 5 # Maximum number of servings the pot can hold.
NUM_SAVAGES = 50
MAX_HELPINGS = 3 # Maximum number of times each savage eats.
NUM_TRIALS = 100

numServings = 0 # Number of servings remaining in the pot.
waitTimes = [0]*NUM_SAVAGES

def cook(emptyPot, fullPot):
    global numServings
    while True:
        emptyPot.acquire()
        #time.sleep(0.001*random.randint(0,100)) # Simulate time to fill up pot.
        numServings = MAX_SERVINGS
        #print("Cook refills the pot.")
        fullPot.release()

def savage(i, emptyPot, fullPot, servingsMutex):
    global numServings
    global waitTimes
    numHelpings = 0
    while numHelpings < MAX_HELPINGS:
        start = time.time()
        servingsMutex.acquire()
        if numServings == 0:   # Wake up cook to refill pot.
            emptyPot.release()
            fullPot.acquire()
        #time.sleep(0.001*random.randint(0,100)) # Simulate time to get a serving from pot.
        numServings -= 1
        #print("Savage", i, "takes a serving from the pot.")
        servingsMutex.release()
        end = time.time()
        #time.sleep(0.001*random.randint(0,100)) # Simulate time to eat serving.
        numHelpings += 1
        waitTimes[i] += end-start

def main():
    durations = [0]*NUM_TRIALS
    averageWaitTimes = [0]*NUM_TRIALS
    for j in range(NUM_TRIALS):
        emptyPot = threading.Semaphore(0)
        fullPot = threading.Semaphore(0)
        servingsMutex = threading.Lock()

        cookThread = threading.Thread(target=cook, args=(emptyPot, fullPot))
        # Set the cook thread to run in the background so that the main thread can exit even if cook is still running.
        cookThread.daemon = True 
        cookThread.start()

        start = time.time()
        savages = []
        for i in range(NUM_SAVAGES):
            savageThread = threading.Thread(target=savage, args=(i, emptyPot, fullPot, servingsMutex))
            savages.append(savageThread)
            savageThread.start()

        for s in savages:
            s.join()
        end = time.time()
        durations[j] = end - start
        global waitTimes
        averageWaitTimes[j] = sum(waitTimes)/len(waitTimes)
        waitTimes = [0]*NUM_SAVAGES
        global numServings
        numServings = 0
    
    print("Average wait time:", sum(averageWaitTimes)/len(averageWaitTimes), "s")
    print("Average duration:", sum(durations)/len(durations), "s")

if __name__ == "__main__":
    main()