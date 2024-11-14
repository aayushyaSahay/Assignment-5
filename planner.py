from flight import Flight

class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        self.n_vertices = 0
        self.flights = flights # this will be necessary to get a fresh list of flights
        for flight in flights:
            self.n_vertices = max(self.n_vertices, flight.start_city, flight.end_city)
        self.adj_list = [[] for i in range(self.n_vertices+1)]
        for flight in flights:
            self.adj_list[flight.start_city].append(flight)
        self.debug = False
    
    def least_flights_ealiest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        arrives the earliest
        """
        bfs_queue_of_flights = myQueue()
        end_city_best_flight = None # this will contain the best flight to arrive at the end city
        for flight in self.adj_list[start_city]:
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                bfs_queue_of_flights.append(flight)
                flight.set_parent(None, 0)
        while not bfs_queue_of_flights.is_empty():
            flight = bfs_queue_of_flights.pop()
            dest_city = flight.end_city
            if dest_city == end_city:
                if end_city_best_flight == None:
                    end_city_best_flight = flight
                else:
                    if flight.n_flights < end_city_best_flight.n_flights:
                        end_city_best_flight = flight
                    elif flight.n_flights == end_city_best_flight.n_flights:
                        if flight.arrival_time < end_city_best_flight.arrival_time:
                            end_city_best_flight = flight
            else:
                for next_flight in self.adj_list[dest_city]:
                    if next_flight.parent != None: # ek bar kisiko assign ho gaya agar to fir agli bar nahi karna padega 
                        continue
                    elif next_flight.departure_time >= flight.arrival_time+20 and next_flight.arrival_time <= t2:
                        next_flight.set_parent(flight, flight.n_flights + 1)
                        bfs_queue_of_flights.append(next_flight)
        # start making up the path
        path = []
        flight = end_city_best_flight
        while flight != None:
            path.append(flight)
            flight = flight.parent
        if self.debug:
            print([flight.flight_no for flight in path])
        for flight in self.flights: # revert the changes
            flight.parent = None
            flight.n_flights = float('inf')

        return path[::-1]


    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route is a cheapest route
        """
        pqueue_for_flights = Heap(lambda x,y: x.cost_to_reach < y.cost_to_reach) # this will be based on a min-heap
        end_city_best_params = [None, float('inf')]
        for flight in self.adj_list[start_city]:
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                flight.set_parent(None, float('inf'), 0) # using the flight.cost_to_reach as the cost to reach that flight
                pqueue_for_flights.insert(flight)
        while not pqueue_for_flights.is_empty():
            flight = pqueue_for_flights.extract()
            dest_city = flight.end_city
            if dest_city == end_city:
                if end_city_best_params[0] == None:
                    end_city_best_params = [flight, flight.cost_to_reach + flight.fare]
                else:
                    if flight.cost_to_reach + flight.fare < end_city_best_params[1]:
                        end_city_best_params = [flight, flight.cost_to_reach + flight.fare]                        
            else:
                for next_flight in self.adj_list[dest_city]:
                    if next_flight.departure_time >= flight.arrival_time+20 and next_flight.arrival_time <= t2:
                        if next_flight.cost_to_reach > flight.fare + flight.cost_to_reach:
                            next_flight.set_parent(flight,float('inf'), flight.cost_to_reach + flight.fare)
                            pqueue_for_flights.insert(next_flight)
        # start making up the path
        path = []
        flight = end_city_best_params[0]
        while flight != None:
            path.append(flight)
            flight = flight.parent
        if self.debug:
            print([flight.flight_no for flight in path])
        for flight in self.flights: # revert the changes
            flight.parent = None
            flight.cost_to_reach = float('inf')
        return path[::-1]
        

        
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest
        """
        pqueue_for_flights = Heap(lambda x, y: (x.n_flights, x.cost_to_reach) < (y.n_flights, y.cost_to_reach)) # lexicographically check karta hai
        end_city_best_params = [None, float('inf'), float('inf')]
        for flight in self.adj_list[start_city]:
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                flight.set_parent(None, 0, 0) # n_flight and cost_to_reach both zero
                pqueue_for_flights.insert(flight)
        while not pqueue_for_flights.is_empty():
            flight = pqueue_for_flights.extract()
            dest_city = flight.end_city
            if dest_city == end_city:
                if end_city_best_params[0] == None:
                    end_city_best_params = [flight, flight.n_flights, flight.cost_to_reach + flight.fare]
                else:
                    if (flight.n_flights, flight.cost_to_reach + flight.fare) < (end_city_best_params[1], end_city_best_params[2]): # again lexicographic comparision
                        end_city_best_params = [flight, flight.n_flights, flight.cost_to_reach + flight.fare]                        
            else:
                for next_flight in self.adj_list[dest_city]:
                    # if next_flight.parent != None: # agar parent assign ho gaya hai fir bhi ho sakta hai ki aisa path mile jisme cost kam ho isliye ye nahi kar sakte yaha pe
                    #     continue
                    if next_flight.n_flights > flight.n_flights + 1:
                        if next_flight.departure_time >= flight.arrival_time+20 and next_flight.arrival_time <= t2:
                            next_flight.set_parent(flight,flight.n_flights+1, flight.cost_to_reach + flight.fare)
                            pqueue_for_flights.insert(next_flight)
                    elif next_flight.n_flights == flight.n_flights + 1:
                        if next_flight.departure_time >= flight.arrival_time+20 and next_flight.arrival_time <= t2:
                            if next_flight.cost_to_reach > flight.fare + flight.cost_to_reach:
                                next_flight.set_parent(flight,flight.n_flights+1, flight.cost_to_reach + flight.fare)
                                pqueue_for_flights.insert(next_flight)

        # start making up the path
        path = []
        flight = end_city_best_params[0]
        while flight != None:
            path.append(flight)
            flight = flight.parent
        if self.debug:
            print([flight.flight_no for flight in path])
        for flight in self.flights: # revert the changes
            flight.parent = None
            flight.n_flights = float('inf')
            flight.cost_to_reach = float('inf')
        return path[::-1]
    

    
# Utility classes:

class myQueue:
    def __init__(self, initial_capacity=10):
        self.items = [None] * initial_capacity
        self.size = 0
        self.head = 0
        self.tail = 0
        self.capacity = initial_capacity

    def append(self, item):
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        self.size += 1
        self.items[self.tail] = item
        self.tail = (self.tail + 1) % self.capacity

    def pop(self):
        if self.size == 0:
            return None
        self.size -= 1
        item = self.items[self.head]
        self.head = (self.head + 1) % self.capacity
        if self.size > 0 and self.size == self.capacity // 4:
            self._resize(self.capacity // 2)
        return item

    def is_empty(self):
        return self.size == 0

    def _resize(self, new_capacity):
        new_items = [None] * new_capacity
        for i in range(self.size):
            new_items[i] = self.items[(self.head + i) % self.capacity]
        self.items = new_items
        self.capacity = new_capacity
        self.head = 0
        self.tail = self.size

class Heap:
    def __init__(self, comparison_function=lambda x, y: x < y, initial_elements=None):
        self.comparison_function = comparison_function
        self.elements = initial_elements if initial_elements is not None else []
        self.size = len(self.elements)
        if initial_elements:
            self.build_heap()

    def is_empty(self):
        return self.size == 0
    def top(self):
        return self.elements[0] if self.size > 0 else None
    
    def build_heap(self):
        for i in range(self.size // 2, -1, -1):
            self.heapify_down(i)

    def heapify_down(self, index):
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index

        if left < self.size and self.comparison_function(self.elements[left], self.elements[smallest]):
            smallest = left
        if right < self.size and self.comparison_function(self.elements[right], self.elements[smallest]):
            smallest = right
        if smallest != index:
            self.elements[index], self.elements[smallest] = self.elements[smallest], self.elements[index]
            self.heapify_down(smallest)

    def insert(self, value):
        self.elements.append(value)
        self.size += 1
        self.heapify_up(self.size - 1)

    def heapify_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.comparison_function(self.elements[index], self.elements[parent]):
            self.elements[index], self.elements[parent] = self.elements[parent], self.elements[index]
            self.heapify_up(parent)

    def extract(self):
        if self.size == 0:
            return None
        root = self.elements[0]
        self.elements[0] = self.elements[self.size - 1]
        self.size -= 1
        self.elements.pop()
        self.heapify_down(0)
        return root