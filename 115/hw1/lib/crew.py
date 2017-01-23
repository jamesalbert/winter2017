from random import uniform


class Crew(object):
    def __init__(self):
        self.hours_left = 0
        self.request_crew()
        self.until_arrival = 0

    def request_crew(self):
        self.hours_left = uniform(6, 11)
        self.until_arrival = uniform(2.5, 3.5)
