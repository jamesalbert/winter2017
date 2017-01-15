#!/usr/bin/env python

import scipy.integrate as integrate
from math import e, log
from random import randint, random, seed


def exponential(x, r):
    return integrate.quad(lambda t: r * e**(-r*t), 0, x)


def inverted_cdf():
    ret = list()
    x = 0
    interval = 10
    while True:
        y = exponential(x, 10)
        # print y[0]
        if y[0] > interval:
            break
        x += 1
        interval -= y[0]
        ret.append(-.1 * log(y[0]))
    return ret


def get_interarrival_time():
    seed(3)
    return -.1 * log(random())

if __name__ == '__main__':
    # Fxi = inverted_cdf()
    # print Fxi[0]
    for i in range(10):
        print get_interarrival_time()
