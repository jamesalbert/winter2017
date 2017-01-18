Stats Review
============

Assignment1 is due thurs week 3
  - a1 must use non-siumulation language

Arrival Process
  - all arrive/entities act independently "arrival rate", 2 customer / minute = r
  - 1 / r = average inter-arrival time (eg 30s = 1/2 minute/customer) = average arrival rate


Poisson Distribution:
  - number of events = k
  - p(k) = (e^-r * r^k) / k! on unit interval
  - this whole thing is called the poisson arrival process
  - arrivals are distributed uniformly at random in any given interval
  - with interval L, expect ~Lr total arrivals
  - results in:
    - Let N(t) be cumulative arrivals in internal [0, t]
    - P(N(t) = k) = (e^(-rt) * (rt)^k) / k!
      - in particular P(N(t)=0) = e^-rt # the probability that no body has arrived yet is tiny and is getting smaller

therefore:
  - P(N(t) > 0) = 1 - e^(-rt) <=> P(A1, <= t) = 1 - e^(-rt)

Recall exponential distribution f(t) = r*e^-rt
claim: inter arrival times in a poisson arrival process are exponentially distributed
  - f(t) = re^(-rt) => F(t) = P(T<=t)
  - F(t) = int(0, t, re^(-rx) dx)
  - = [-e^(-rx)] for x = [0, t]
  - = [e^(-rx)] for x = [t, 0]
  - = 1 - e^(-rt)
  - we've worked out the distribution of the distance between inter-arrival times; how much time to expect between the arrival of customer k and the arrival of customer k+1.
    - interarrival times in a poisson arrival process is exponentially distributed.


Entities and Relationships
==========================

- these are the things we need to define before writing code
- what are the entities i'm going to have to model.

#### banks and tellers

- entities:
  - individual customers
  - tellers
  - queue of customers
- relationships:
  - implicit in the state diagram
  - state diagrams:
    - for each entity, we will draw a directed graph where each entity has states, and a state by definition (derived by "static") are static, and events that change the state.
    - events are directed edges
  - customer state diagram:
    - first state: outside the bank
      - arrival event happens

```
Customer State Diagram

          +------------+
          |being served|  
     +----+------------+--+
     |                    ^
     |departure           | Start service
    \/                    |
+-------+   arrival   +--------+
|outside|------------>|In queue|
+---^---+----+        +--------+
    |        |
    |  balk  |
    ---------+

Teller State Diagram

      arrival to empty queue
+------+  /-------\  +--------+
| Busy |--         --|Not Busy|
+------+  \_______/  +--------+
  departure with nobody in queue

Queue State Diagram

  arrival arrival arrival
|0| -> |1| -> |2| -> ... -> |k|
    <-     <-     <- ... <-
  departure departure departure/
   start service for each departure
```

- all action occurs along arrows
- your code is written to implement events which will change states of various entities.


#### Event Routines
- must handle all possibilities of all state changes for all entities affected by that event
- not all states need to be explicitly stored, for example the queue size

#### Event graph

```
  +____+
  |    |
  |  |arrival|..........|start service|---->|end service|
  |    ^       .                  ^              .
  |____|        .>|enter queue|   .            . .
               .                  .          .  \./
               .                 .         .  |departure|
                .>|exit queue|...  < . . .

```

#### Pseudocode

```python
queue = []
event_list = []

def schedule_next_customer_arrival():
  delta_t = generate_interarrival_time()  # exponential
  cust = generate_customer_object()
  event_list.append(cust)
  if teller not busy:
    schedule_start_service('myself', time=now)
  else:
    schedule_enter_queue('myself')

def customer_arrival(customer):
    schedule_next_customer_arrival()  # stochastic

```
