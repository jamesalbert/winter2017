from random import expovariate
from .queues import Events, FIFOQueue
from .train import Train
from .config import conf


class Simulator(object):
    def __init__(self):
        self.dock_in_use = None
        self.events = Events(self)
        self.time = 0
        self.queue = FIFOQueue()

    def start(self):
        while self.time <= 7200:
            self.events.schedule('enter-queue',
                                 train=Train(self.time),
                                 time=self.time)
            self.time += expovariate(.1)
        while self.events:
            event = self.events.pop()
            event.callback()
            print(conf[event.type].format(**event.__dict__))
