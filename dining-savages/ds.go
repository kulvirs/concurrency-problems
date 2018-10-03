package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

const numServings = 5 // The number of servings the pot can hold.
const numSavages = 10
const maxHelpings = 4 // The maximum number of times each savage eats.

type flag struct {
	sync.Mutex
	value bool
}

func cook(pot chan int, emptyPot chan int, cookSignal *flag) {
	for {
		<-emptyPot
		fmt.Println("Cook refills the pot.")
		for i := 0; i < numServings; i++ {
			time.Sleep(time.Duration(rand.Intn(10)) * time.Millisecond) // Simulates time to refill each serving.
			pot <- i
		}
		cookSignal.Lock()
		cookSignal.value = false
		cookSignal.Unlock()
	}
}

func savage(i int, pot chan int, emptyPot chan int, cookSignal *flag, wg *sync.WaitGroup) {
	numHelpings := 0
	for numHelpings < maxHelpings {
		select {
		case <-pot:
			// There is food in the pot.
			fmt.Println("Savage", i, "takes a serving from the pot.")
			time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond) // Simulates time to get a serving from the pot.
		default:
			// There is no food in the pot.
			cookSignal.Lock()
			if !cookSignal.value {
				// Send a signal to the cook about the empty pot.
				emptyPot <- i
				cookSignal.value = true
			}
			cookSignal.Unlock()
			<-pot // Block until there is food in the pot.
			fmt.Println("Savage", i, "takes a serving from the pot.")
			time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond) // Simulates time to get a serving from the pot.
		}
		time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond) // Simulates time to eat the serving.
		numHelpings++
	}
	wg.Done()
}

func main() {
	var wg sync.WaitGroup
	pot := make(chan int, numServings)
	emptyPot := make(chan int, 1)
	var cookSignal = &flag{value: false} // Keeps track of whether the cook has been signalled to refill the pot.

	wg.Add(numSavages)
	go cook(pot, emptyPot, cookSignal)
	for i := 0; i < numSavages; i++ {
		go savage(i, pot, emptyPot, cookSignal, &wg)
	}
	wg.Wait()
}
