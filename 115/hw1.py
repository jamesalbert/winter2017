#!/usr/bin/env python

from math import e, factorial
from random import randint
from sys import argv
import simplejson as json
from Queue import Queue
from numpy import arange
from numpy.random import choice


def get_time_interval(total_time):
    return [x * 0.01 for x in range(0, int((total_time+0.01)/0.01))]


def get_unload_time():
    return randint(3.5, 4.5)


def get_poisson_pdf(t, mu):
    return e**(-mu) * mu**t / factorial(t)


'''
def log(time):
    print(conf['train']['incoming'].format(**{'time': time}))
'''


def get_trains():
    '''
    returns the number of trains that will arrive
    within the next hour.
    '''
    probabilities = list()
    for i in range(0, 20):
        probabilities.append(get_poisson_pdf(i, 1))
    return choice(arange(0, 20), p=probabilities)


if __name__ == '__main__':
    '''
    dock = {
        'state': 'ready'
    }
    with open('config.json', 'r') as json_file:
        conf = json.load(json_file)
    for i in get_time_interval(total_time):
        print("%.2f" % i)
    loading_queue = Queue()
    '''
    argv.pop(0)
    avg_arrival_time, total_time = map(float, argv)
    for _ in range(10):
        print(get_trains())
