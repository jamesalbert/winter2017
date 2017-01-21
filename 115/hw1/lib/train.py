from random import uniform


class Train(object):
    id = 0

    def __init__(self, time):
        self.id = Train.id
        self.unload_time = uniform(3.5, 4.5)
        self.time = time
        self.next = None
        Train.id += 1
