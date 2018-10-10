# Dining Philosophers

The Little Book of Semaphores states that the Dining Philosophers problem "was proposed by Dijkstra in 1965, when dinosaurs ruled the earth". Obviously I could not pass up the chance to implement such a classic problem. For those of you living under a rock, the basic premise is that there is a table with 5 seats and 5 chopsticks, with one big bowl of rice in the middle. Five philosophers come to the table and each loops forever between thinking and eating. When a philosopher eats, it grabs the chopsticks that are on either side of it, which means it may have to wait for its neighbour to finish eating so that it can acquire both chopsticks. The diagram below illustrates this scenario.  
![Dining Philsophers Image](https://github.com/kulvirs/concurrency-problems/blob/master/dining-philosophers/dp.PNG)

## Applications
