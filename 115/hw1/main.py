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
        raise NotImplementedError


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


class FIFOQueue(object):
    def __init__(self):
        self.values = list()
        self.current = 0

    def insert(self, value):
        self.values.append(value)

    def pop(self, value=None, index=0):
        if value:
            self.values.remove(value)
            return value
        return self.values.pop(index)

    def sort(self):
        pass

    def is_empty(self):
        return len(self) is 1

    def __bool__(self):
        return bool(self.values)

    def __getitem__(self, index):
        if index < len(self.values):
            return self.values[index]
        return None

    def __iter__(self):
        return self

    def __next__(self):
        if self.current + 1 > len(self.values):
            raise StopIteration
        else:
            self.current += 1
            return self.values[self.current - 1]

    def __len__(self):
        return len(self.values)


class Events(FIFOQueue):
    def __init__(self):
        super().__init__()
        self.dispatch = {
            'enter-queue': EnterQueue,
            'exit-queue': ExitQueue,
            'start-service': StartService,
            'end-service': EndService
        }

    def schedule(self, name, **kwargs):
        event = self.dispatch[name](**{**{'name': name}, **kwargs})
        self.insert(event)
        self.sort()

    def sort(self):
        self.values = sorted(self.values,
                             key=lambda x: x.time)

    def is_empty(self):
        return len(self) is 0


class Simulator(object):
    time = 0
    dock_in_use = None
    events = Events()
    queue = FIFOQueue()

    def start(self):
        while Simulator.time <= 7200:
            Simulator.events.schedule('enter-queue',
                                      train=Train(),
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
