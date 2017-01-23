from random import expovariate
from .queues import Events, Trains
from .train import Train
from .config import conf


class Simulator(object):
    event_shift = 0

    def __init__(self):
        self.dock_in_use = None
        self.events = Events(self)
        self.time = 0
        self.queue = Trains(self)
        self.stats = {
            'trains_served': int(),
            'indv_train_count': list(),
            'trains_in_system_detail': str(),
            'start_service_time': float(),
            'end_service_time': float(),
            'start_hogout_time': float(),
            'avg_trains_in_system': int(),
            'max_trains_in_system': int(),
            'avg_time_in_queue': float(),
            'max_time_in_queue': float(),
            'busy': float(),
            'idle': float(),
            'hogged_out': float(),
            'final_time': float()
        }

    def start(self):
        while self.time <= 7200:
            self.events.schedule('arrival',
                                 train=Train(self.time),
                                 time=self.time)
            self.time += expovariate(.1)
        previous_event = self.events.pop()
        sorted_events = [previous_event]
        while self.events:
            event = self.events.pop()
            sorted_events.append(event)
            event.callback()
            print(conf[event.type].format(**event.__dict__))
            self.gather_statistics(event, previous_event)
            previous_event = event
            Simulator.event_shift += 1
            if not self.events:
                self.stats['final_time'] = event.time
        return self

    def gather_statistics(self, event, previous_event):
        if event.type == 'start-service':
            self.stats['start_service_time'] = event.time
        elif event.type == 'end-service':
            self.stats['end_service_time'] = event.time
            self.stats['busy'] += event.time - self.stats['start_service_time']
        elif event.type == 'hogout' and event.train is self.dock_in_use:
            self.stats['end_service_time'] = event.time
            self.stats['start_hogout_time'] = event.time
            self.stats['busy'] += event.time - self.stats['start_service_time']
        elif event.type == 'hogin' and event.train is self.dock_in_use:
            self.stats['start_service_time'] = event.time
            self.stats['hogged_out'] += event.time - self.stats['start_hogout_time']
        end_service_time = self.stats['end_service_time']
        start_service_time = self.stats['start_service_time']
        if end_service_time >= start_service_time and \
           previous_event.time > end_service_time:
            self.stats['idle'] += event.dt
        trains_in_system = len(self.queue)
        trains_in_system += 1 if self.dock_in_use else 0
        self.stats['indv_train_count'].append(trains_in_system)
        max_trains_in_system = self.stats['max_trains_in_system']
        self.stats['max_trains_in_system'] = max(trains_in_system,
                                                 max_trains_in_system)
        self.stats['avg_trains_in_system'] *= Simulator.event_shift
        self.stats['avg_trains_in_system'] += trains_in_system
        self.stats['avg_trains_in_system'] /= Simulator.event_shift + 1

    def analyze(self):
        detail = str()
        for count in set(self.stats['indv_train_count']):
            detail += 'There were ' + str(count) + ' trains in the system '
            detail += str(self.stats['indv_train_count'].count(count))
            detail += ' times out of all events\n'
        self.stats['trains_in_system_detail'] = detail
        for dock_state in ('idle', 'busy', 'hogged_out'):
            self.stats[dock_state] /= self.stats['final_time']
            self.stats[dock_state] *= 100
        print(conf['stats'].format(**self.stats))
