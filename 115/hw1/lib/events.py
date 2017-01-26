from random import uniform


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
        self.dt = int()

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
        time = self.time + self.train.unload_time
        duration = self.train.unload_time
        self.sim.keep_track('busy', self.train, duration)
        self.sim.events.schedule('end-service',
                                 train=self.train,
                                 time=time)


class EndService(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)

    def callback(self):
        self.sim.events.remove(train=self.train,
                               event_type='hogout')
        self.sim.events.schedule('departure',
                                 train=self.train,
                                 time=self.time)
        if self.sim.queue:
            self.sim.events.schedule('exit-queue',
                                     train=self.sim.queue[0],
                                     time=self.time)
        self.sim.dock_in_use = None


class Hogout(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)

    def callback(self):
        # add time it takes for new crew to arrival to all trains
        time = self.time + self.train.crew.until_arrival
        duration = self.train.crew.until_arrival
        self.sim.keep_track('hogged_out', self.train, duration)
        self.train.crew.request_crew()
        self.sim.queue.delay(self.train)
        self.sim.events.schedule('hogout',
                                 train=self.train,
                                 time=self.time + self.train.crew.hours_left)
        self.sim.events.schedule('hogin',
                                 train=self.train,
                                 time=time)


class Hogin(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)

    def callback(self):
        self.train.crew.request_crew()
        self.sim.queue.delay(self.train)


class Arrive(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)

    def callback(self):
        self.sim.stats['trains_in_system'][self.train.id] = self.time
        self.train.unload_time = uniform(3.5, 4.5)
        self.sim.events.schedule('hogout',
                                 train=self.train,
                                 time=self.time + self.train.crew.hours_left)
        self.sim.events.schedule('enter-queue',
                                 train=self.train,
                                 time=self.time)


class Depart(Event):
    def __init__(self, **kwargs):
        Event.__init__(self, **kwargs)

    def callback(self):
        start = self.sim.stats['trains_in_system'][self.train.id]
        self.sim.stats['trains_in_system'][self.train.id] = self.time - start
        self.sim.stats['trains_served'] += 1
        # gather statistics
        pass
