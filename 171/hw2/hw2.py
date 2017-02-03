from random import choice, randint, shuffle
from search import *
from time import perf_counter


'''
Part 1: 8-puzzle
'''


def random_puzzle():
    puzzle = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    shuffle(puzzle)
    return tuple([
        tuple(puzzle[0:3]),
        tuple(puzzle[3:6]),
        tuple(puzzle[6:9])
    ])


def getInvCount(arr):
    inv_count = 0
    for i in range(8):
        for j in range(i + 1, 9):
            # Value 0 is used for empty space
            if arr[j] and arr[i] and arr[i] > arr[j]:
                inv_count += 1
    return inv_count


# This function returns true if given 8 puzzle is solvable.
def isSolvable(puzzle):
    # Count inversions in given 8 puzzle
    invCount = getInvCount([item for sublist in puzzle for item in sublist])
    # return true if inversion count is even.
    return invCount % 2 == 0

rp = None
while True:
    rp = random_puzzle()
    if isSolvable(rp):
        break

for AlGoreRhythm in [astar_search, recursive_best_first_search]:
    print(f"trying to solve solvable puzzle: {rp} using {AlGoreRhythm.__name__}")
    puzzle = EightPuzzleSearchProblem(
        rp,
        ((0, 1, 2),
         (3, 4, 5),
         (6, 7, 8)))
    start = perf_counter()
    AlGoreRhythm(puzzle)
    # AlGoreRhythm(puzzle, h=lambda node: puzzle.h(node) + randint(1, 5))
    print(f"solved puzzle in {perf_counter() - start:.2f} seconds with {puzzle.num_states} generated")

'''
Part 2: TSP
'''


def r():
    return randint(20, 151)

romania_map = UndirectedGraph(dict(
    Arad=dict(Zerind=r(), Sibiu=r(), Timisoara=r()),
    Bucharest=dict(Urziceni=r(), Pitesti=r(), Giurgiu=r(), Fagaras=r()),
    Craiova=dict(Drobeta=r(), Rimnicu=r(), Pitesti=r()),
    Drobeta=dict(Mehadia=r()),
    Eforie=dict(Hirsova=r()),
    Fagaras=dict(Sibiu=r()),
    Hirsova=dict(Urziceni=r()),
    Iasi=dict(Vaslui=r(), Neamt=r()),
    Lugoj=dict(Timisoara=r(), Mehadia=r()),
    Oradea=dict(Zerind=r(), Sibiu=r()),
    Pitesti=dict(Rimnicu=r()),
    Rimnicu=dict(Sibiu=r()),
    Urziceni=dict(Vaslui=r())))
root = choice(romania_map.nodes())
dest = None
while True:
    dest = choice(romania_map.nodes())
    if dest != root:
        break

for AlGoreRhythm in [astar_search, recursive_best_first_search]:
    print(f"trying to find a path from {root} to {dest} using {AlGoreRhythm.__name__}")

    tsp = TSPSearchProblem(root, dest, romania_map)
    start = perf_counter()
    AlGoreRhythm(tsp)
    print(f"path found {perf_counter() - start:.5f} seconds  with {tsp.num_states} generated")
