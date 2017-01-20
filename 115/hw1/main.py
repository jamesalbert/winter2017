#!/usr/bin/env python

from math import log
from random import expovariate, uniform
from yaml import load


class Train(object):
    id = 0

    def __init__(self):
        self.start_wait_time = 0
        self.id = Train.id
        self.unload_time = uniform(3.5, 4.5)
        self.time = Simulator.time
        self.next = None
        Train.id += 1


class Event(object):
    def __init__(self, event_type=None, train=None, time=None):
        self.type = event_type
        self.train = train
        self.time = time

    def callback(self):
        pass


class EnterQueue(Event):
    def __init__(self, name, train, time):
        super().__init__(name, train, time)

    def callback(self):
        Simulator.queue.insert(self.train)
        if not Simulator.dock_in_use:
            Simulator.events.schedule('exit-queue',
                                      train=self.train,
                                      time=self.time)


class ExitQueue(Event):
    def __init__(self, name, train, time):
        super().__init__(name, train, time)

    def callback(self):
        train = Simulator.queue.pop()
        Simulator.events.schedule('start-service',
                                  train=train,
                                  time=self.time)


class StartService(Event):
    def __init__(self, name, train, time):
        super().__init__(name, train, time)

    def callback(self):
        Simulator.dock_in_use = self.train
        Simulator.events.schedule('end-service',
                                  train=self.train,
                                  time=self.time + self.train.unload_time)


class EndService(Event):
    def __init__(self, name, train, time):
        super().__init__(name, train, time)

    def callback(self):
        Simulator.dock_in_use = None
        if Simulator.queue:
            Simulator.events.schedule('exit-queue',
                                      train=Simulator.queue[0],
                                      time=self.time)


class Events(object):
    def __init__(self):
        self.events = []
        self.current = 0
        self.dispatch = {
            'enter-queue': EnterQueue,
            'exit-queue': ExitQueue,
            'start-service': StartService,
            'end-service': EndService
        }

    def schedule(self, name, **kwargs):
        event = self.dispatch[name](**{**{'name': name}, **kwargs})
        self.events.append(event)
        self.sort()
        #  event.callback()

    def pop(self):
        return self.events.pop(0)

    def sort(self):
        self.events = sorted(self.events, key=lambda x: x.time)

    def __bool__(self):
        return bool(self.events)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current + 1 > len(self.events):
            raise StopIteration
        else:
            self.current += 1
            return self.events[self.current - 1]


class FIFOQueue(object):
    def __init__(self, values=[]):
        self.values = values

    def insert(self, value):
        self.values.append(value)

    def pop(self, value=None, index=0):
        if value:
            self.values.remove(value)
            return value
        return self.values.pop(index)

    def is_empty(self):
        return len(self) is 1

    def __bool__(self):
        return bool(self.values)

    def __getitem__(self, index):
        if index < len(self.values):
            return self.values[index]
        return None

    def __len__(self):
        return len(self.values)


class Simulator(object):
    time = 0
    dock_in_use = None
    events = Events()
    queue = FIFOQueue()

    def __init__(self):
        self.state = dict()

    def start(self):
        while Simulator.time <= 7200:
            train = Train()
            self.events.schedule('enter-queue',
                                 train=train,
                                 time=Simulator.time)
            Simulator.time += expovariate(.1)
        while Simulator.events:
            event = Simulator.events.pop()
            event.callback()
            print(conf[event.type].format(**event.__dict__))


if __name__ == '__main__':
    with open('config.yaml', 'r') as yaml_file:
        conf = load(yaml_file)
    Simulator().start()