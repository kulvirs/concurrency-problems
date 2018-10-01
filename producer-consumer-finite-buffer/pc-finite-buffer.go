package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

const bufferLength = 5 // Size of the finite buffer.
const numProducers = 10
const numConsumers = 1

func produceEvent(event int) {
	time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond) // Simulates time to produce the event.
	fmt.Println("Produced event", event)
}

func consumeEvent(event int) {
	time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond) // Simulates time to consume the event.
	fmt.Println("Consumed event", event)
}

func producer(event int, buffer chan int) {
	produceEvent(event)
	buffer <- event // Send event to buffer.
}

func consumer(buffer chan int, wg *sync.WaitGroup) {
	for {
		event := <-buffer // Get the event from the buffer.
		consumeEvent(event)
		wg.Done()
	}
}

func main() {
	buffer := make(chan int, bufferLength) // There can only be a finite number of items on the buffer at any time.
	var wg sync.WaitGroup
	wg.Add(numProducers)
	for i := 0; i < numConsumers; i++ {
		go consumer(buffer, &wg)
	}
	for i := 0; i < numProducers; i++ {
		go producer(i, buffer)
	}
	wg.Wait()
}
