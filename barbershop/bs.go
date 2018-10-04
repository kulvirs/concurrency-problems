package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

const maxCustomers = 4    // Maximum number of customers allowed in the shop.
const totalCustomers = 10 // Total number of customers that will arrive throughout the program.

type counter struct {
	sync.Mutex
	value int
}

func balk(i int) {
	fmt.Println("Customer", i, "balks.")
}

func getHairCut(i int) {
	fmt.Println("Customer", i, "gets a haircut.")
	time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond) // Simulates time to get haircut.
}

func barberThread(customer chan int, barber chan int, customerDone chan int, barberDone chan int) {
	for {
		customerNum := <-customer
		barber <- customerNum
		// cutHair() time simulated by getHairCut()
		customerNum = <-customerDone
		barberDone <- customerNum
	}
}

func customerThread(i int, numCustomers *counter, customer chan int, barber chan int, customerDone chan int, barberDone chan int, wg *sync.WaitGroup) {
	numCustomers.Lock()
	if numCustomers.value == maxCustomers {
		numCustomers.Unlock()
		balk(i)
		return
	}
	numCustomers.value++
	fmt.Println("Customer", i, "enters the barbershop.")
	numCustomers.Unlock()

	customer <- i
	<-barber
	getHairCut(i)
	customerDone <- i
	<-barberDone

	numCustomers.Lock()
	numCustomers.value--
	fmt.Println("Customer", i, "leaves the barbershop.")
	numCustomers.Unlock()
	wg.Done()
}

func main() {
	var wg sync.WaitGroup
	var numCustomers = &counter{value: 0} // Keeps track of how many customers are in the barbershop.
	customer := make(chan int, 1)
	barber := make(chan int, 1)
	customerDone := make(chan int, 1)
	barberDone := make(chan int, 1)

	go barberThread(customer, barber, customerDone, barberDone)
	wg.Add(totalCustomers)
	for i := 0; i < totalCustomers; i++ {
		time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond) // Simulates time between customers arriving.
		go customerThread(i, numCustomers, customer, barber, customerDone, barberDone, &wg)
	}
	wg.Wait()
}
