import matplotlib.pyplot as plt
import numpy as np
from random import expovariate, seed
from .queues import Events, Trains
from .train import Train
from .config import conf


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
        self.stats = {
            'trains_served': int(),
            'indv_train_count': list(),
            'trains_in_system': dict(),
            'start_service_time': float(),
            'end_service_time': float(),
            'start_hogout_time': float(),
            'max_time_in_system': int(),
            'time_in_system': float(),
            'avg_time_in_queue': float(),
            'max_trains_in_queue': int(),
            'times_in_queue': dict(),
            'busy': float(),
            'idle': float(),
            'hogged_out': float(),
            'final_time': float()
        }

    def start(self):
        # seed(15)
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

    def keep_track(self, state, train, duration):
        if state == 'hogged_out':
            if train.id not in self.hogged_out:
                self.hogged_out[train.id] = 1
            else:
                self.hogged_out[train.id] += 1
        if train is self.dock_in_use:
            self.stats[state] += duration

    def gather_statistics(self, event):
        ''' A big mess :(

        let's break it down...
                            ___                                          ___
         __________________/  /                       __________________/  /
        | _    _______    /  /                       | _    _______    /  /
        |(_) .d########b.//)| _____________________ |(_) .d########b.//)|
        |  .d############//  ||        _____        ||  .d############//  |
        | .d######""####//b. ||() ||  [JAMES]  || ()|| .d######""####//b. |
        | 9######(  )#_//##P ||()|__|  | = |  |__|()|| 9######(  )#_//##P |
        | 'b######++#/_/##d' ||() ||   | = |   || ()|| 'b######++#/_/##d' |
        |  "9############P"  ||   ||   |___|   ||   ||  "9############P"  |
        |  _"9a#######aP"    ||  _   _____..__   _  ||  _"9a#######aP"    |
        | |_|  `""""''       || (_) |_____||__| (_) || |_|  `""""''       |
        |  ___..___________  ||_____________________||  ___..___________  |
        | |___||___________| |                       | |___||___________| |
        |____________________|                       |____________________|
        '''

        '''
        this part gathers percentages of time in dock as:
            - busy
            - idle
            - hogged out
        '''
        if event.type == 'start-service':
            # service started, keep track of how long
            self.stats['start_service_time'] = event.time
        elif event.type == 'end-service':
            # service ended, add time dock was busy
            self.stats['end_service_time'] = event.time
        elif event.type == 'hogout' and event.train is self.dock_in_use:
            # service was ended due to hogged out crew
            # stop tracking service time and add the time
            # it was busy for
            self.stats['end_service_time'] = event.time
        elif event.type == 'hogin' and event.train is self.dock_in_use:
            # service started again due to hogin
            # start tracking service time again
            self.stats['start_service_time'] = event.time
        end_service_time = self.stats['end_service_time']
        start_service_time = self.stats['start_service_time']
        if end_service_time >= start_service_time and \
           event.time - event.dt > end_service_time:
            self.stats['idle'] += event.dt

        '''
        Gathering max statistics is easy. For each event,
        check if the amount of trains in system/queue is
        greater than anything we've seen yet in the sim.
        '''
        trains_in_queue = len(self.queue)
        max_trains_in_queue = self.stats['max_trains_in_queue']
        self.stats['max_trains_in_queue'] = max(trains_in_queue,
                                                max_trains_in_queue)

        if event.type == 'enter-queue':
            self.stats['times_in_queue'][str(event.train.id)] = event.time
        elif event.type == 'exit-queue':
            time_entered = self.stats['times_in_queue'][str(event.train.id)]
            time_spent = event.time - time_entered
            self.stats['times_in_queue'][str(event.train.id)] = time_spent

    def plot_histogram(self):
        '''histogram'''
        occurances = list(self.hogged_out.values())
        plt.hist(occurances)
        plt.xlabel("sequential hogouts")
        plt.ylabel("number of trains")
        plt.title("Hogging Out Frequences")
        plt.show()

    def analyze(self):
        '''system statistics'''
        time_in_system = float()
        self.stats['max_time_in_system'] = max(
            self.stats['trains_in_system'].values()
        )
        for _, stats in self.stats['trains_in_system'].items():
            time_in_system += stats
        time_in_system /= len(self.stats['trains_in_system'].keys())
        self.stats['time_in_system'] = time_in_system

        '''queue statistics'''
        times_in_queue = self.stats['times_in_queue'].values()
        total_time_in_queue = sum(times_in_queue)
        number_of_time_in_queue = len(times_in_queue)
        self.stats['avg_time_in_queue'] = total_time_in_queue / number_of_time_in_queue
        for dock_state in ('idle', 'busy', 'hogged_out'):
            self.stats[dock_state] /= self.stats['final_time']
            self.stats[dock_state] *= 100
        print(conf['stats'].format(**self.stats))
        self.plot_histogram()
