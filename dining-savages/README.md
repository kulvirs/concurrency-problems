# Dining Savages

## Description
Imagine there is a tribe of savages that share one common pot filled with M servings of stew. When a savage is hungry, he takes a serving from the pot. If the pot is empty, the savage signals the cook and waits until the cook refills the pot.

## Relevance
This problem has applications to any kind of concurrent program where multiple threads are trying to take from the same shared finite resource. For example, imagine maintaining some kind of dynamic table that multiple threads can insert into. As long as there are spots available, the threads will keep inserting, but as soon as there is no more space left in the table and an item needs to be inserted, a signal will be sent so that the table can be resized. After resizing, previously blocked threads can now insert into the table.

## Results
To make the program finite, each savage only takes a serving from the pot a certain number of times. Each solution prints when a savage takes a serving from the pot and when the cook refills the pot. Sleep statements are added to simulate the amount of time to eat a serving, get a serving from the pot, and for the cook to refill the pot. The following results were gathered for each solution:

Test 1 - Correctness: The output of each solution on the same configuration (10 savages, 5 helpings per pot, 3 servings per savage) is recorded. (Other test configurations were run, but for brevity only this one is recorded in the analysis).

Test 2 - Performance: The print and sleep statements are removed. The average duration of the program and wait time over 100 trials on the same configuration (50 savages, 5 helpings per pot, 3 servings per savage) is recorded. The wait time is defined as the total amount of time a savage spends waiting to get a serving.

### Solution 1 - `ds.py`
This implementation is written in Python. It follows the solution presented in the Little Book of Semaphores and uses Locks and Semaphores.

Test 1 Output:
```
Cook refills the pot.
Savage 0 takes a serving from the pot.
Savage 1 takes a serving from the pot.
Savage 2 takes a serving from the pot.
Savage 3 takes a serving from the pot.
Savage 4 takes a serving from the pot.
Cook refills the pot.
Savage 5 takes a serving from the pot.
Savage 6 takes a serving from the pot.
Savage 7 takes a serving from the pot.
Savage 8 takes a serving from the pot.
Savage 9 takes a serving from the pot.
Cook refills the pot.
Savage 1 takes a serving from the pot.
Savage 0 takes a serving from the pot.
Savage 2 takes a serving from the pot.
Savage 3 takes a serving from the pot.
Savage 4 takes a serving from the pot.
Cook refills the pot.
Savage 5 takes a serving from the pot.
Savage 7 takes a serving from the pot.
Savage 6 takes a serving from the pot.
Savage 8 takes a serving from the pot.
Savage 9 takes a serving from the pot.
Cook refills the pot.
Savage 1 takes a serving from the pot.
Savage 0 takes a serving from the pot.
Savage 2 takes a serving from the pot.
Savage 3 takes a serving from the pot.
Savage 4 takes a serving from the pot.
Cook refills the pot.
Savage 5 takes a serving from the pot.
Savage 7 takes a serving from the pot.
Savage 6 takes a serving from the pot.
Savage 8 takes a serving from the pot.
Savage 9 takes a serving from the pot.
```

Test 2 Output:
```
Average wait time: 0.0002675807476043701 s
Average duration: 0.022325329780578614 s
```

### Solution 2 - `ds.go`
This implementation is written in Go. It uses a buffered channel to represent the pot.

Test 1 Output:
```
Cook refills the pot.
Savage 8 takes serving 1 from the pot.
Savage 7 takes serving 2 from the pot.
Savage 2 takes serving 3 from the pot.
Savage 1 takes serving 4 from the pot.
Savage 4 takes serving 5 from the pot.
Cook refills the pot.
Savage 3 takes serving 1 from the pot.
Savage 6 takes serving 2 from the pot.
Savage 3 takes serving 3 from the pot.
Savage 0 takes serving 4 from the pot.
Savage 5 takes serving 5 from the pot.
Cook refills the pot.
Savage 9 takes serving 1 from the pot.
Savage 1 takes serving 2 from the pot.
Savage 7 takes serving 3 from the pot.
Savage 2 takes serving 4 from the pot.
Savage 8 takes serving 5 from the pot.
Cook refills the pot.
Savage 7 takes serving 1 from the pot.
Savage 4 takes serving 2 from the pot.
Savage 9 takes serving 3 from the pot.
Savage 0 takes serving 4 from the pot.
Savage 8 takes serving 5 from the pot.
Cook refills the pot.
Savage 6 takes serving 1 from the pot.
Savage 5 takes serving 2 from the pot.
Savage 9 takes serving 3 from the pot.
Savage 1 takes serving 4 from the pot.
Savage 3 takes serving 5 from the pot.
Cook refills the pot.
Savage 4 takes serving 1 from the pot.
Savage 0 takes serving 2 from the pot.
Savage 2 takes serving 3 from the pot.
Savage 6 takes serving 4 from the pot.
Savage 5 takes serving 5 from the pot.
Cook refills the pot.
```

Test 2 Output:
```
Average wait time: 0.00013915934 s
Average duration: 0.0003649219999999999 s
```

## Analysis
### Correctness
The Little Book of Semaphores lists the following synchronization constraints for the Dining Savages problem:  
1. Savages cannot get servings from the pot if the pot is empty.
2. The cook can put servings in the pot only if the pot is empty.

Both solutions satisfy these constraints.  
For constraint 1, each savage in Solution 1 acquires a mutex and decrements the number of servings in the pot by 1, and then releases the mutex. However, if a savage arrives and finds the pot is empty (0 servings), it signals the cook to fill the pot, waits until it recieves a signal that the pot is full, and then takes a serving. It then decrements the number of servings remaining and releases the mutex. In Solution 2, if the pot is empty the buffered channel representing the pot will have no more items (servings) on it, so all threads will block until there are items on the channel.   
For constraint 2, in Solution 1, the cook only fills the pots if it is signalled, and it is only signalled if a savage arrives, acquires the mutex shared by all savages, and finds the number of servings remaining in the pot is 0. In Solution 2, when the cook puts servings on the buffered channel, each serving has a unique integer representing it. If the pot holds M servings, the last item placed on the buffered channel representing the pot is the integer M-1. Since items are removed in FIFO order from a buffered channel, this means that when a savage thread gets the serving M-1 off the buffer, it has taken the last serving in the pot, so it signals the cook at this point. Since no other serving with id M-1 at that point exists on the buffer, we can ensure that the cook is only signalled when the pot is empty. The output from Test 1 also helps back up the claim that both constraints are satisfied.
While both solutions do satisfy these synchronization constraints, Solution 2 does not quite solve the problem as intended. The problem description in the Little Book of Semaphores states that a savage only signals the cook if he goes to eat a serving and finds the pot is empty. Solution 2, however, signals the cook after a savage has taken the last serving, instead of when the next savage goes to take a serving. The other description detail that Solution 2 does not meet is that a savage is supposed to wait until the cook has refilled the pot before taking a serving. Since the cook refills the pot using a for loop instead of being able to fill it all at once, as soon as a single loop iteration occurs and an item is placed on the buffered channel representing the pot, waiting savage threads can take it off the channel. In other words, savages only wait as long as the pot is empty, but not until the pot has fully refilled.  
Because of these discrepancies in Solution 2, I would say Solution 1 is more correct. 

### Comprehensibility
If we ignore the code in `main()` which mostly just contains extra overhead to start the threads and measure performance, Solution 1 and Solution 2 both take up 26 lines of code, so neither solution is very long.  
Solution 1 uses two Semaphores and one Lock variable for synchronization, while Solution 2 only uses 2 buffered channels. Overall I think this makes Solution 2 more intuitive to understand and less clunky than Solution 1, because instead of having to go through all the acquire and release statements, we just send and receive on channels. The names of the channels also make it pretty clear what their purpose is and what each thread does with them. The buffered channel, `pot` indicates we are either putting items on the pot if we are sending, or taking items from the pot if we are receiving on the channel. Similarly, when the pot is empty, we send on the channel `emptyPot` to simulate signalling the cook and the cook waits to receive on this channel to simulate waiting for a signal. While Solution 1 is also pretty straightforward, the names `release` and `signal` that are used for locks and semaphores in Python don't have as intuitive of a meaning to the problem in this case as the channels do. 

### Performance
The results from Test 2 indicate that on average, savage threads wait for twice as long in Solution 1 than Solution 2. The average duration of Solution 1 is also about 60 times slower than Solution 2. This suggests that Solution 2 performs significantly better than Solution 1.  
The main reason for this is that Solution 2 takes more advantange of concurrency and parallelism than Solution 1. In Solution 1, each savage must acquire the same mutex before being able to decrement the counter to indicate it took a serving. This essentially means that we are not allowing more than one savage to take a serving from the pot at the same time, ie: the savages are lining up one by one to take a serving from the pot. This slows down the duration of the program a lot, and in my opinion is not a correct representation of how a group of savages would behave anyway. In fact, the phrase 'orderly line of savages' sounds almost like an oxymoron.  
In reality, I think each savage would be trying to get at the pot as long as its not empty, and this is what my Solution 2 tries to do. By representing the pot with a buffered channel of size equal to the number of servings, we are allowing as many threads as there are servings to concurrently take servings from the pot. And when the pot gets empty, as soon as the cook begins adding servings to the pot by putting items on the channel, the savage threads immediately begin taking the servings instead of waiting for it to completely refill. While Solution 2  may not be completely correct in terms of the problem definition, it still accomplishes the same goal in the end and does so much faster, which is why I think it's a better approach than the mutual exclusion in Solution 1.