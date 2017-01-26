import matplotlib.pyplot as plt
import numpy as np
from random import expovariate, seed
from .queues import Events, Trains
from .train import Train
from .config import conf, schema


class Simulator(object):
    event_shift = 0

    def __init__(self, mu, limit, verbose=True):
        self.dock_in_use = None
        self.events = Events(self)
        self.num_events = int()
        self.time = int()
        self.mu = float(mu)
        self.limit = int(limit)
        self.verbose = verbose
        self.queue = Trains(self)
        self.hogged_out = dict()
        self.stats = schema['stats']

    def start(self):
        while self.time <= self.limit:
            self.events.schedule('arrival',
                                 train=Train(self.time),
                                 time=self.time)
            self.time += expovariate(1.0 / self.mu)
        while self.events:
            event = self.events.pop()
            event.callback()
            if self.verbose:
                print(conf[event.type].format(**event.__dict__))
            self.gather_statistics(event)
            Simulator.event_shift += 1
            if not self.events:
                self.stats['final_time'] = event.time
        return self

    def keep_track(self, state, train, duration, always=False):
        if state == 'hogged_out':
            if train.id not in self.hogged_out:
                self.hogged_out[train.id] = 1
            else:
                self.hogged_out[train.id] += 1
        if state == 'queue':
            if train.id in self.stats[state]:
                start = self.stats[state][train.id]
                self.stats[state][train.id] = duration - start
            else:
                self.stats[state][train.id] = duration
            return
        if always or train is self.dock_in_use:
            self.stats[state] += duration

    def gather_statistics(self, event):
        # busy, idle, and hogged out stats
        if event.type == 'start-service':
            # service started, keep track of how long
            self.stats['start_service'] = event.time
        elif event.type == 'end-service':
            # service ended, add time dock was busy
            self.stats['end_service'] = event.time
        elif event.type == 'hogout' and event.train is self.dock_in_use:
            # service was ended due to hogged out crew
            # stop tracking service time and add the time
            # it was busy for
            self.stats['end_service'] = event.time
        elif event.type == 'hogin' and event.train is self.dock_in_use:
            # service started again due to hogin
            # start tracking service time again
            self.stats['start_service'] = event.time
        end_service = self.stats['end_service']
        start_service = self.stats['start_service']
        if end_service >= start_service and \
           event.time - event.dt > end_service:
            self.stats['idle'] += event.dt

        # find queue max
        trains_in_queue = len(self.queue)
        max_queue = self.stats['max_queue']
        self.stats['max_queue'] = max(trains_in_queue, max_queue)

    def plot_histogram(self):
        '''histogram'''
        occurances = list(self.hogged_out.values())
        plt.hist(occurances)
        plt.xlabel("sequential hogouts")
        plt.ylabel("number of trains")
        plt.title("Hogging Out Frequences")
        plt.show()

    def get_queue_stats(self):
        '''queue statistics'''
        times_in_queue = self.stats['queue'].values()
        total_time_in_queue = sum(times_in_queue)
        number_of_time_in_queue = len(times_in_queue)
        self.stats['avg_queue'] = total_time_in_queue / number_of_time_in_queue
        for dock_state in ('idle', 'busy', 'hogged_out'):
            self.stats[dock_state] /= self.stats['final_time']
            self.stats[dock_state] *= 100

    def get_system_stats(self):
        '''system statistics'''
        avg_time = float()
        self.stats['max_time'] = max(
            self.stats['trains'].values()
        )
        for _, time in self.stats['trains'].items():
            avg_time += time
        avg_time /= len(self.stats['trains'])
        self.stats['avg_time'] = avg_time

    def get_stats(self):
        self.get_system_stats()
        self.get_queue_stats()

    def print_stats(self):
        print(conf['stats'].format(**self.stats))

    def analyze(self):
        self.get_stats()
        self.print_stats()
        self.plot_histogram()
