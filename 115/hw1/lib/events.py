class Event(object):
    def __init__(self,
                 sim=None,
                 event_type=str(),
                 train=None,
                 time=float()):
        self.sim = sim
        self.type = event_type
        self.train = train
        self.time = time

    def callback(self):
        raise NotImplementedError


class EnterQueue(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)

    def callback(self):
        self.sim.queue.insert(self.train)
        if not self.sim.dock_in_use:
            self.sim.events.schedule('exit-queue',
                                     train=self.train,
                                     time=self.time)


class ExitQueue(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)

    def callback(self):
        train = self.sim.queue.pop()
        self.sim.events.schedule('start-service',
                                 train=train,
                                 time=self.time)


class StartService(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)

    def callback(self):
        self.sim.dock_in_use = self.train
        self.sim.events.schedule('end-service',
                                 train=self.train,
                                 time=self.time + self.train.unload_time)


class EndService(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)

    def callback(self):
        self.sim.dock_in_use = None
        if self.sim.queue:
            self.sim.events.schedule('exit-queue',
                                     train=self.sim.queue[0],
                                     time=self.time)
