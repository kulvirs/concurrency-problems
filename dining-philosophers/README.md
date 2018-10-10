# Dining Philosophers

## Description
The Little Book of Semaphores states that the Dining Philosophers problem "was proposed by Dijkstra in 1965, when dinosaurs ruled the earth". Obviously I could not pass up the chance to implement such a classic problem. For those of you living under a rock, the basic premise is that there is a table with 5 seats and 5 chopsticks, with one big bowl of rice in the middle. Five philosophers come to the table and each loops forever between thinking and eating. When a philosopher eats, it grabs the chopsticks that are on either side of it, which means it may have to wait for its neighbour to finish eating so that it can acquire both chopsticks.   
![Dining Philsophers Image](https://github.com/kulvirs/concurrency-problems/blob/master/dining-philosophers/dp.PNG)

## Relevance 
The Dining Philosophers problem illustrates a common issue that comes up in concurrent programs where we have shared resources between threads and wish to prevent deadlock, while also trying to have as many threads running concurrently as possible.  
An example application of this could be modelling transactions between bank accounts. To move money from Account A into Account B, we need to lock both Account A and Account B. While this transaction is occurring, another account, say Account C, would have to wait before being able to transfer money to Account A. Account B would also have to wait before being able to transfer money to Account C, etc. There could be many accounts that are dependent on each other in this way, so maximizing the amount of concurrent transactions would help speed things up, but accounting for deadlock is crucial since we do not want the process to halt indefinitely (or some customers would be very upset).

## Results
In order to stop the programs from running forever, a restriction was added on how many helpings each philosopher eats throughout the program. 
Each solution prints when a philosopher gets hungry, when they start eating, and when they are thinking. The philosophers also sleep for random intervals to simulate the time to eat and think. The following results were gathered for each solution:

Test 1 - Correctness: The output of each solution on the same configuration (5 philosophers, 2 helpings per philosopher) is recorded. (Other test configurations were run, but for brevity, only this one is recorded in the analysis).

Test 2 - Performance: The print and sleep statements are removed. The average duration of the entire program as well as the average wait time over 100 trials on the same configuration (5 philosophers, 100 helpings per philosopher) is recorded. The wait time is defined as the amount of time a philosopher spends waiting to eat during the entire program.

Solution 1 - `dp.py`
This implementation is written in Python and follows the solution proposed by Tanenbaum in the Little Book of Semaphores. It uses locks and semaphores.

Test 1 Output:
```
Philosopher 2 is hungry.
Philosopher 2 is eating.
Philosopher 1 is hungry.
Philosopher 0 is hungry.
Philosopher 0 is eating.
Philosopher 2 is thinking.
Philosopher 4 is hungry.
Philosopher 3 is hungry.
Philosopher 3 is eating.
Philosopher 2 is hungry.
Philosopher 0 is thinking.
Philosopher 1 is eating.
Philosopher 0 is hungry.
Philosopher 3 is thinking.
Philosopher 4 is eating.
Philosopher 4 is thinking.
Philosopher 1 is thinking.
Philosopher 2 is eating.
Philosopher 0 is eating.
Philosopher 2 is thinking.
Philosopher 3 is hungry.
Philosopher 3 is eating.
Philosopher 4 is hungry.
Philosopher 0 is thinking.
Philosopher 1 is hungry.
Philosopher 1 is eating.
Philosopher 3 is thinking.
Philosopher 4 is eating.
Philosopher 4 is thinking.
Philosopher 1 is thinking.
```

Test 2 Output:
```
Average waiting time: 6.438846588134761e-05 s
Average duration: 0.010681324005126953 s
```

Solution 2 - `dp.go`
This implementation is written in Go and follows Solution #1 from the Little Book of Semaphores, except channels are used in the place of Semaphores.

Test 1 Output:
```
Philosopher 3 is hungry
Philsopher 3 is eating
Philosopher 0 is hungry
Philsopher 0 is eating
Philosopher 3 is thinking
Philosopher 4 is hungry
Philosopher 2 is hungry
Philsopher 2 is eating
Philosopher 0 is thinking
Philosopher 0 is hungry
Philsopher 4 is eating
Philosopher 1 is hungry
Philosopher 3 is hungry
Philosopher 2 is thinking
Philsopher 1 is eating
Philosopher 2 is hungry
Philsopher 3 is eating
Philosopher 4 is thinking
Philosopher 1 is thinking
Philsopher 0 is eating
Philosopher 4 is hungry
Philosopher 0 is thinking
Philosopher 3 is thinking
Philsopher 2 is eating
Philsopher 4 is eating
Philosopher 1 is hungry
Philosopher 4 is thinking
Philosopher 2 is thinking
Philsopher 1 is eating
Philosopher 1 is thinking
```

Test 2 Output:
```
Average waiting time: 0.0006223617999999997 s
Average duration: 0.0008377379999999998 s
```

## Analysis

### Correctness
The Little Book of Semaphores presents the following synchronization constraints on the dining philosophers problem:
1. Only one philosopher can hold a fork at a time.
2. It must be impossible for a deadlock to occur.
3. It must be impossible for a philosopher to starve waiting for a fork.
4. It must be possible for more than one philosopher to eat at the same time.

Constraint 1 is satisfied by both solutions. In Solution 1, a philosopher only picks up the forks beside him if neither of his neighbours are eating, which guarantees that only one philosopher holds a fork. In Solution 2, each fork is modelled as a buffered channel of size 1, which means there can only ever be one philosopher in a fork buffer, and everyone else would be blocked.  
Constraint 2 is also satisfied by both solutions. In Solution 1, deadlock is impossible because `mutex` is the only synchronization variable accessed by all threads (philosophers), and no thread executes any blocking calls while holding `mutex`. In Solution 2, we only ever allow `numPhilosophers-1` philosophers to sit at the table. This makes deadlock impossible because even if every philosopher picks up a fork at the same time, there will still be one fork remaining at the table, which either of its adjacent philosophers can pick up and start eating.   
Constraint 3 is not satisfied by Solution 1. As is described in the Little Book of Semaphores, it is possible that a philosopher never gets to eat because one of its neighbours is always eating whenever it gets signalled. Since we have limited our solution to be finite however, starvation will never happen because eventually all neighbours of any philosopher will have eaten all their helpings and they will no longer try to acquire the mutex. Constraint 3 is satisfied by Solution 2, in both the finite and infinite case. If a philosopher is waiting for a fork, it is guaranteed that eventually his neighbour holding that fork will finish eating. At that point, no other thread is waiting for the fork, so the philosopher will get the fork and be able to eat.  
Constraint 4 is also satisfied by both solutions. In Solutions 1 and 2, a philosopher can eat as long as his neighbours are not, which means non-adjacent philosophers can be eating at same time.   
Overall, due to Solution 1 not satisfying Constraint 3 in the infinite case, we can conclude that Solution 2 is more correct.

### Comprehensibility
Not including the code in `main()` which is mostly just the overhead of creating the threads and measuring run time, Solution 1 uses 39 lines of code for the philosopher threads. Solution 2 uses 36, 30 if you don't count the curly braces that are included in Go. 
In terms of understanding the code, Solution 2 just uses buffered channels. Looking at the code, it is pretty easy to explain to somebody what is going on, philosophers wait until they can sit at the table, and then wait until their right and left fork is free. At this point they can eat, and then they release their right and left fork, and leave the table.
Solution 1 on the other hand uses Semaphores and a Lock. The solution takes a bit more work to explain and it's not intuitively obvious just by reading the code once why it works. However, the use of the state variable being set to "hungry", "thinking", or "eating" for each philosopher does help in understanding what is happening in the code.
Overall, Solution 2 is shorter and intuitively easier to understand than Solution 1.

### Performance
From the results we can see that in Solution 2, each philosopher thread waits when it is hungry on average 10 times longer than it does in Solution 1. However, the overall duration of Solution 2 is about 12 times faster than Solution 1.   
As mentioned earlier, in Solution 2 we only allow `numPhilosophers-1` people to sit at the table at the same time. While this approach does avoid deadlock, it means that we are not utilizing the full concurrency of our system. It is possible that philosophers that are waiting for the table to have less than 4 people at it could have sat down and eaten if not for this restriction. This could be what causes the philosopher threads in Solution 2 to have a longer average wait time than the threads in Solution 2.  
Overall though, Solution 1 runs faster than Solution 2. This could be because the overhead of having Semaphores and Locks in Python is still much slower than using channels in Go, so even though each thread is waiting for less time in Solution 1, the overall synchronization takes longer. 
In terms of which solution performs better, it depends what we are prioritizing. If we want each philosopher to wait the least amount of time, then Solution 1 performs better. If we want the overall program to take as little time as possible, then Solution 2 performs better.