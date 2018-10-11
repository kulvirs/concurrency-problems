# Unisex Bathroom
## Description
A workplace decides to convert one of their bathrooms to a unisex bathroom. At most 3 employees can be in the bathroom at any given time, and there cannot be men and women in the bathroom at the same time.  

## Relevance
This problem has applications in any kind of concurrent program where only certain kinds of threads can have access to the same resource at the same time. In a way, it is similar to the reader-writer problem except that both parties in this problem have equal priority, with the only condition being mutual exclusion between the two parties.

## Results
Each solution prints when an employee arrives, when they enter the bathroom, and when they leave the bathroom. The employees sleep for random intervals to simulate the time between them arriving and to simulate the time to use the bathroom. The following results were gathered for each solution:

Test 1 - Correctness: The output of each solution on the same configuration (10 employees: 5 male, 5 female) is recorded. (Other test configurations were run, but for brevity only this one is recorded in the analysis).

Test 2 - Performance: The print and sleep statements are removed. The average duration of the program and wait time over 100 trials on the same configuration (100 employees: 50 male, 50 female) is recorded. The wait time is defined as the amount of time between an employee arriving and entering the bathroom.

### Solution 1 - `ub.py`
This implementation is written in Python and follows the solution described in the Little Book of Semaphores.

Test 1 Output:
```
Female employee 3 arrives.
Female employee 3 enters the bathroom.
Female employee 1 arrives.
Female employee 1 enters the bathroom.
Male employee 8 arrives.
Male employee 6 arrives.
Male employee 0 arrives.
Male employee 2 arrives.
Female employee 3 leaves the bathroom.
Female employee 1 leaves the bathroom.
Male employee 8 enters the bathroom.
Male employee 6 enters the bathroom.
Male employee 0 enters the bathroom.
Female employee 7 arrives.
Male employee 0 leaves the bathroom.
Male employee 2 enters the bathroom.
Female employee 9 arrives.
Male employee 8 leaves the bathroom.
Female employee 5 arrives.
Male employee 4 arrives.
Male employee 4 enters the bathroom.
Male employee 4 leaves the bathroom.
Male employee 6 leaves the bathroom.
Male employee 2 leaves the bathroom.
Female employee 7 enters the bathroom.
Female employee 9 enters the bathroom.
Female employee 5 enters the bathroom.
Female employee 9 leaves the bathroom.
Female employee 5 leaves the bathroom.
Female employee 7 leaves the bathroom.
```

Test 2 Output:
```
Average wait time: 1.0489583015441894e-05 s
Average duration: 0.060289435386657715 s
```

### Solution 2 - `ub-no-starve.py`
This implementation is also written in Python and uses a condition variable to prevent starvation in the infinite case.

Test 1 Output:
```
Female employee 3 arrives.
Female employee 3 enters the bathroom.
Male employee 8 arrives.
Female employee 7 arrives.
Male employee 4 arrives.
Female employee 3 leaves the bathroom.
Male employee 8 enters the bathroom.
Male employee 4 enters the bathroom.
Male employee 2 arrives.
Female employee 5 arrives.
Female employee 9 arrives.
Male employee 8 leaves the bathroom.
Male employee 6 arrives.
Male employee 0 arrives.
Female employee 1 arrives.
Male employee 4 leaves the bathroom.
Female employee 9 enters the bathroom.
Female employee 7 enters the bathroom.
Female employee 5 enters the bathroom.
Female employee 9 leaves the bathroom.
Female employee 5 leaves the bathroom.
Female employee 7 leaves the bathroom.
Male employee 2 enters the bathroom.
Male employee 6 enters the bathroom.
Male employee 0 enters the bathroom.
Male employee 0 leaves the bathroom.
Male employee 6 leaves the bathroom.
Male employee 2 leaves the bathroom.
Female employee 1 enters the bathroom.
Female employee 1 leaves the bathroom.
```

Test 2 Output:
```
Average wait time: 7.700371742248532e-06 s
Average duration: 0.06324758529663085 s
```

## Analysis
### Correctness
The Little Book of Semaphores presents the following synchronization constraints on the unisex bathroom problem:
1. There cannot be men and women in the bathroom at the same time.
2. There should never be more than three employees in the bathroom at the same time.

Both solutions satisfy these constraints.  
For constraint 1, in Solution 1, a `LightSwitch` class is used to ensure that there are never men and women in the bathroom at the same time. When the first employee of either sex arrives, it acquires the empty mutex with the `LightSwitch` class. Only when the last employee in the bathroom of that same sex leaves does the mutex get released. In Solution 2, a mode variable protected by a condition lock ensures that men can only enter the bathroom if the mode is currently `EMPTY` or `MALE`, and similarly women can only enter the bathroom if the mode is currently `EMPTY` or `FEMALE`.  
For constraint 2, both implementations use Semaphores of size 3 to ensure there are never more than 3 employees in the bathroom at the same time.  
While both solutions are correct in this sense, Solution 1 does not prevent starvation in the infinite case. This is not a constraint of the problem, but I think it is an important feature for correctness. Suppose that men get the mutex first. As long as more men keep arriving before all men leave the bathroom, this mutex will never be released, and the women will starve waiting forever in line. Even in the finite case, this means one sex may have to wait a very long time before being able to enter the bathroom. Solution 2 on the other hand uses condition variables to ensure that both sides get their turn without having to wait forever. If an employee arrives and the mode is set to the opposite sex, they wait on a condition variable. Suppose that men arrive and set the mode to `MALE` first. If a man arrives and sees that women are waiting, it does not enter the bathroom. When the last man leaves the bathroom, if it sees that women are waiting, it sets the mode to `FEMALE` and signals the condition variable those women are waiting on, otherwise it sets the mode to `EMPTY`. This ensures that no woman has to wait for more than 3 men before entering the bathroom and vice versa for men.

### Comprehensibility
Not including the code in `main()` which is mostly just overhead of setting up threads and calculating results, Solution 1 uses 47 lines of code while Solution 2 uses 68. So Solution 1's implementation is considerably shorter than Solution 1 and would probably take less work for somebody to read and understand.  
Solution 1 uses a lock, two semaphores, and two instances of the `LightSwitch` class, which essentially allow the men or women to maintain a lock on what kind of employees can enter the bathroom. Solution 2 only uses two multiplexes and a condition variable, all three of which are sychronization primitives. In this sense, Solution 2 is probably easier for a programmer who is already familiar with concurrency and synchronizaton primitives to understand because they would not have to additionally learn how the `LightSwitch` class works.  
Overall though Solution 1 is probably easier to understand because even without reading how the `LightSwitch` class works, the methods all make it very clear that each employee arrives, tries to acquire the bathroom lock for their sex, and once that is successful, they try to enter the bathroom if there are not 3 people in it already. Without the added complication that Solution 2 has of trying to synchronize the threads so that no one side ends up waiting forever, the flow of the code is a lot easier to follow in Solution 1.

### Performance
We can see from the results of Test 2 that the performance of both programs does not differ by very much. However, on average, employee threads wait for less time in Solution 2, but the program has an overall longer duration than Solution 1.   
This tradeoff is to be expected. In Solution 2, as mentioned earlier, a condition variable is used to ensure that neither sex has to wait for very long before being able to enter the bathroom, and this probably explains why the average wait time for each employee is shorter. However, the overhead of maintaining the communication and synchronization between the threads to ensure that neither side waits for too long probably causes the overall duration of Solution 2 to be longer than Solution 1. Another factor that may cause Solution 2 to have a larger overall duration is that it does not take full advantage of the concurreny available in the system. For example, suppose a woman is in the bathroom and a man arrives, and then two women arrive. Since the man is waiting, neither of the women who arrived will enter the bathroom, even though there is space for them in it.   
In terms of which approach performs better, it depends on what the user prioritizes. If we want each employee to wait for as little as possible before being able to use the bathroom, then Solution 2 performs better. However, if we just want the overall time it takes all the employees to use the bathroom to be as short as possible, then Solution 1 performs better.