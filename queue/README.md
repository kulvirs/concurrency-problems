# Thread-Safe Queue

## Description
This is my own sixth problem that I decided to implement. In the solutions to the previous problems from the Little Book of Semaphores, we have seen synchronized queues being used a couple times. I mentioned then that behind the scenes, Python's synchronized queue uses synchronization primitives to maintain its thread-safe data structure. I decided it would be interesting to try and implement my own synchronized thread-safe queue from scratch two different ways and compare which approach is better.   
To keep things simple, the queue will just have two methods: enqueue and dequeue. The queue will have unlimited size, and if a dequeue is attempted on an empty queue, the dequeue call will block until an item is placed on the queue.

## Relevance
Having a thread-safe queue is relevant to many problems that come up in concurrent programming. I specifically wanted to implement this data structure because I can see it being used in my upcoming Concurrency project, where I want to build a collaborative text editor. In this project, client threads will be sending their updates to the server and these updates will be placed on a queue. The server will then remove items from this queue and process the updates accordingly. 

## Results

## Analysis
### Correctness
### Comprehensiblity
### Performance