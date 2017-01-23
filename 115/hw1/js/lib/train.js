class Train(object):
    id = 0

    def __init__(self, time):
        self.id = Train.id
        self.unload_time = 0
        self.time = time
        self.next = None
        Train.id += 1
