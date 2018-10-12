package main

import (
	"fmt"
	"sync"
	"time"
)

const numServings = 5 // The number of servings the pot can hold.
const numSavages = 50
const maxHelpings = 3 // The maximum number of times each savage eats.
const numTrials = 100

var waitTimes [numSavages]float64

func cook(pot chan int, emptyPot chan int) {
	for {
		//fmt.Println("Cook refills the pot.")
		for i := 1; i <= numServings; i++ {
			pot <- i
		}
		<-emptyPot
	}
}

func savage(i int, pot chan int, emptyPot chan int, wg *sync.WaitGroup) {
	numHelpings := 0
	for numHelpings < maxHelpings {
		//time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond) // Simulates time between getting hungry.
		start := time.Now()
		serving := <-pot
		end := time.Now()
		//fmt.Println("Savage", i, "takes serving", serving, "from the pot.")
		if serving == numServings {
			emptyPot <- i // No more servings remaining, so we signal the cook.
		}
		//time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond) // Simulates time to get and eat the serving.
		numHelpings++
		waitTimes[i] += end.Sub(start).Seconds()
	}
	wg.Done()
}

func main() {
	var durations float64
	var averageWaitTimes float64
	for j := 0; j < numTrials; j++ {
		var wg sync.WaitGroup
		pot := make(chan int, numServings)
		emptyPot := make(chan int, 1)

		start := time.Now()
		wg.Add(numSavages)
		go cook(pot, emptyPot)
		for i := 0; i < numSavages; i++ {
			go savage(i, pot, emptyPot, &wg)
		}
		wg.Wait()
		end := time.Now()
		durations += end.Sub(start).Seconds()
		var sumWaitTimes float64
		for i := 0; i < numSavages; i++ {
			sumWaitTimes += waitTimes[i]
			waitTimes[i] = 0
		}
		averageWaitTimes += sumWaitTimes / numSavages
	}
	fmt.Println("Average wait time:", averageWaitTimes/numTrials, "s")
	fmt.Println("Average duration:", durations/numTrials, "s")
}
