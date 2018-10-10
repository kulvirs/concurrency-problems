# Producer-Consumer (Finite Buffer)

## Description
Imagine we have two types of threads: producers and consumers. They share a bounded buffer. Producers produce items and add them to the buffer. Consumers remove items from the buffer and consume them. If a producer thread tries to place an item on a full buffer, it will block until a consumer removes an item from the buffer first. Similarly, if a consumer tries to remove an item from an empty buffer, it will block until a producer places an item on the buffer first.

## Relevance
The producer-consumer problem presents a pattern that is very common in multi-threaded programs. Often, there will be scenarios where multiple threads are creating items and adding them to a data structure (producers), while others are removing the items from this data structure and processing them accordingly (consumers).  
One good real world example is in event-driven programs, such as network packets. When an event occurs, ie: a packet arrives, a producer thread places it on some sort of event buffer. Consumer threads will remove these events from the buffer and process them.   
There are often limits on how large these buffers can be based on the environment they are in. Having a finite buffer ensures these limits are not exceeded. 

## Results

Each solution prints when an event is placed on the buffer and when it is removed from the buffer. The producers and consumers also sleep for random intervals to simulate the time that it would take to produce or consume an event. The following results were gathered for each solution: 

Test 1 - Correctness: The output of each solution on the same configuration (1 consumer, 10 producers, buffer size 3) is recorded. (Other test configurations were run, but for brevity only this one is recorded in the analysis).  

Test 2 - Performance: The print and sleep statements are removed. The average duration of the program and wait time over 100 trials on the same configuration (2 consumers, 50 producers, buffer size 5) is recorded. The wait time is defined as the amount of time between an item being produced and being consumed.

### Solution 1 - `pcfb.py`
This implementation is written in Python and uses Python's [synchronized queue](https://docs.python.org/3/library/queue.html) as a shared buffer between the producer and consumer threads. 

Test 1 Output:   
``` 
Event 4 placed on buffer.
Event 4 removed from buffer.
Event 7 placed on buffer.
Event 2 placed on buffer.
Event 8 placed on buffer.
Event 7 removed from buffer.
Event 1 placed on buffer.
Event 2 removed from buffer.
Event 6 placed on buffer.
Event 8 removed from buffer.
Event 5 placed on buffer.
Event 1 removed from buffer.
Event 0 placed on buffer.
Event 6 removed from buffer.
Event 3 placed on buffer.
Event 5 removed from buffer.
Event 9 placed on buffer.
Event 0 removed from buffer.
Event 3 removed from buffer.
Event 9 removed from buffer.
```

Test 2 Output:
```
Average wait time: 0.0002314748287200928 s
Average duration: 0.02663850545883179 s
```

### Solution 2 - `pcfb.go`
This implementation is written in Go and uses a buffered channel to communicate between the producer and consumer goroutines (threads). 

Test 1 Output:  
```
Event 4 placed on buffer.
Event 4 removed from buffer.
Event 6 placed on buffer.
Event 7 placed on buffer.
Event 8 placed on buffer.
Event 6 removed from buffer.
Event 5 placed on buffer.
Event 7 removed from buffer.
Event 1 placed on buffer.
Event 8 removed from buffer.
Event 0 placed on buffer.
Event 5 removed from buffer.
Event 3 placed on buffer.
Event 1 removed from buffer.
Event 2 placed on buffer.
Event 0 removed from buffer.
Event 9 placed on buffer.
Event 3 removed from buffer.
Event 2 removed from buffer.
Event 9 removed from buffer.
```

Test 2 Output:
```
Average wait time: 5.5622199999999996e-06 s
Average duration: 0.00012972599999999998 s
```

## Analysis

### Correctness
The Little Book of Semaphores lists the following synchronization constraints on the finite buffer producer-consumer problem: 
1) Threads must have exclusive access to the buffer.
2) If a consumer thread arrives while the buffer is empty, it blocks until a producer adds a new item.
3) If a producer arrives when the buffer is full, it blocks until a consumer removes an item.

Python's synchronized queue [documentation](https://docs.python.org/3/library/queue.html) confirms that one thread at any given time can modify the queue, the put() method will "block if necessary until a free slot is available", and the get() method will also "block if necessary until an item is available".   
Similarly, the Tour of Go section on [buffered channels](https://tour.golang.org/concurrency/3) states that "sends to a buffered channel block only when the buffer is full. Receives block when the buffer is empty."   
Therefore we can conclude that both solutions are correct in their implementation. The results of Test 1 also back up this claim, as we can see that items are not removed until there is something in the buffer to remove, and items are not placed in the full buffer until something is removed.

### Comprehensibility
For each solution, we can see that code is pretty short and straightforward. Ignoring the code in `main()`, which contains extra overhead to set up the threads and calculate times, the actual code in the producer and consumer threads is only 23 lines in each solution. Each solution only uses one data structure or type to represent the buffer, a queue in Solution 1 and a channel in Solution 2. There are no confusing Semaphores or Mutexes present in either one that may confuse a reader.  
Imagine we presented both of these solutions to somebody who is familiar with programming but not concurrency. All computer scientists learn basic data structures, so they would be familiar with a queue and probably understand Solution 1 very easily as a result, even if they don't know Python. Solution 2 would require first understanding how channels work in Go, so it would be a bit more work for someone to understand and is more language-specific. However, the arrow concept of sending and receiving on channels is very intuitive, so some people might find it easier to understand than Solution 1 if their familiarity with data structures isn't very good.

### Performance
Performance-wise it is very clear that Solution 2 is better. Each item in Solution 2 spends significantly less time waiting between production and consumption and the overall time to produce and consume all the items in Solution 2 is about 20 times faster than Solution 1.
There are a number of reasons why Solution 2 performs better. Firstly, Solution 1 is implemented in Python, which, while it is known for being more readable, is interpreted at run time instead of compiled to native code at compile time. It also is a higher level language than Go, so many details are abstracted away from the user, such as memory management, pointers, etc, and managing all this takes more time.  
Finally, the synchronized queue used in Solution 1 is not a primitive type like channels are in Go. If we look at the [source code](https://github.com/python/cpython/blob/3.7/Lib/queue.py) for the synchronized queue, we can see that behind the scenes it uses mutexes and conditions which take time to lock and unlock and may cause more context switching. So while the code may look short to us when we use it, there is a lot more overhead to handle synchronization in Solution 1 than there is in Solution 2.

