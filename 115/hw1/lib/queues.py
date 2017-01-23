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

    def sort(self):
        print("sorting")
        self.values = sorted(self.values,
                             key=lambda x: x.time)
        for event in self.values[1:]:
            index = self.values.index(event)
            event.dt = event.time - self.values[index - 1].time

    def is_empty(self):
        return len(self) is 0


class Trains(FIFOQueue):
    def __init__(self, sim):
        FIFOQueue.__init__(self)
        self.sim = sim

    def delay(self, hogged_train):
        delay_time = hogged_train.crew.until_arrival
        for event in self.sim.events:
            event.time += delay_time
        '''
        index = 0
        if hogged_train in self.values:
            index = self.values.index(hogged_train)
        elif hogged_train is self.sim.dock_in_use:
            self.sim.dock_in_use.unload_time += delay_time
            index = 0
        for train in self.values[index:]:
            train.unload_time += hogged_train.crew.until_arrival
        '''
