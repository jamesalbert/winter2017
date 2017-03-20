"""
Station example.

Covers:

- Waiting for other processes
- Resources: Resource

Scenario:

"""
import random

import simpy


RANDOM_SEED = 42


class Station(object):
    def __init__(self, env):
        self.env = env
        self.dock = simpy.Resource(env, 1)

    def service(self, train, time):
        yield self.env.timeout(time)
        print("Dock serviced train %s at %.2f" % (train, self.env.now))


def hogout(env, name):
    def func():
        remaining_time = random.uniform(6, 11)
        yield env.timeout(remaining_time)
        print("%s hogged out at %.2f" % (name, env.now))
    return env.process(func())


def train(env, name, station):
    def run():
        try:
            print('%s arrives at the service queue at %.2f.' % (name, env.now))
            # yield env.process(hogout(env, name))
            with station.dock.request() as request:
                yield request

                '''
                if request not in res:
                    print("%s hogged out at %.2f" % (name, env.now))
                    yield env.timeout(random.uniform(2.5, 3.5))
                    print("%s's new crew has arrived at %.2f" % (name, env.now))
                '''

                print('%s enters the service station at %.2f.' % (name, env.now))
                proc = env.process(station.service(name, ))
                yield proc

                print('%s leaves the service station at %.2f.' % (name, env.now))
        except simpy.Interrupt:
            print("%s hogged out at %.2f" % (name, env.now))
            if request.triggered and proc:
                proc.interrupt()
            yield env.timeout(random.uniform(2.5, 3.5))
            print("%s's new crew has arrived at %.2f" % (name, env.now))
    proc = env.process(run())
    res = yield proc | env.timeout(random.uniform(6, 11))
    if proc not in res:
        proc.interrupt()


class setup(object):
    def __init__(self, env):
        self.service = Station(env)

    def run(self, mean=.1):
        i = -1
        trains = list()
        while True:
            yield env.timeout(random.expovariate(mean))
            i += 1
            t = env.process(train(env, 'Train %d' % i, self.service))




# Setup and start the simulation
print('Station')
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
sim = setup(env)
env.process(sim.run())

# Execute!
env.run(until=50)
