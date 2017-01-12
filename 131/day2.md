Distributed Systems
===================

#### Definition

review: collection of independent computers that appears to its users as a single coherent system

standard software engineering rules are not enough, pitfalls include assuming:
  - network is reliable
  - network is secure
  - network is homogeneous
  - topology does not change
  - latency is zero
  - bandwidtch is infinite
  - transport cost is zero
  - there is only one admin

most ds design principles relate to assuming that one or more of these are false

DS:
  - (computing) targets increase in application performance
  - (information) supports enterprise computing
  - (pervasive) collections of small devices, not even always on

MPI - message passing interface

SPMD - single program multiple data
  - every node runs the same program

grid - intergrate resources on the internet
  - layered sofrware organization
    - fabric layer: interface to local resources at a given site
    - communication layered
      - authentication, communication
    - resource layer: alows access to a given resource
      - access control, configuration data access, specific operations
    - collective layer: access to multiple resources
      - resource discovery, allocation, scheduling

Transaction processing Systems
  - some similarity to mutual exclusion
    - transactions are used to protect data
  - a much more powerful model
    - access/modify mnay data items in one atomic operation
    - all or nothing operations
      - either all data is accessed/modified or all is aborted
        - aborted = no state change occurs
    - the origin is in business transactions
      - neggatiation followed by contract
    - distributed systems and transactions are similar

store inventory computation
  - input: tapes of last inventory, today's sales+deliveries

computation can be aborted at any time
  - rewind tapes, start over


atomic
  - all or nothing
  - looks like everything happens at once

consistent
  - maintains system invariants
    - during a transaction may not be consistent
      - no one can observe that

isolated or serializable
  - concurrent transactions do not affect each other
  - result is as if they ran sequentially in some order

durable
  - after commit the results ARE made permanent

#### Distributed Hardware Concepts

issues:
  - what is a basic "node"?
    - cpu plus cache plus ...
      - a complete system
        - can run OS, necessary IO devices, etc
  - communication:
    - is there memory sharing
      - single address space
      - distributed shared memory
    - message passing
  - what is the interoconnect?
    - bus, switch, networks

multiprocessors:
  - a single system with multiple cpus
    - everything else is typically shared in hw
    - single memory address space, cache coherence
  - hard to achieve scalability
  - easier to program?

multicomputers
  - a set of independent nodes
    - each node a complete system
    - can be heterogeneous nodes
    - how to connect?
  - more scalable
  - harder to program?

why interconnects matter?
  - different latencies
    - affects scalability
  - different bandwidth
    - affects scalability
  - single or multiple paths between nodes
    - affects fault tolerance

MP/MC interconnect
  - processors and memories are all the same
  - each processor can access any memory, with conflicts
    - or access any other processor

other interconnect types:
  - gird or mesh (cube or torus in 3d)
    - now there are "5D" cubes in supercomputers
  - hypercube and other variants

multiprocessors
  - each node is your nasic microprocessor
  - interconnected by a memory bus
    - a bus-based multiprocessor
  - cache for performance (replicated memory)
    - lowers avergage memory latency
    - creates memory coherence problems

```
|CPU|........|CPU|
|L1|         |L1|
|L2|         |L2|
+---------------+
|     L3        |
+---------------+
+---------------+
|     MEM       |
+---------------+
```

intel terminology: processor = socket
  - not a core

additional instructions for locking, indivisibility
  - atomic processor instructions to atomically update a memory space
  - the atomic instructions use a lock prefix on the instruction and having the destination operand assigned to a memory address
  - intel processors support these instructions iwth a loc prefix
    - ADD, ADC, AND, BTC, etc

inter-processor interrupt (IPI)
  - each processor has an APIC
  - a processor puts the IV, destination ID into its local APIC
  - its lcoal APIC delivers it to the remote APIC

```
--------------
    |  P1     |       Pn
APIC|---------      ........
    |  Cache  |         |         _________
--.-----------          |         |       |
  .     |_______________|_________|   MEM |
  ................................|________
```

heterogeneous multicomputers
  - nodes are different types of computers
  - running different OS's
  - having different types of IO devices
    - this is true of all multicomputers

processor virtualization
  - want to run multple OS's on the same processor
    - technology developed at IBM in 80's
  - need 'a private OS' underneath
    - the hypervisor (Intel term = VMM)
      - intel provides VM extensions (VMX)
  - what processor support is required?
