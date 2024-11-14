# New Idea : Take the departure gates of the flights as individual vertices

## What's the new data structure?
- each city is a supernode that contains the list of vertices of the graph
- when you access any vertex, you get the arriving city, and hence you get the list of arriving gates
- all these gates will then be accessed according to the arrival time being in the < 20 range 
- you will assign these gates the first flight that has reached these gates
- any other flight that reaches such gates won't be able to change the parent flight because the departure time is same, and there is no way that you get less number of flights later in bfs
- keeping the flights in the parent array of the departing gates will help in backtracking
- also keep a number the number of flights taken to reach the corresponding gate
- hence you need to store (parent, dp) for each of the gates, parent will be the just before flight and dp will be the number of flights taken to reach the gate
- each gate is associated with the departing city hence in each city you will keep a list of these gates.
- keep a list of objects(flight, parent, dp) for all the departing flights.

## How would you implement the first part?
- start from the start_city and enqueue all the objetcs (elements of the list in the supernode) in the queue
- keep popping out the objects and visit the city where this flight leads to
- in the new city, choose the eligible flights and mark their parent as this 


- the test case for checking is :
```
flights = [
    Flight(0, 0, 0, 1, 50, 50),      # City 0 to 1
    Flight(1, 0, 0, 2, 10, 200),     # City 0 to 2           
    Flight(2, 2, 30, 1, 40, 20),     # City 2 to 1
    Flight(3, 1, 70, 3, 80, 120),   # City 1 to 3           
    Flight(4, 3, 100, 4, 110, 100),  # City 3 to 4           
    Flight(5, 1, 60, 4, 70, 500),  # City 1 to 4               
]

expected_route1 = [flights[1], flights[2], flights[-1]]  
```

## Now how would you implement the next part?
- in this you just implement the dijkstra algorithm on the cost as the parameter/bias in the min-heap or the priority queue
- while checking the flights you will just need to check the arrival_time+20 and t2 range bounds
- here flight.cost_to_reach can be utilised as the fare to reach the flight
- so you can change the dijkstra's condition by:
    ```
    if next_flight.cost_to_reach > flight.fare + flight.cost_to_reach:
        next_flight.set_parent(flight,float('inf'), flight.cost_to_reach + flight.fare)
        pqueue_for_flights.insert(next_flight)
    ```
## The last part is where you would also have to consider the shortest path as well, so what change to make?
- since you have to minimise the cost, this part is going to use the similar algo as the last part
- further, we can see the "shortest-path" similarity from the first part hence we need to include the n_filghts required to reach the flight as one of the paramaters as well, like this:
    ```
    pqueue_for_flights = Heap(lambda x, y: (x.n_flights, x.cost_to_reach) < (y.n_flights, y.cost_to_reach))
    ```
- after this, you just need to add these checks:
    ```
    # when two paths compete and the current is smaller than the already present, then the current one is the winner
    if next_flight.n_flights > flight.n_flights + 1:
        if next_flight.departure_time >= flight.arrival_time+20 and next_flight.arrival_time <= t2:
            next_flight.set_parent(flight,flight.n_flights+1, flight.cost_to_reach + flight.fare)
            pqueue_for_flights.insert(next_flight)

    #if two paths compete for the shortest path, you should just check the cost to decide the winner
    elif next_flight.n_flights == flight.n_flights + 1: 
        if next_flight.departure_time >= flight.arrival_time+20 and next_flight.arrival_time <= t2:
            if next_flight.cost_to_reach > flight.fare + flight.cost_to_reach:
                next_flight.set_parent(flight,flight.n_flights+1, flight.cost_to_reach + flight.fare)
                pqueue_for_flights.insert(next_flight)
    ```

## Miscellaneous Points!
- remember to reset the attributes of the  
