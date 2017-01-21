from .events import (
    EnterQueue,
    ExitQueue,
    StartService,
    EndService
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
            'end-service': EndService
        }

    def schedule(self, event_type, **kwargs):
        kwargs.update({
            'event_type': event_type,
            'sim': self.sim
        })
        event = self.dispatch[event_type](**kwargs)
        self.insert(event)
        self.sort()

    def sort(self):
        self.values = sorted(self.values,
                             key=lambda x: x.time)

    def is_empty(self):
        return len(self) is 0
