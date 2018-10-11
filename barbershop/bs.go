// This is an implementation using Go channels of the solution described in the Little Book of Semaphores.
package main

import (
	"fmt"
	"sync"
	"time"
)

const maxCustomers = 4     // Maximum number of customers allowed in the shop.
const totalCustomers = 100 // Total number of customers that will arrive throughout the program.
const numTrials = 100

var waitingTimes [totalCustomers]float64

type counter struct {
	sync.Mutex
	value int
}

func balk(i int) {
	//fmt.Println("Customer", i, "balks.")
}

func getHairCut(i int) {
	//fmt.Println("Customer", i, "gets a haircut.")
	//time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond) // Simulates time to get haircut.
}

func cutHair() {
	//time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond) // Simulates time to give a haircut.
}

func barberThread(customer chan int, barber chan int, customerDone chan int, barberDone chan int) {
	for {
		customerNum := <-customer
		barber <- customerNum
		cutHair()
		customerNum = <-customerDone
		barberDone <- customerNum
	}
}

func customerThread(i int, numCustomers *counter, customer chan int, barber chan int, customerDone chan int, barberDone chan int, wg *sync.WaitGroup) {
	//fmt.Println("Customer", i, "enters the barbershop.")
	start := time.Now()
	numCustomers.Lock()
	if numCustomers.value == maxCustomers {
		numCustomers.Unlock()
		balk(i)
		wg.Done()
		return
	}
	numCustomers.value++
	numCustomers.Unlock()

	customer <- i
	<-barber
	end := time.Now()
	getHairCut(i)
	customerDone <- i
	<-barberDone

	numCustomers.Lock()
	numCustomers.value--
	//fmt.Println("Customer", i, "leaves the barbershop.")
	numCustomers.Unlock()
	waitingTimes[i] = end.Sub(start).Seconds()
	wg.Done()
}

func main() {
	var durations float64
	var averageWaitingTimes float64
	for j := 0; j < numTrials; j++ {
		var wg sync.WaitGroup
		var numCustomers = &counter{value: 0} // Keeps track of how many customers are in the barbershop.
		customer := make(chan int, 1)
		barber := make(chan int, 1)
		customerDone := make(chan int, 1)
		barberDone := make(chan int, 1)

		start := time.Now()
		go barberThread(customer, barber, customerDone, barberDone)
		wg.Add(totalCustomers)
		for i := 0; i < totalCustomers; i++ {
			//time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond) // Simulates time between customers arriving.
			go customerThread(i, numCustomers, customer, barber, customerDone, barberDone, &wg)
		}
		wg.Wait()
		end := time.Now()
		durations += end.Sub(start).Seconds()

		// get all non-zero waiting times
		var sum float64
		var len float64
		for i := 0; i < totalCustomers; i++ {
			if waitingTimes[i] != 0 {
				sum += waitingTimes[i]
				len++
				waitingTimes[i] = 0
			}
		}
		if len == 0 {
			averageWaitingTimes = 0
		} else {
			averageWaitingTimes += sum / len
		}
	}
	fmt.Println("Average waiting time:", averageWaitingTimes/numTrials, "s")
	fmt.Println("Average duration:", durations/numTrials, "s")
}
