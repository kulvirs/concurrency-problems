package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

const bufferLength = 5 // Size of the finite buffer.
const numProducers = 50
const numConsumers = 2
const numTrials = 100

var startTimes [numProducers]time.Time
var endTimes [numProducers]time.Time

func produceEvent(event int) {
	time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond) // Simulates time to produce the event.
}

func consumeEvent(event int) {
	time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond) // Simulates time to consume the event.
}

func producer(event int, buffer chan int) {
	//produceEvent(event)
	startTimes[event] = time.Now()
	buffer <- event // Send event to buffer.
	//fmt.Println("Event", event, "placed on buffer.")
}

func consumer(buffer chan int, wg *sync.WaitGroup) {
	for {
		event := <-buffer // Get the event from the buffer.
		//fmt.Println("Event", event, "removed from buffer.")
		endTimes[event] = time.Now()
		//consumeEvent(event)
		wg.Done()
	}
}

func main() {
	var durations float64
	var averageWaitTimes float64
	for j := 1; j < numTrials; j++ {
		buffer := make(chan int, bufferLength) // There can only be a finite number of items on the buffer at any time.
		var wg sync.WaitGroup
		wg.Add(numProducers)
		start := time.Now()
		for i := 0; i < numConsumers; i++ {
			go consumer(buffer, &wg)
		}
		for i := 0; i < numProducers; i++ {
			go producer(i, buffer)
		}
		wg.Wait()
		end := time.Now()

		var waitTimes = endTimes[0].Sub(startTimes[0])
		for i := 1; i < numProducers; i++ {
			waitTimes += endTimes[i].Sub(startTimes[i])
		}
		averageWaitTimes += waitTimes.Seconds() / numProducers
		durations += end.Sub(start).Seconds()
	}
	fmt.Println("Average wait time:", averageWaitTimes/numTrials, "s")
	fmt.Println("Average duration:", durations/numTrials, "s")
}
