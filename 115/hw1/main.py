#!/usr/bin/env python

from lib import *
from sys import argv


if __name__ == '__main__':
    argv.pop(0)
    Simulator(*argv)\
        .start()\
        .analyze()
