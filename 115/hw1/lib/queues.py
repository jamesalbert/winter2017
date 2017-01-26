from .events import (
    EnterQueue,
    ExitQueue,
    StartService,
    EndService,
    Depart,
    Arrive,
    Hogout,
    Hogin
)


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
    def __init__(self, sim):
        FIFOQueue.__init__(self)
        self.sim = sim
        self.dispatch = {
            'enter-queue': EnterQueue,
            'exit-queue': ExitQueue,
            'start-service': StartService,
            'end-service': EndService,
            'hogout': Hogout,
            'hogin': Hogin,
            'departure': Depart,
            'arrival': Arrive
        }

    def schedule(self, event_type, **kwargs):
        kwargs.update({
            'event_type': event_type,
            'sim': self.sim
        })
        event = self.dispatch[event_type](**kwargs)
        self.insert(event)
        self.sort()
        self.sim.num_events += 1

    def remove(self, train=None, event_type=None):
        if not (train or event_type):
            return
        to_remove = None
        for event in self.values:
            if event.train is train and \
               event.type == event_type:
                to_remove = event
                break
        if not to_remove:
            return
        self.values.remove(to_remove)

    def chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def apply_dt(self, events):
        '''
        Applies the delta time to each event

        Uses a divide-and-conquer method to break up
        the list of events, and calculates the difference
        in time between the start to two sequentially ordered
        events.
        '''
        if len(events) is 2:
            events[1].dt = events[1].time - events[0].time
            return events
        elif len(events) < 2:
            return events
        length = len(events)
        left = self.apply_dt(events[0:length // 2])
        right = self.apply_dt(events[length // 2:length])
        right[0].dt = right[0].time - left[-1].time
        return left + right

    def sort(self):
        self.values = sorted(self.values,
                             key=lambda x: x.time)
        self.values = self.apply_dt(self.values)

    def is_empty(self):
        return len(self) is 0


class Trains(FIFOQueue):
    def __init__(self, sim):
        FIFOQueue.__init__(self)
        self.sim = sim

    def delay(self, hogged_train):
        delay_time = hogged_train.crew.until_arrival
        for event in self.sim.events.values:
            event.time += delay_time
