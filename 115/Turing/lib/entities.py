

num_pumps = raw_input("number of pumps> ")
avail_pumps = 1


class Car(object):
    def __init__(self, time, litres, next_car):
        self.time = time
        self.litres = litres
        self.next_car = next_car


class Pump(object):
    def __init__(self):
        self.services = list()

    def add(self, time, next_pump, car):
        self.services.append({
            'time': time,
            'next_pump': next_pump,
            'car': car
        })
        return self
