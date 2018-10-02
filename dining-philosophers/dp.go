// This is an implementation using Go channels of the Dining Philosophers Solution #1 from the Little Book of Semaphores.
package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

const numPhilosophers = 5
const maxEats = 2 // Maximum number of times each philosopher eats.

func rightFork(i int) int {
	return i
}

func leftFork(i int) int {
	return (i + 1) % numPhilosophers
}

func getForks(i int, rightFork chan int, leftFork chan int) {
	rightFork <- i
	leftFork <- i
}

func putForks(i int, rightFork chan int, leftFork chan int) {
	<-rightFork
	<-leftFork
}

func philosopher(i int, table chan int, rightFork chan int, leftFork chan int, wg *sync.WaitGroup) {
	numEats := 0
	for numEats < maxEats {
		time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond) // Simulates time to think.
		fmt.Println("Philosopher", i, "is hungry")
		table <- i
		getForks(i, rightFork, leftFork)
		fmt.Println("Philsopher", i, "is eating")
		time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond) // Simulates time to eat.
		putForks(i, rightFork, leftFork)
		fmt.Println("Philosopher", i, "is thinking")
		<-table
		numEats++
	}
	wg.Done()
}

func main() {
	var wg sync.WaitGroup
	table := make(chan int, numPhilosophers-1) // Makes sure only numPhilosophers-1 people are ever seated at the table at the same time (to avoid deadlock)
	var forks [numPhilosophers]chan int
	for i := range forks {
		forks[i] = make(chan int, 1)
	}

	wg.Add(numPhilosophers)
	for i := 0; i < numPhilosophers; i++ {
		go philosopher(i, table, forks[rightFork(i)], forks[leftFork(i)], &wg)
	}
	wg.Wait()
}
