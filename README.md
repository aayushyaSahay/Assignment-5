
# New Idea: Take Departure Gates of Flights as Individual Vertices

---

## What's the new data structure?
- Each **city** is a **supernode** that contains a list of vertices of the graph.
- When you access any **vertex**, you get the **arriving city**, and hence, the list of **arriving gates**.
- All these gates will then be accessed according to the **arrival time** being in the <20 range.
- Assign these gates to the **first flight** that has reached them.
  - Any other flight arriving at these gates won’t be able to change the **parent flight** since the **departure time** is the same, and there is no way fewer flights will be reached later in BFS.
- Keeping flights in the **parent array** of the departing gates will help in **backtracking**.
- Also, keep track of the **number of flights taken** to reach each gate.
  - Thus, you need to store **(parent, dp)** for each gate:
    - `parent` will be the previous flight.
    - `dp` will be the number of flights taken to reach the gate.
- Each gate is associated with the **departing city**; hence, each city maintains a list of its gates.
- Maintain a list of **objects** (flight, parent, dp) for all departing flights.

---

## How would you implement the first part?
1. Start from the **start_city** and enqueue all objects (elements of the list in the supernode) in the queue.
2. Keep popping out the objects and visit the city to which the flight leads.
3. In the new city, choose the eligible flights and mark their **parent** as the current flight.

---

### Test Case for Checking:
```python
flights = [
    Flight(0, 0, 0, 1, 50, 50),      # City 0 to 1
    Flight(1, 0, 0, 2, 10, 200),     # City 0 to 2           
    Flight(2, 2, 30, 1, 40, 20),     # City 2 to 1
    Flight(3, 1, 70, 3, 80, 120),    # City 1 to 3           
    Flight(4, 3, 100, 4, 110, 100),  # City 3 to 4           
    Flight(5, 1, 60, 4, 70, 500),    # City 1 to 4               
]

expected_route1 = [flights[1], flights[2], flights[-1]]
```

---

## How would you implement the next part?
- Implement **Dijkstra's algorithm** with **cost** as the priority parameter in the min-heap or priority queue.
- While checking flights, ensure the `arrival_time+20` and `t2` bounds are respected.
- Use `flight.cost_to_reach` as the **fare** to reach the flight, adjusting Dijkstra’s condition:
    ```python
    if next_flight.cost_to_reach > flight.fare + flight.cost_to_reach:
        next_flight.set_parent(flight, float('inf'), flight.cost_to_reach + flight.fare)
        pqueue_for_flights.insert(next_flight)
    ```

---

## Handling Shortest Path: What changes to make?
- To minimize **cost**, use the same algorithm as before, but include **n_flights** (number of flights) as an additional parameter:
    ```python
    pqueue_for_flights = Heap(lambda x, y: (x.n_flights, x.cost_to_reach) < (y.n_flights, y.cost_to_reach))
    ```
- Add the following checks:
    ```python
    # When two paths compete, choose the one with fewer flights
    if next_flight.n_flights > flight.n_flights + 1:
        if next_flight.departure_time >= flight.arrival_time + 20 and next_flight.arrival_time <= t2:
            next_flight.set_parent(flight, flight.n_flights + 1, flight.cost_to_reach + flight.fare)
            pqueue_for_flights.insert(next_flight)

    # If two paths have the same number of flights, compare costs
    elif next_flight.n_flights == flight.n_flights + 1:
        if next_flight.departure_time >= flight.arrival_time + 20 and next_flight.arrival_time <= t2:
            if next_flight.cost_to_reach > flight.fare + flight.cost_to_reach:
                next_flight.set_parent(flight, flight.n_flights + 1, flight.cost_to_reach + flight.fare)
                pqueue_for_flights.insert(next_flight)
    ```

---

## Miscellaneous Points
- Add any points if you find them not listed here.
- Remember to **reset** the attributes of flights after operating on them.

---
