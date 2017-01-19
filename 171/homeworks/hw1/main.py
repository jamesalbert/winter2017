from agents import *
from itertools import combinations, cycle, product

agents = (
    ReflexVacuumAgent,
    RandomVacuumAgent,
    TableDrivenVacuumAgent,
    ModelBasedVacuumAgent
)

states = set(combinations(['Clean', 'Dirty'] * 3, 3))
locations = [(0, 0), (1, 0), (2, 0)]
opts = list(product(states, locations))
settings = product(agents, opts)

for i, setting in enumerate(settings):
    agent, opt = setting
    print(f"{i+1}. {agent.__name__}")
    states, location = opt
    status = dict()
    for i, loc in enumerate(locations):
        status[loc] = states[i]
    e = TrivialVacuumEnvironment(status)
    print(f"  location statuses: {e.status}")
    e.add_thing(agent(), location)
    e.run()
    print(f"  average performance over 1000 steps: {e.things[0].performance}")
