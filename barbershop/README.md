# Barbershop

## Description
Imagine we have a barbershop with n chairs, and a barber room containing a barber chair. If there are no customers, the barber sleeps. When a customer enters, if all chairs are occupied, they leave (balk). If the barber is busy but chairs are free, the customer sits in a free chair. If the barber is asleep, the customer wakes up the barber.

## Relevance
The sleeping barber problem presents a classic example of the challenge of synchronizing and communicating between threads. An example application of this could be having mulitple worker threads (customers), each running part of some large computation. At some point each worker would need to synchronize with the parent thread (barber) to give it the result of its portion of the computation. The number of worker threads running concurrently would also have to be limited to ensure CPU usage doesn't get too high, which brings in the waiting room concept.

## Results
Each program prints when a customer enters, when they get a haircut, and when they leave the barbershop. If a customer balks, this is printed as well. The customer threads sleep for random amounts of time to simulate the time between customers arriving, and the customer and barber sleep for a random amount of time to simulate the time to get a haircut. The following results were gathered for each solution:

Test 1 - Correctness: The output of each solution on the same configuration (barbershop capacity 4, 10 total customers) is recorded. (Other test configurations were run, but for brevity, only this one is recorded in the analysis).

Test 2 - Performance: The sleep and print statements are removed. The average duration and waiting time of the program over 100 trials on the same configuration (barbershop capacity 4, 100 total customers) is recorded. The waiting time is defined as the amount of time a customer waits for a haircut. This does not account for customers that balk.

### Solution 1 - `bs.py`
This solution is implemented in Python and models the problem using a synchronized queue for the waiting chairs and a lock for the barber chair.

Test 1 Output:
```
Customer 0 enters the barbershop.
Customer 0 gets a haircut.
Customer 1 enters the barbershop.
Customer 2 enters the barbershop.
Customer 0 leaves the barbershop.
Customer 1 gets a haircut.
Customer 1 leaves the barbershop.
Customer 2 gets a haircut.
Customer 3 enters the barbershop.
Customer 2 leaves the barbershop.
Customer 3 gets a haircut.
Customer 4 enters the barbershop.
Customer 3 leaves the barbershop.
Customer 4 gets a haircut.
Customer 5 enters the barbershop.
Customer 6 enters the barbershop.
Customer 4 leaves the barbershop.
Customer 5 gets a haircut.
Customer 7 enters the barbershop.
Customer 5 leaves the barbershop.
Customer 6 gets a haircut.
Customer 8 enters the barbershop.
Customer 9 enters the barbershop.
Customer 6 leaves the barbershop.
Customer 7 gets a haircut.
Customer 7 leaves the barbershop.
Customer 8 gets a haircut.
Customer 8 leaves the barbershop.
Customer 9 gets a haircut.
Customer 9 leaves the barbershop.
```

Test 2 Output:
```
Average wait time: 0.0020884927586050073 s
Average duration: 0.046332077980041506 s
```

### Solution 2 - `bs.go`
This solution is implemented in Go and follows the solution presented in the Little Book of Semaphores, except channels are used in place of semaphores in some cases.

Test 1 Output:
```
Customer 0 enters the barbershop.
Customer 0 gets a haircut.
Customer 0 leaves the barbershop.
Customer 1 enters the barbershop.
Customer 1 gets a haircut.
Customer 1 leaves the barbershop.
Customer 2 enters the barbershop.
Customer 2 gets a haircut.
Customer 3 enters the barbershop.
Customer 3 gets a haircut.
Customer 2 leaves the barbershop.
Customer 3 leaves the barbershop.
Customer 4 enters the barbershop.
Customer 4 gets a haircut.
Customer 4 leaves the barbershop.
Customer 5 enters the barbershop.
Customer 5 gets a haircut.
Customer 6 enters the barbershop.
Customer 7 enters the barbershop.
Customer 6 gets a haircut.
Customer 5 leaves the barbershop.
Customer 7 gets a haircut.
Customer 6 leaves the barbershop.
Customer 8 enters the barbershop.
Customer 9 enters the barbershop.
Customer 7 leaves the barbershop.
Customer 8 gets a haircut.
Customer 9 gets a haircut.
Customer 8 leaves the barbershop.
Customer 9 leaves the barbershop.
```

Test 2 Output:
```
Average waiting time: 9.98e-06 s
Average duration: 0.000179532 s
```

## Analysis 
### Correctness
The Little Book of Semaphores lists the following synchronization constraints for the barbershop problem:
1. Customer threads should invoke a function named getHairCut.
2. If a customer thread arrives when the shop is full, it can invoke balk, which does not return.
3. The barber thread should invoke cutHair.
4. When the barber invokes cutHair there should be exactly one thread invoking getHairCut concurrently.

Looking at the code we can verify that constraints 1 and 3 are met by both solutions.   
Constraint 2 is also met by both solutions. In Solution 1, if the customer cannot acquire the mutex for the barber chair or be put on the queue immediately, the customer balks. Similarly in Solution 2, if the number of customers in the barbershop is already at capacity, the customer balks.  
Constraint 4 is also met by both solutions. In Solutions 1 and 2, semaphores or channels of size 1 respectively are used to signal to the barber and customer that each side is ready for a haircut and getHairCut() and cutHair() is only called by either thread when both of these signals are acquired. This ensures that when the barber invokes cutHair, there is only one thread invoking getHairCut concurrently.  
We can conclude that both solutions are correct because they meet the constraints outlined by the problem, the sample output in Test 1 also backs up this claim. It should be noted that neither solution guarantees that customers get a haircut in the order they arrive, although this isn't a constraint of the problem, it does seem incorrect if we compare it to how a normal barbershop works.
In Solution 1, customers that enter the barbershop can bypass the waiting queue and immediately sit on the barber chair if the barber is not busy at the exact moment they enter. However, customers are removed from the waiting queue in FIFO order. In Solution 2, customers that enter the barbershop wait for a signal from the barber, and any one of the waiting customer threads can receive this signal, regardless of the order they entered. 

### Comprehensibility
If we look at the code for each solution, ignoring the code in `main()` which just contains the overhead of creating the threads and calculating results, we can see that Solution 1 uses 42 lines and Solution 2 uses 40 lines. So both solutions are roughly equal in length.  
Solution 1 uses 4 semaphores, a synchronized queue, and a mutex to synchronize all its threads. However, Solution 2 only uses 4 channels of size 1 and one lock to synchronize all of its threads. In terms of the complexity the extra synchronization variables introduce to understanding the solution, Solution 2 would logically be easier to follow. Solution 1 also makes some non-blocking calls to the barber chair mutex and the queue, which would involve extra explanation to somebody who is not aware that Python allows non-blocking checks on locks and queues. For these reasons, I would say that Solution 2 is a more comprehensible solution than Solution 1.

### Performance
From the results of Test 2, we can see that Solution 2 is about 258 times faster than Solution 1 on average, so we can conclude that Solution 2 performs much better.
This difference in performance could be caused a number of reasons, but the primary reasons are probably (as mentioned in the producer-consumer problem) that Python overall is a higher level language with more overhead than Go, and it is interpreted at run time instead of compiled beforehand.  
A contributing factor to Solution 1 being slower could also be that it uses the synchronized queue, which is a data structure that has more semaphores and a mutex in it behind the scenes. The added cost of these extra sychronization variables compared to Solution 2 which just uses lightweight primitive Go channels and only one mutex probably causes Solution 1 to run slower.