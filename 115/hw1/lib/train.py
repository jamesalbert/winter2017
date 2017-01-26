from .crew import Crew


class Train(object):
    id = 0

    def __init__(self, time):
        self.id = str(Train.id)
        self.crew = Crew()
        self.unload_time = 0
        self.time = time
        self.next = None
        Train.id += 1
