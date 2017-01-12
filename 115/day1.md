Flavors of Simulation
=====================

#### Static vs Dynamic
  - static:
    - time is passing in Simulation
    - monte carlo integration
    - numerical quadrature
      - estimating area under the curve
    - load on a bridge
  - dynamic:
    - orbits of planets
    - customers arriving at a bank
      - or packets arriving in system

#### Deterministic vs. Stochastic
  - deterministic:
    - newtonian physics
      - no randomness
      - initial state completely defines the solution (if dynamic)
    - may be a very long calculation
  - Stochastic:
    - randomness involved
      - real or psuedo
      - arrivals in queue
      - input is random -> output is random
        - so must be careful to ensure robust statistics on the output variables

#### Discrete Vs. Continuous
  - discrete:
    - time, or space or entities
    - people in  a bank
    - events: arrival, departures, begin service
  - continuous:
    - motion
    - space + time

#### Simulations *almost* always make errors
  - estimating errors is *vital*
  - one exception is a discrete deterministic system with few enough entities and relationships to explicitly list them all in your simulation.
    - FSM, FSA (Cellular automata)

#### monte carlo:
  - has sampling error or statistical noise

#### Queueing systems
- this course will focus on dynamic, Stochastic, discrete systems/simulations.
  - queueing systems

#### Time
  - continuous
  - ways to handle time in simulation.
    - time-driven simulation.
      - choose some small time interval, delta t.
      - figure out what's happening at time 0
      - advance time forward

  - we'll use event-driven time sumulation
    - you don't have to choose a delta t beforehand
    - we look at interesting points in time (events) when an even occurs


balk
  - insert into queue and for some reason, it leaves
    - restaurant is too packed
