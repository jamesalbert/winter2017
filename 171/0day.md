actors
======

P[S* -> A]

Vacuum World State:
  - state spaces:
    - basic:
      - bit / boolean = 0 or 1
      - natural numbers
        - [up to a certain number]
    - combinations:
      - type constructors
        - discrete sum (union in C)
    - connectivity:
      - or graph structure
      - or move structure
  - Bl (move left) x Br (move right) x Bu (suck)
  - Observable, start in #5
    - Solution?
      - [Right, Suck]
  - Unobservable, start in {1,2,3,4,5,6,7,8}
    - Solution?
      - [Right, Suck, Left, Suck]

Search:
  - Formulate "what to do" as a search problem
    - solution tells the agent what to do if no solution in the current search spaces
      - find space that does contain a solution (use search)
        - solve original problem in new search spaces.

State space problem:
  - a problem is defined by four items:
    - initial state e.g. "at Arad"
    - actions: Actions(s) = set of actions avail in state s
    - transition model Results(s, a) = state that results from action a in states
      - Alt: successor function S(x) = set of action-state pairs
        - S(Arad) = {<Arad -> Zerind, Zerind>, ...}
    - goal test ( or goal state)
      - x = "at Bucharest", Checkmate(x)
    - path cost (additive)
      - sum of distances, number of actions executed, etc
      - c(x,a,y) is the step cost, assumed to be >= 0
    - a solution is a sequence of actions leading from the initial state to a goal state

Vacuum world revisited
  - states?
    - discrete: dirt, location
  - initial state:
    - any
  - actions?
    - left, right, suck
  - goal test
    - no dirt at all
  - path cost?
    - 1 per action

8 queens:
  - place as many queens as possible on the chess board without capture
    - states:
      - any arrangement of n <= 8 queens
      - state space = big number
    - initial state
      - no queens on the board
    - actions
      - add queen to any empty square
        - or add queen to leftmost empty sqaure such that it is not attacked by other queens
    - goal test
      - 8 queens on the board, none attacked
    - path cost
      - q per move (not relevant)

Robitic assembly
  - states
    - real-values coordinates of robot joint angles and parts of the object to be assembled
  - initial 0


Uninformed Search
  - strategies:
    - uninformed (blind):
      - you have no clue whether one non-goal state is better than any other. your search is blind.
