Random Numbers
==============

How do you generate random variables between 0 and 1?

not how we do it anymore:
  - generate a sequence of integers
    - Xi+1 = (AXi + B) mod MAX_INT
    - where A and B are chosen (carefully)
    - Xo = "seed"
  - note this is a deterministic sequence
    - not actually random, given Xo
    - in particular, the same seed leads to the same sequence
      - good for debugging, bad for statistics
        - to gather meaningful information
      - practicality: get seed: ask the os for process id
      - generate seed only once per run, then run fixed sequence
  - for this sequence we desire:
    - to "look" random
    - rarely repeating patterns -> ideally hit every integer in [0, 2^32] exactly once before repeating "long cycle time"
    - long term average
    - google "diehard randomness test"
  - to use properly
    - seed only once per run
    - must use eery number given to
    - must use every bit of the number given
    - say:
      ```
      # incorrect way(?)
      irandom() -> integer in [0, 2^32]
      integers {0, 1, ..., 9}
      irandom() mod 10 # only uses ~3.5 bits -> ~12% randomness

      # correct way
      int(random() * 10)
      uniform random number between 0 and 1 [0, 1), times it by 10
      ```

#### Real randomness

- /dev/random


#### averages

time avg vs space avg
  - recall mean f^cn f(x) = int(a, b, x*f(x), x)
  - what is x?
  - suppose we drive 60 miles in 1 hour
    - what is the average speed
    - time average: what everyone's used to
      - 60 miles / 1 hour = 60 miles per hour
    - space average:
      - 120 mph for first 30 minutes
      - and then stop
      - = 120 mph

#### Population average

- time average usually measuring time average of a discrete variable.

avg waiting time for customers
  - 1/N * sum(1, N, Ti), Ti = customer is watiing time, accumulate only at events
