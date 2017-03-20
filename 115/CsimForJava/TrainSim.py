#!/usr/bin/env python
""" generated source for module TrainSimulator """
#  Al Gore Invented The Internet
from com.mesquite.csim import *
from com.mesquite.csim import Process
from com.mesquite.csim.file import Files
import java.io

class TrainSimulator(Model):
    """ generated source for class TrainSimulator """
    simTime = float()
    mu = float()
    dockbusy = float()
    dockhogged = float()
    dockidle = 0

    @classmethod
    def main(cls, args):
        """ generated source for method main """
        cls.simTime = Double.parseDouble(args[0]) if args.length >= 1 else 7200
        cls.mu = Double.parseDouble(args[1]) if args.length >= 2 else 10
        model = TrainSimulator()
        model.enableTrace(True)
        model.run()
        model.report()
        dockbusyperc = (cls.dockbusy / cls.simTime) * 100
        dockhoggedperc = (cls.dockhogged / cls.simTime) * 100
        dockidleperc = (cls.dockidle / cls.simTime) * 100
        docktimeperc = dockbusyperc + dockhoggedperc + dockidleperc
        DockMessage = String.format("Time Dock was Busy: %1$f%%\n" + "Time Dock was Hogged: %2$f%%\n" + "Time Dock was Idle: %3$f%%\n" + "With a total of %4$f%%", dockbusyperc, dockhoggedperc, dockidleperc, docktimeperc)
        print DockMessage

    def __init__(self):
        """ generated source for method __init__ """
        super(TrainSimulator, self).__init__("TrainSimulator")

    def run(self):
        """ generated source for method run """
        start(Sim())

    class Sim(Process):
        """ generated source for class Sim """
        def __init__(self):
            """ generated source for method __init__ """
            super(Sim, self).__init__("Sim")

        def run(self):
            """ generated source for method run """
            rand.setSeed(10)
            self.dock = FCFSFacility("Dock", 1)
            self.NotInUse = Event("NotInUse")
            self.NotIdle = Event("NotIdle")
            self.Idle = Event("Idle")
            add(IdleChecker())
            self.Idle.set()
            add(TrainGenerator())
            hold(self.simTime)

    class TrainGenerator(Process):
        """ generated source for class TrainGenerator """
        def __init__(self):
            """ generated source for method __init__ """
            super(TrainGenerator, self).__init__("TrainGenerator")
            self.TimeInQueue = Table("Time in Queue")
            self.TimeInSystem = Table("Time in System")
            self.TimeDockBusy = Table("Time Dock was Busy")
            self.TimeDockHogged = Table("Time Dock was Hogged")
            self.TimeDockIdle = Table("Time Dock was Idle")
            self.TimeInSystem.confidence()
            self.TimeInQueue.setPermanent(True)
            self.TimeDockBusy.setPermanent(True)
            self.TimeDockHogged.setPermanent(True)
            self.TimeDockIdle.setPermanent(True)
            self.TimeInSystem.setPermanent(True)
            self.TrainsInQueue = QTable("Number of Trains in Queue")
            self.TrainsInQueue.setPermanent(True)
            self.HoggedOutTrains = Table("Hogged Out Trains")
            self.HoggedOutTrains.add_histogram(5, 0, 5)

        def run(self):
            """ generated source for method run """
            self.NotInUse.set()
            while True:
                add(Train())
                hold(rand.exponential(self.mu))

    class Train(Process):
        """ generated source for class Train """
        hogout = Event("Hogout")
        hogin = Event("Hogin")
        crew = Crew(hogout, hogin)
        hogouts = 0

        def __init__(self):
            """ generated source for method __init__ """
            super(Train, self).__init__("Train")

        def run(self):
            """ generated source for method run """
            arrived_in_system = float()
            arrived_in_queue = float()
            departed_from_system = float()
            departed_from_queue = float()
            service_time = float()
            time_left = float()
            start = float()
            end = float()
            time_in_system = float()
            time_in_queue = float()
            next_hogout = float()
            arrived_in_system = clock()
            new_crew()
            arrived_in_queue = clock()
            self.TrainsInQueue.note_entry()
            while not self.NotInUse.timed_queue(self.crew.get_next_hogout()):
                self.hogouts += 1
                self.hogin.untimed_wait()
                new_crew()
            self.TrainsInQueue.note_exit()
            self.NotIdle.set()
            departed_from_queue = clock()
            time_in_queue = departed_from_queue - arrived_in_queue
            done = Event("End Service")
            self.TimeInQueue.record(time_in_queue)
            self.dock.reserve()
            service_time = rand.uniform(3.5, 4.5)
            time_left = service_time
            next_hogout = crew.get_next_hogout()
            while time_left > next_hogout:
                hold(next_hogout)
                self.TimeDockBusy.record(next_hogout)
                self.dockbusy += next_hogout
                start = clock()
                self.hogout.untimed_wait()
                self.hogouts += 1
                self.hogin.untimed_wait()
                new_crew()
                end = clock()
                self.TimeDockHogged.record(end - start)
                self.dockhogged += end - start
                time_left -= next_hogout
                next_hogout = crew.get_next_hogout()
            hold(time_left)
            self.TimeDockBusy.record(time_left)
            self.dockbusy += time_left
            self.dock.release()
            self.NotInUse.set()
            departed_from_system = clock()
            time_in_system = departed_from_system - arrived_in_system
            self.TimeInSystem.record(time_in_system)
            self.HoggedOutTrains.record(self.hogouts)
            self.Idle.set()

        def new_crew(self):
            """ generated source for method new_crew """
            self.crew = Crew(hogout, hogin)
            add(self.crew)
            hold(0)

    class Crew(Process):
        """ generated source for class Crew """
        hogout = Event()
        hogin = Event()
        time = float()
        start = float()

        def __init__(self, ho, hi):
            """ generated source for method __init__ """
            super(Crew, self).__init__("Crew")
            self.hogout = ho
            self.hogin = hi
            self.start = clock()

        def run(self):
            """ generated source for method run """
            self.time = rand.uniform(6, 11)
            hold(self.time)
            self.hogout.set()
            hold(rand.uniform(2.5, 3.5))
            self.hogin.set()

        def get_next_hogout(self):
            """ generated source for method get_next_hogout """
            return (self.start + self.time) - clock()

    class IdleChecker(Process):
        """ generated source for class IdleChecker """
        start = float()
        end = float()

        def __init__(self):
            """ generated source for method __init__ """
            super(IdleChecker, self).__init__("Idle Checker")

        def run(self):
            """ generated source for method run """
            while True:
                self.Idle.untimed_wait()
                self.start = clock()
                self.NotIdle.untimed_wait()
                self.end = clock()
                self.TimeDockIdle.record(self.end - self.start)
                self.dockidle += end - start


if __name__ == '__main__':
    import sys
    TrainSimulator.main(sys.argv)
