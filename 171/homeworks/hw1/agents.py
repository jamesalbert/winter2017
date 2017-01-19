"""Implement Agents and Environments (Chapters 1-2).

The class hierarchies are as follows:

Thing ## A physical object that can exist in an environment
    Agent
        Wumpus
    Dirt
    Wall
    ...

Environment ## An environment holds objects, runs simulations
    XYEnvironment
        VacuumEnvironment
        WumpusEnvironment

An agent program is a callable instance, taking percepts and choosing actions
    SimpleReflexAgentProgram
    ...

EnvGUI ## A window with a graphical representation of the Environment

EnvToolbar ## contains buttons for controlling EnvGUI

EnvCanvas ## Canvas to display the environment of an EnvGUI

"""

# TO DO:
# Implement grabbing correctly.
# When an object is grabbed, does it still have a location?
# What if it is released?
# What if the grabbed or the grabber is deleted?
# What if the grabber moves?
#
# Speed control in GUI does not have any effect -- fix it.

from statistics import mean

import random
import copy
import collections

# ______________________________________________________________________________


class Thing(object):

    """This represents any physical object that can appear in an Environment.
    You subclass Thing to get the things you want.  Each thing can have a
    .__name__  slot (used for output only)."""

    def __repr__(self):
        return '<{}>'.format(getattr(self, '__name__', self.__class__.__name__))

    def is_alive(self):
        "Things that are 'alive' should return true."
        return hasattr(self, 'alive') and self.alive

    def show_state(self):
        "Display the agent's internal state.  Subclasses should override."
        print("I don't know how to show_state.")

    def display(self, canvas, x, y, width, height):
        # Do we need this?
        "Display an image of this Thing on the canvas."
        pass


class Agent(Thing):

    """An Agent is a subclass of Thing with one required slot,
    .program, which should hold a function that takes one argument, the
    percept, and returns an action. (What counts as a percept or action
    will depend on the specific environment in which the agent exists.)
    Note that 'program' is a slot, not a method.  If it were a method,
    then the program could 'cheat' and look at aspects of the agent.
    It's not supposed to do that: the program can only look at the
    percepts.  An agent program that needs a model of the world (and of
    the agent itself) will have to build and maintain its own model.
    There is an optional slot, .performance, which is a number giving
    the performance measure of the agent in its environment."""

    def __init__(self, program=None):
        self.alive = True
        self.bump = False
        self.holding = []
        self.performance = 0
        if program is None:
            def program(percept):
                return eval(input('Percept={}; action? ' .format(percept)))
        assert isinstance(program, collections.Callable)
        self.program = program

    def can_grab(self, thing):
        """Returns True if this agent can grab this thing.
        Override for appropriate subclasses of Agent and Thing."""
        return False


def TableDrivenAgentProgram(table):
    """This agent selects an action based on the percept sequence.
    It is practical only for tiny domains.
    To customize it, provide as table a dictionary of all
    {percept_sequence:action} pairs. [Figure 2.7]"""
    percepts = []

    def program(percept):
        percepts.append(percept)
        action = table.get(tuple(percepts))
        return action
    return program


def RandomAgentProgram(actions):
    "An agent that chooses an action at random, ignoring all percepts."
    return lambda percept: random.choice(actions)

# ______________________________________________________________________________


def SimpleReflexAgentProgram(rules, interpret_input):
    "This agent takes action based solely on the percept. [Figure 2.10]"
    def program(percept):
        state = interpret_input(percept)
        rule = rule_match(state, rules)
        action = rule.action
        return action
    return program


def ModelBasedReflexAgentProgram(rules, update_state):
    "This agent takes action based on the percept and state. [Figure 2.12]"
    def program(percept):
        program.state = update_state(program.state, program.action, percept)
        rule = rule_match(program.state, rules)
        action = rule.action
        return action
    program.state = program.action = None
    return program


def rule_match(state, rules):
    "Find the first rule that matches state."
    for rule in rules:
        if rule.matches(state):
            return rule

# ______________________________________________________________________________

loc_A, loc_B, loc_C = (0, 0), (1, 0), (2, 0)  # The three locations for the Vacuum world


def RandomVacuumAgent():
    "Randomly choose one of the actions from the vacuum environment."
    return Agent(RandomAgentProgram(['Right', 'Left', 'Suck', 'NoOp']))


def TableDrivenVacuumAgent():
    "[Figure 2.3]"
    table = {((loc_A, 'Clean'),): 'Right',
             ((loc_A, 'Dirty'),): 'Suck',
             ((loc_B, 'Clean'),): 'Left',
             ((loc_B, 'Dirty'),): 'Suck',
             ((loc_C, 'Clean'),): 'Left',
             ((loc_C, 'Dirty'),): 'Suck',
             ((loc_A, 'Clean'), (loc_A, 'Clean')): 'Right',
             ((loc_A, 'Clean'), (loc_A, 'Dirty')): 'Suck',
             # ...
             ((loc_A, 'Clean'), (loc_A, 'Clean'), (loc_A, 'Clean')): 'Right',
             ((loc_A, 'Clean'), (loc_A, 'Clean'), (loc_A, 'Dirty')): 'Suck',
             # ...
             }
    return Agent(TableDrivenAgentProgram(table))


def ReflexVacuumAgent():
    "A reflex agent for the two-state vacuum environment. [Figure 2.8]"
    def program(percept):
        location, status = percept
        if status == 'Dirty':
            return 'Suck'
        elif location == loc_A:
            return 'Right'
        elif location == loc_B:
            return 'Left'
        elif location == loc_C:
            return 'Left'
    return Agent(program)


def ModelBasedVacuumAgent():
    "An agent that keeps track of what locations are clean or dirty."
    model = {loc_A: None, loc_B: None, loc_C: None}

    def program(percept):
        "Same as ReflexVacuumAgent, except if everything is clean, do NoOp."
        location, status = percept
        model[location] = status  # Update the model here
        if model[loc_A] == model[loc_B] == model[loc_C] == 'Clean':
            return 'NoOp'
        elif status == 'Dirty':
            return 'Suck'
        else:
            if location == loc_A:
                return 'Right'
            elif location == loc_C:
                return 'Left'
            else:
                if model[loc_A] == 'Dirty':
                    return 'Left'
                else:
                    return 'Right'
    return Agent(program)

# ______________________________________________________________________________


class Environment(object):

    """Abstract class representing an Environment.  'Real' Environment classes
    inherit from this. Your Environment will typically need to implement:
        percept:           Define the percept that an agent sees.
        execute_action:    Define the effects of executing an action.
                           Also update the agent.performance slot.
    The environment keeps a list of .things and .agents (which is a subset
    of .things). Each agent has a .performance slot, initialized to 0.
    Each thing has a .location slot, even though some environments may not
    need this."""

    def __init__(self):
        self.things = []
        self.agents = []

    def thing_classes(self):
        return []  # List of classes that can go into environment

    def percept(self, agent):
        '''
            Return the percept that the agent sees at this point.
            (Implement this.)
        '''
        raise NotImplementedError

    def execute_action(self, agent, action):
        "Change the world to reflect this action. (Implement this.)"
        raise NotImplementedError

    def default_location(self, thing):
        "Default location to place a new thing with unspecified location."
        return None

    def exogenous_change(self):
        "If there is spontaneous change in the world, override this."
        pass

    def is_done(self):
        "By default, we're done when we can't find a live agent."
        return not any(agent.is_alive() for agent in self.agents)

    def step(self):
        """Run the environment for one time step. If the
        actions and exogenous changes are independent, this method will
        do.  If there are interactions between them, you'll need to
        override this method."""
        if not self.is_done():
            actions = []
            for agent in self.agents:
                if agent.alive:
                    actions.append(agent.program(self.percept(agent)))
                else:
                    actions.append("")
            for (agent, action) in zip(self.agents, actions):
                self.execute_action(agent, action)
            self.exogenous_change()

    def run(self, steps=1000):
        "Run the Environment for given number of time steps."
        for step in range(steps):
            if self.is_done():
                return
            self.step()
        for thing in self.things:
            thing.performance /= steps

    def list_things_at(self, location, tclass=Thing):
        "Return all things exactly at a given location."
        return [thing for thing in self.things
                if thing.location == location and isinstance(thing, tclass)]

    def some_things_at(self, location, tclass=Thing):
        """Return true if at least one of the things at location
        is an instance of class tclass (or a subclass)."""
        return self.list_things_at(location, tclass) != []

    def add_thing(self, thing, location=None):
        """Add a thing to the environment, setting its location. For
        convenience, if thing is an agent program we make a new agent
        for it. (Shouldn't need to override this."""
        if not isinstance(thing, Thing):
            thing = Agent(thing)
        assert thing not in self.things, "Don't add the same thing twice"
        thing.location = location if location is not None else self.default_location(thing)
        self.things.append(thing)
        if isinstance(thing, Agent):
            thing.performance = 0
            self.agents.append(thing)

    def delete_thing(self, thing):
        """Remove a thing from the environment."""
        try:
            self.things.remove(thing)
        except ValueError as e:
            print(e)
            print("  in Environment delete_thing")
            print("  Thing to be removed: {} at {}" .format(thing, thing.location))
            print("  from list: {}" .format([(thing, thing.location) for thing in self.things]))
        if thing in self.agents:
            self.agents.remove(thing)


class Direction():
    '''A direction class for agents that want to move in a 2D plane
        Usage:
            d = Direction("Down")
            To change directions:
            d = d + "right" or d = d + Direction.R #Both do the same thing
            Note that the argument to __add__ must be a string and not a Direction object.
            Also, it (the argument) can only be right or left. '''

    R = "right"
    L = "left"
    U = "up"
    D = "down"

    def __init__(self, direction):
        self.direction = direction

    def __add__(self, heading):
        if self.direction == self.R:
            return{
                self.R: Direction(self.D),
                self.L: Direction(self.U),
            }.get(heading, None)
        elif self.direction == self.L:
            return{
                self.R: Direction(self.U),
                self.L: Direction(self.L),
            }.get(heading, None)
        elif self.direction == self.U:
            return{
                self.R: Direction(self.R),
                self.L: Direction(self.L),
            }.get(heading, None)
        elif self.direction == self.D:
            return{
                self.R: Direction(self.L),
                self.L: Direction(self.R),
            }.get(heading, None)

    def move_forward(self, from_location):
        x, y = from_location
        if self.direction == self.R:
            return (x + 1, y)
        elif self.direction == self.L:
            return (x - 1, y)
        elif self.direction == self.U:
            return (x, y - 1)
        elif self.direction == self.D:
            return (x, y + 1)


class XYEnvironment(Environment):

    """This class is for environments on a 2D plane, with locations
    labelled by (x, y) points, either discrete or continuous.

    Agents perceive things within a radius.  Each agent in the
    environment has a .location slot which should be a location such
    as (0, 1), and a .holding slot, which should be a list of things
    that are held."""

    def __init__(self, width=10, height=10):
        super(XYEnvironment, self).__init__()

        self.width = width
        self.height = height
        self.observers = []
        # Sets iteration start and end (no walls).
        self.x_start, self.y_start = (0, 0)
        self.x_end, self.y_end = (self.width, self.height)

    perceptible_distance = 1

    def things_near(self, location, radius=None):
        "Return all things within radius of location."
        if radius is None:
            radius = self.perceptible_distance
        radius2 = radius * radius
        return [(thing, radius2 - distance2(location, thing.location)) for thing in self.things
                if distance2(location, thing.location) <= radius2]

    def percept(self, agent):
        '''By default, agent perceives things within a default radius.'''
        return self.things_near(agent.location)

    def execute_action(self, agent, action):
        agent.bump = False
        if action == 'TurnRight':
            agent.direction = agent.direction + Direction.R
        elif action == 'TurnLeft':
            agent.direction = agent.direction + Direction.L
        elif action == 'Forward':
            agent.bump = self.move_to(agent, agent.direction.move_forward(agent.location))
#         elif action == 'Grab':
#             things = [thing for thing in self.list_things_at(agent.location)
#                     if agent.can_grab(thing)]
#             if things:
#                 agent.holding.append(things[0])
        elif action == 'Release':
            if agent.holding:
                agent.holding.pop()

    def default_location(self, thing):
        return (random.choice(self.width), random.choice(self.height))

    def move_to(self, thing, destination):
        '''Move a thing to a new location. Returns True on success or False if there is an Obstacle
            If thing is grabbing anything, they move with him '''
        thing.bump = self.some_things_at(destination, Obstacle)
        if not thing.bump:
            thing.location = destination
            for o in self.observers:
                o.thing_moved(thing)
            for t in thing.holding:
                self.delete_thing(t)
                self.add_thing(t, destination)
                t.location = destination
        return thing.bump

    # def add_thing(self, thing, location=(1, 1)):
    #     super(XYEnvironment, self).add_thing(thing, location)
    #     thing.holding = []
    #     thing.held = None
    #     for obs in self.observers:
    #         obs.thing_added(thing)

    def add_thing(self, thing, location=(1, 1), exclude_duplicate_class_items=False):
        '''Adds things to the world.
            If (exclude_duplicate_class_items) then the item won't be added if the location
            has at least one item of the same class'''
        if (self.is_inbounds(location)):
            if (exclude_duplicate_class_items and
               any(isinstance(t, thing.__class__) for t in self.list_things_at(location))):
                    return
            super(XYEnvironment, self).add_thing(thing, location)

    def is_inbounds(self, location):
        '''Checks to make sure that the location is inbounds (within walls if we have walls)'''
        x, y = location
        return not (x < self.x_start or x >= self.x_end or y < self.y_start or y >= self.y_end)

    def random_location_inbounds(self, exclude=None):
        '''Returns a random location that is inbounds (within walls if we have walls)'''
        location = (random.randint(self.x_start, self.x_end), random.randint(self.y_start, self.y_end))
        if exclude is not None:
            while(location == exclude):
                location = (random.randint(self.x_start, self.x_end), random.randint(self.y_start, self.y_end))
        return location

    def delete_thing(self, thing):
        '''Deletes thing, and everything it is holding (if thing is an agent)'''
        if isinstance(thing, Agent):
            for obj in thing.holding:
                super(XYEnvironment, self).delete_thing(obj)
                for obs in self.observers:
                    obs.thing_deleted(obj)

        super(XYEnvironment, self).delete_thing(thing)
        for obs in self.observers:
            obs.thing_deleted(thing)

    def add_walls(self):
        '''Put walls around the entire perimeter of the grid.'''
        for x in range(self.width):
            self.add_thing(Wall(), (x, 0))
            self.add_thing(Wall(), (x, self.height - 1))
        for y in range(self.height):
            self.add_thing(Wall(), (0, y))
            self.add_thing(Wall(), (self.width - 1, y))

        # Updates iteration start and end (with walls).
        self.x_start, self.y_start = (1, 1)
        self.x_end, self.y_end = (self.width - 1, self.height - 1)

    def add_observer(self, observer):
        """Adds an observer to the list of observers.
        An observer is typically an EnvGUI.

        Each observer is notified of changes in move_to and add_thing,
        by calling the observer's methods thing_moved(thing)
        and thing_added(thing, loc)."""
        self.observers.append(observer)

    def turn_heading(self, heading, inc):
        "Return the heading to the left (inc=+1) or right (inc=-1) of heading."
        return turn_heading(heading, inc)


class Obstacle(Thing):

    """Something that can cause a bump, preventing an agent from
    moving into the same square it's in."""
    pass


class Wall(Obstacle):
    pass


# ______________________________________________________________________________
# Vacuum environment


class Dirt(Thing):
    pass


class VacuumEnvironment(XYEnvironment):

    """The environment of [Ex. 2.12]. Agent perceives dirty or clean,
    and bump (into obstacle) or not; 2D discrete world of unknown size;
    performance measure is 100 for each dirt cleaned, and -1 for
    each turn taken."""

    def __init__(self, width=10, height=10):
        super(VacuumEnvironment, self).__init__(width, height)
        self.add_walls()

    def thing_classes(self):
        return [Wall, Dirt, ReflexVacuumAgent, RandomVacuumAgent,
                TableDrivenVacuumAgent, ModelBasedVacuumAgent]

    def percept(self, agent):
        """The percept is a tuple of ('Dirty' or 'Clean', 'Bump' or 'None').
        Unlike the TrivialVacuumEnvironment, location is NOT perceived."""
        status = ('Dirty' if self.some_things_at(
            agent.location, Dirt) else 'Clean')
        bump = ('Bump' if agent.bump else'None')
        return (status, bump)

    def execute_action(self, agent, action):
        if action == 'Suck':
            dirt_list = self.list_things_at(agent.location, Dirt)
            if dirt_list != []:
                dirt = dirt_list[0]
                agent.performance += 100
                self.delete_thing(dirt)
        else:
            super(VacuumEnvironment, self).execute_action(agent, action)

        if action != 'NoOp':
            agent.performance -= 1


class TrivialVacuumEnvironment(Environment):

    """This environment has two locations, A and B. Each can be Dirty
    or Clean.  The agent perceives its location and the location's
    status. This serves as an example of how to implement a simple
    Environment."""

    def __init__(self, status):
        super(TrivialVacuumEnvironment, self).__init__()
        self.status = status
        '''
        self.status = {loc_A: random.choice(['Clean', 'Dirty']),
                       loc_B: random.choice(['Clean', 'Dirty']),
                       loc_C: random.choice(['Clean', 'Dirty'])}
        '''

    def thing_classes(self):
        return [Wall, Dirt, ReflexVacuumAgent, RandomVacuumAgent,
                TableDrivenVacuumAgent, ModelBasedVacuumAgent]

    def percept(self, agent):
        "Returns the agent's location, and the location status (Dirty/Clean)."
        return (agent.location, self.status[agent.location])

    def execute_action(self, agent, action):
        """Change agent's location and/or location's status; track performance.
        Score 10 for each dirt cleaned; -1 for each move."""
        for loc, status in self.status.items():
            if status == 'Clean':
                agent.performance += 1
        if action == 'Right':
            if agent.location == loc_A:
                agent.location = loc_B
            else:
                agent.location = loc_C
            agent.performance -= 1
        elif action == 'Left':
            if agent.location == loc_C:
                agent.location = loc_B
            else:
                agent.location = loc_A
            agent.performance -= 1
        elif action == 'Suck':
            if self.status[agent.location] == 'Dirty':
                agent.performance += 10
            self.status[agent.location] = 'Clean'

    def default_location(self, thing):
        "Agents start in either location at random."
        return random.choice([loc_A, loc_B, loc_C])
