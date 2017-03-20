#!/usr/bin/env python

"""Project 3

Usage:
  main.py --vminput=<vminput> --vainput=<vainput> --tlb=<enabled/disabled>

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

from math import floor

import numpy as np
from docopt import docopt


class PageFault(Exception):
    def __init__(self):
        self.message = 'pf'


class Error(Exception):
    def __init__(self):
        self.message = 'err'


def group(l, span=2):
    # deal with it
    return [list(map(int, map(lambda x:
                              x.strip(), l[i:i + span])))
            for i in range(0, len(l), span)
            if l[i].strip()]


def dec2bin(integer):
    return format(integer, '#034b').replace('0b', str())


class Memory(object):
    def __init__(self, tlb_enabled):
        self.pm = np.array([[0] * 512] * 1024, np.int32)
        self.bitmap = [0] * 1024
        self.bitmap[0] = 1
        self.tlb_enabled = True if tlb_enabled == 'enabled' else False
        self.tlb = np.array([[0] * 3] * 4, np.int32)

    def add(self, addrs, offsets):
        for addr in addrs:
            self.allocate(*map(int, addr))
        for offset in offsets:
            self.assign(*map(int, offset))

    def allocate(self, s, f):
        cb = self.parse_addr(f)
        self.pm[0][s] = f
        self.bitmap[f / 512] = 1
        self.bitmap[(f / 512) + 1] = 1

    def assign(self, p, s, f):
        pt = self.pm[0][s] / 512
        self.pm[pt + (1 if p >= 512 else 0)][p % 512] = f
        self.bitmap[f / 512] = 1

    def find(self, length=1):
        for i, bit in enumerate(self.bitmap):
            if not (bit or self.bitmap[i + (length - 1)]):
                return i

    def update_tlb(self, flag):
        for entry in self.tlb:
            if entry[0] > flag:
                entry[0] -= 1

    def lookup(self, cb):
        if self.tlb_enabled and int(cb['addr'], 2) > 0:
            for entry in self.tlb:
                if entry[1] == int(cb['addr'][0:19], 2):
                    self.update_tlb(entry[0])
                    entry[0] = 3
                    return ('h ' if self.tlb_enabled else '') + \
                        str(entry[2] + cb['w'])
        pt = self.pm[0][cb['s']]
        if pt < 0:
            raise PageFault
        pt /= 512
        page = self.pm[pt + (1 if cb['p'] >= 512 else 0)][cb['p'] % 512]
        if page < 0:
            raise PageFault
        if cb['write']:
            if pt == 0:
                f = self.find(length=2)
                self.allocate(cb['s'], f * 512)
                return self.lookup(cb)
            if page == 0:
                f = self.find()
                self.assign(cb['p'], cb['s'], f * 512)
                return self.lookup(cb)
        else:
            if 0 in [pt, page]:
                raise Error
        for entry in self.tlb:
            if entry[0] == 0:
                entry[0] = 3
                entry[1] = int(cb['addr'][0:19], 2)
                entry[2] = page + cb['w']
                self.update_tlb(0)
                break
        return ('m ' if self.tlb_enabled else '') + str(page + cb['w'])

    def parse_addr(self, integer):
        addr = dec2bin(integer)[4:]
        s = int(addr[0:9], 2)
        p = int(addr[9:19], 2)
        w = int(addr[19:28], 2)
        return {
            'addr': addr,
            's': s,
            'p': p,
            'w': w,
        }

    def translate(self, integer, write):
        cb = self.parse_addr(integer)
        cb['write'] = write
        return self.lookup(cb)

    def eval(self, instructions):
        output = list()
        for inst in instructions:
            write, integer = inst
            out = str()
            try:
                out = mem.translate(integer, write)
            except (PageFault, Error) as e:
                out = ('m ' if self.tlb_enabled else '') + e.message
            output.append(out)
        return ' '.join(output)


if __name__ == '__main__':
    args = docopt(__doc__, version='v0.1')
    addrs = list()
    offsets = list()
    instructions = list()
    mem = Memory(args['--tlb'])
    with open(args['--vminput'], 'r') as vmfile:
        addrs_line, offsets_line = vmfile.readlines()
        addrs = group(addrs_line.split(' '))
        offsets = group(offsets_line.split(' '), span=3)
    mem.add(addrs, offsets)
    with open(args['--vainput'], 'r') as vafile:
        content = [x for x in vafile.read().split(' ') if x]
        instructions = group(content)
    print(mem.eval(instructions))
