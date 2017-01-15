

arrival = 0
progress_report = -1
all_done = -2


class Event(object):
    def __init__(self, state, time, next_event_index=None):
        self.state = state
        self.time = time
        self.next = next_event_index

    def set_next(event_index):
        self.next = event_index


class EventManager(object):
    def __init__(self):
        self.events = [Event(0, 0.00)]
        self.first = 0

    def insert(state, time):
        event = Event(state, time)
        self.events.append(event)
        index = len(self.events) - 1
        if self.first == 0 or time < self.events[0].time:
            self.events[index].next = self.first
            self.first = index
        else:
            behind = self.first
            ahead = self.events[self.first].next
            while True:
                if ahead == 0 or time < self.events[ahead].time:
                    break
                behind = ahead
                ahead = self.events[ahead].next
            self.events[behind].next = index
            self.events[index].next = ahead

    def get_next():
        if self.first == 0:
            return
        ret = self.events[self.first]
        self.first = ret.next
        return ret
