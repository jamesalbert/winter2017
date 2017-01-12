Introduction
============

Textbook: "Distributed Systems" Andrew Tanenbaum and maarten van steen 2nd edition

Office hours:
  Prof: after each lecture by appointment
  TA: Tu at 10am

Objectives:
  learn basic principles of distributed system design

  learn basic of distributed system programming
    - labs

  parallel systems are a special case of distributed systems, but have a specific
  case of distributed systems, but have specific tools and approached to programming

Topics:
  hardware parallel and distributed systems
  os support
  programming models
  parallel/distributed programming and performance
  coordination and synchronization
  consistency and replication
    - including cache coherence
  fault tolerance
  data centers

LABS ARE INDIVIDUAL
  - will use MOSS

Homework solutions will be in discussion section

No late submissions without prior contact

Grading (on a curve)
  - 60% assignments (6 total, different weights)
  - 40% exams

Grading issues - please resolve within 1 week
  - after scores are posted


Language:
  - C++ std 11



@DEFINITION
What is a distributed system?
  - a distributed system (DS) is a collection of independent computers that
    appears to its users as a single coherent system.


@DEFINITION
What is a parallel system?
  - specialized for the type of programs that people might write
  - a special case of a distributed system
    - for certain use cases

A layered distributed system architecture

    Machine A - Machine B - Machine C
    ----distributed applications--
    ------------------------------
    ----Middleware service--------
        |         |         |
    Local OS - Local OS - Local OS


@DEFINITION
Middleware Layer: MPI runtime (Message Passing Interface)

P&D systems - why do we need them?
  - it is almost impossible to find a single-processor system
  - millions of computers are connected through networks
    - internet
  - there is too much data for one computer
  - each computer may have different resources to share
  - one computer is not fast enough to solve a problem
  - and many other reasons


How much data can it handle?
  - Gigabytes of memory (fast)
  - Terabytes of disk (slow)

Many different types of resources are used
  - printers
  - file servers
  - parallel computers
  - video/audio streaming

some are a computer, others attached to one

Need software for a user to:
  - find them
  - access them
  - send data, execute jobs on them, and get results back
  - in a straightforward and transparent way


@DEFINITION
Programming Models:
  - a single processor model (von Neumann)
    - set of instructions
    - set of data types
    - instructions and data in memory
      - transparently to a user they migrate to caches
    - program counter PC points to the next instructions

  - A (shared memory) multi-core processor Models
    - each processor follows a single-processor Models
    - all processors share the same memory
    - need additional instructions for coordination
    - need to keep caches and memory consistent
    - need inter-processor interrupt


Major DS design goals:
  - Transparensy: hide the fact tha reources are distributed
  - openness: allow extendibility
  - scalability: ability to grow with problems
  - security, fault-tolerance

Transparensy:
  - is complete Transparensy alays desired?
  - many different types (levels) of Transparency exist
    - access
    - location
    - migration
    - relocation
    - replication
    - concurrency
    - failure
    - persistence

Scalability
  - ability to grow
      - one of the key advantages of distributed systems
        - adapt to new requirements, like more users`
  - centralization of resources limits scalability
  - replication and caching improves scalability
    - BUT they lead to consistency problems
      - multiple copies exist and may be different

Scalability Problems:
  - centralized services: single server for all users
  - centralized data: single online telephone book
  - centralized algorithmsL doing routing based on complete information

Scaling Techniques:
    - replication helps limit performance problems
      - local servers
      - multiple resources - google computer farm
    - caching is a special form of replication
    - replication/caching lead to consistency problems
      - multiple copies may differ
        - consider browser caching

Possiblem Implementations:
  - consider a large database with many users, how to implement:
    - one central database
    - multiple database partitions distributed somehow
    - each computer has a full database
