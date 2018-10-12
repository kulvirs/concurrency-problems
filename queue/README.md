# Thread-Safe Queue

## Description
This is my own sixth problem that I decided to implement. In the solutions to the previous problems from the Little Book of Semaphores, we have seen synchronized queues being used a couple times. I mentioned then that behind the scenes, Python's synchronized queue uses synchronization primitives to maintain its thread-safe data structure. I decided it would be interesting to try and implement my own synchronized thread-safe queue from scratch two different ways and compare which approach is better.   
To keep things simple, the queue will just have two methods: `enqueue` and `dequeue`. The queue will have unlimited size, and if a `dequeue` is attempted on an empty queue, the `dequeue` call will block until an item is placed on the queue.

## Relevance
Having a thread-safe queue is relevant to many problems that come up in concurrent programming. I specifically wanted to implement this data structure because I can see it being used in my upcoming Concurrency project, where I want to build a collaborative text editor. In this project, client threads will be sending their updates to the shared document to the server and these updates will be placed on a queue. The server will then remove items from this queue and process the updates accordingly. 

## Results
Each solution prints when an item is placed on the queue and when it is removed from the queue. To test that the queue data structure I wrote works, I created producer and consumer threads which enqueue and dequeue items on the queue, respectively. To simulate the amount of time between placing items on the queue, the producer threads sleep for random intervals. The following results were gathered for each solution:

Test 1 - Correctness: The output of each solution on the same configuration (10 enqueues each done by one producer thread, 1 consumer thread) is recorded. (Other test configurations were run, but for brevity, only this one is recorded in the analysis).

Test 2 - Performance: The sleep and print statements are removed. The average duration and wait time on the same configuration (100 enqueues each done by one producer thread, 1 consumer thread) is recorded. The wait time is defined as the amount of time between an item arriving and being removed from the queue.

Since Python already has a synchronized queue data structure, the performance results of Test 2 were also gathered for this baseline implementation as a comparison.

### Baseline - `q-baseline.py`
This implementation just uses Python's synchronized queue class to provide a comparison for my own implementations of a synchronized queue.

Test 2 Output:
```
Average wait time: 0.000247722601890564 s
Average duration: 0.052110645771026615 s
```

### Solution 1 - `q-lock.py `
This implementation is written in Python and uses a single Lock variable which must be acquired to enqueue or dequeue. A list is used as the underlying implementation for the queue.

Test 1 Output:
```
9 was placed on the queue.
9 was removed from the queue.
5 was placed on the queue.
0 was placed on the queue.
5 was removed from the queue.
0 was removed from the queue.
3 was placed on the queue.
3 was removed from the queue.
2 was placed on the queue.
2 was removed from the queue.
6 was placed on the queue.
4 was placed on the queue.
6 was removed from the queue.
4 was removed from the queue.
8 was placed on the queue.
8 was removed from the queue.
7 was placed on the queue.
7 was removed from the queue.
1 was placed on the queue.
1 was removed from the queue.
```

Test 2 Output:
```
Average wait time: 4.777038097381593e-05 s
Average duration: 0.7256075954437256 s
```

### Solution 2 - `q-condition.py`
This implementation is also written in Python and uses a single Condition variable which must be acquired to enqueue or dequeue. A list is used as the underlying implementation for the queue.

Test 1 Output:
```
5 was placed on the queue.
5 was removed from the queue.
2 was placed on the queue.
2 was removed from the queue.
4 was placed on the queue.
4 was removed from the queue.
9 was placed on the queue.
9 was removed from the queue.
7 was placed on the queue.
7 was removed from the queue.
1 was placed on the queue.
1 was removed from the queue.
3 was placed on the queue.
3 was removed from the queue.
6 was placed on the queue.
6 was removed from the queue.
0 was placed on the queue.
0 was removed from the queue.
8 was placed on the queue.
8 was removed from the queue.
```

Test 2 Output:
```
Average wait time: 0.00015542080402374266 s
Average duration: 0.04377789497375488 s
```

## Analysis
### Correctness
I have defined the following synchronization constraints on the thread-safe queue problem:  
1. Only one thread should be able to modify the queue at any time.
2. If the queue is empty when `dequeue` is called, the call should block until an item is placed on the queue.

Both Solutions 1 and 2 satisfy these constraints.  
For Constraint 1,  both solutions require that a lock or condition is acquired before any modifications can be made to the data structure.  
For Constraint 2, when `dequeue` is called, Solution 1 starts to execute an infinite loop that acquires the queue mutex and checks if the length is 0. If it is, it releases the mutex. If it is not, it removes an item from the queue, releases the mutex, and returns the item. The loop ensures that the thread will be blocked until an item is placed on the queue. Solution 2 uses a condition variable to achieve the same effect. When `dequeue` is called, Solution 2 acquires the condition variable and checks the length of the queue. If the length is zero, it waits on the condition variable. When an item is put in the queue, the `enqueue` method signals the condition variable, causing the waiting dequeue thread to wake up and remove the item from the queue. 

### Comprehensiblity
If we just look at the `ThreadSafeQueue` class, we can see that both implementations of the queue are fairly short. Solution 1 uses 24 lines of code and Solution 2 uses 21 lines of code.  
Both solutions also only use one synchronization variable, so there is not extra complexity in that sense in either solution.   
Intuitively though, I think Solution 2 with a condition variable is more comprehensible to the reader. Instead of continously looping and checking if the length of the queue is non-zero at every loop iteration, Solution 2's approach of just waiting for a signal that there is something on the queue seems much more straightforward and elegant.

### Performance
The results of Test 2 indicate that on average the waiting time in Solution 1 is about 3 times faster than Solution 2. However, the overall duration of Solution 2 is 16 times faster than Solution 1.   
Solution 1 has the disadvantage that the `dequeue` method is running in a loop that continuously acquires and releases a lock. This constant acquiring and releasing of the lock is known as busy waiting, and it means that the thread that is blocked on `dequeue` never actually sleeps, it just keeps continously polling the lock. This wastes CPU cycles that other threads (ie: producers) could be using to put items on the queue. This is probably what causes the overall duration of Solution 1 to be so much longer than Solution 2. For this reason, Solution 2 has better performance than Solution 1.  
Compared to the baseline implementation that uses Python's synchronized queue class, Solution 2 performs slightly better than it in terms of waiting time and overall duration. This is probably because Python's synchronized queue class also supports other methods such as `qsize`, `empty`, and `full`, as well as non-blocking `put` and `remove`, which I have not implemented in Solution 2 since they weren't necessary to the project I'm designing it for. The overhead of maintaining thread safety while also maximizing concurrent thread access for these methods probably causes the baseline implementation to be slower than Solution 2.