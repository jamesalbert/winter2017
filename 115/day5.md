distortion of stats during being/end of sim

assume sum 24/7 manufacturing system

' system busy, running close to full speed

start of sum, system is not busy yet

end of sim, what to do with object currently in q

special purpose simulation language

provide
  - generating pseudo random numbers u[0,1] other pdfs
  - keep track of sim time,
  - determine next event to handle passing control to that event
  - list manipulation (waiting lines, q's)
  - data collection and analysis
  - report generation
  - error detection


## special purpose
  - include commonly-used constructs -> less coding time
  - easier to describe system being sumulated
  - favorite sim language may not be available
  - higher level description
  - easier to change the model
  - simulation not hot software topic
  - sim languages may be old

## general purpose lange
  - programmer already familiar with some lang -> less learning required
  - some general purpose language on a given computer
  - flexibility of custom code.
  - faster code

## in general purpose language
  - imperative 9sequence of instructions)
    - statement oriented expression
  - lisp "applicative" apply ops to a lisp
  - prolog logic-oriented

## special purpose sim language
  - defining entities what they do during "lifetime", how they relate to other entities

Imagine film director in movie about football game.
  - in general, must define how various entities behave overtime.
  - assume somebody pre-planned the choreography
  - Method 1:
    - animation, with list of instructions stating, in sequence, which moves to make.
    - event-scheduling approach.
  - Method 2:
    - giving each actor a sequence of time events/instructions
    - "when the quarterback seq 99, run 10 yards forward, turn around and catch the ball, run left"
    - Process interation approach
      - each entitity has it's own (virtual/real) processor
      - you program it to follow only it's own instructions , subject to communication or sysnchronization with other entities (or objects).
      - allows true parallelism in languages that support


CSIM:
  - facility: (data type) resource such as a queue, service center, etc

```csim
declare FACILITY f=
allocate f=facility("line at entrance")
reserve(f); <- process goes to sleep until resource is available
or f.reserve();

release(f); <-
```
  - storage: resource with potential many sub-entities
    - eg seats in a theatre

```csim
STORE s = storage('seating', 100);

```
