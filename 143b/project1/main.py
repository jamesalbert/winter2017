#!/usr/bin/env python

'''
143B Project 1 Scheduler.

Usage:
  ./main.py --input=<file>
  ./main.py --input=<file> --debug

Options:
  --input  file to read.
'''

from copy import deepcopy
from docopt import docopt
from yaml import dump, load
import os
import traceback

from exceptions import (
    EndOfSessionException,
    NewSessionWarning
)


class Process(object):
    def __init__(self, pid, priority=1, status_type=None):
        self.pcb = {}
        defaults = {
            **deepcopy(conf['process']),
            **{
                'pid': pid,
                'priority': priority,
                'status_type': status_type
            }
        }
        for attr, default in defaults.items():
            self.pcb[attr] = default
        self.dispatch = {
            'cr': self.create_proc,
            'de': self.destroy_proc,
            'req': self.request_resource,
            'rel': self.release_resource,
            'to': self.timeout,
        }

    def check_validity(self, action, rid, quantity):
        resource = scheduler.resources[rid]
        if action == 'request':
            if self['other'].get(rid, None):
                quantity += self['other'][rid]
            if self['status']['type'] == 'blocked' and \
               rid in self['status']['list']:
                quantity += self['status']
            invalid = not (0 < quantity <= resource['capacity'])
        else:
            invalid = quantity > self['other'].get(rid, -1)
        invalid = invalid and self.pcb['pid'] != 'init'
        if self['pid'] == 'init' or invalid:
            raise IndexError
        return resource

    def check_capacity(self, resource, quantity):
        return resource['available'] >= quantity

    def block_process(self, resource, quantity):
        self['status']['list'].append(resource['rid'])
        scheduler.update(self, 'blocked')
        resource['waiting'].append((self['pid'], quantity))
        return self

    def allocate_resource(self, resource, quantity):
        rid = resource['rid']
        resource['available'] -= quantity
        if resource['available'] is 0:
            resource['status'] = 'allocated'
        self['other'][rid] = quantity + self['other'].get(rid, 0)
        return self

    def deallocate_resource(self, resource, quantity):
        rid = resource['rid']
        resource['available'] += quantity
        del self['other'][rid]
        if resource['available'] > 0:
            resource['status'] = 'free'
        return self

    def handle_waiting(self, resource, quantity):
        rid = resource['rid']
        for pid, quantity in resource['waiting']:
            if resource['available'] - quantity >= 0:
                resource['available'] -= quantity
                proc = scheduler.pid_table[pid]
                proc['status'] = {
                    'type': 'ready',
                    'list': scheduler.procs['ready']
                }
                proc['other'][rid] = quantity
                resource['waiting'].remove((proc['pid'], quantity))
                scheduler.update(proc, 'ready')
        return self

    def request_resource(self, rid, quantity):
        resource = self.check_validity('request', rid, quantity)
        free = self.check_capacity(resource, quantity)
        if free:
            self.allocate_resource(resource, quantity)
        else:
            self.block_process(resource, quantity)
        return self

    def release_resource(self, rid, quantity):
        resource = self.check_validity('release', rid, quantity)
        self.deallocate_resource(resource, quantity)
        self.handle_waiting(resource, quantity)
        return self

    def is_descendant(self, parent, supposed_child):
        children = parent['creation_tree']['child']
        for child in children:
            if child is supposed_child:
                return True
            else:
                is_grandchild = self.is_descendant(child, supposed_child)
                if is_grandchild:
                    return True
        return False

    def destroy_proc(self, pid):
        proc = scheduler.pid_table.get(pid, None)
        if not proc:
            raise IndexError
        if self.is_descendant(proc, self):
            raise IndexError
        children = proc['creation_tree']['child']
        for child in children:
            if child['status']['type']:
                self.destroy_proc(child['pid'])
        for rid, quantity in deepcopy(proc['other']).items():
            proc.release_resource(rid, quantity)
        state = proc['status']['type']
        proc['status']['type'] = None
        scheduler.procs[state].remove(proc)
        del scheduler.pid_table[pid]
        return self

    def create_proc(self, pid, priority):
        if pid in scheduler.pid_table:
            raise IndexError
        if not (0 <= priority <= 2):
            raise IndexError
        if pid != 'init' and priority is 0:
            raise IndexError
        proc = Process(pid, priority=priority)
        self['creation_tree']['child'].append(proc)
        proc['creation_tree']['parent'].append(self)
        scheduler.update(proc, 'ready')
        running = scheduler.get_running_proc()['pid']
        scheduler.pid_table[pid] = proc
        return self

    def timeout(self):
        scheduler.update(self, 'ready')
        return self

    def isnt_blocked(self):
        return self['status']['type'] != 'blocked'

    def __getitem__(self, key):
        return self.pcb[key]

    def __setitem__(self, key, value):
        self.pcb[key] = value
        return value


class Resource(object):
    def __init__(self, rid, status, quantity):
        self.rcb = {
            'rid': rid,
            'status': status,
            'capacity': quantity,
            'available': quantity,
            'waiting': []
        }

    def __getitem__(self, key):
        return self.rcb[key]

    def __setitem__(self, key, value):
        self.rcb[key] = value
        return value


class Scheduler(object):
    def __init__(self, args):
        self.args = args
        self.initialize()

    def initialize(self):
        self.clean_state()
        for resource, quantity in conf['resources'].items():
            self.resources[resource] = Resource(resource, 'free', quantity)
        self.init = Process('init', 0, 'running')
        self.procs['running'].append(self.init)
        self.schedule()
        return self

    def clean_state(self):
        for attr, default in conf['scheduler'].items():
            setattr(self, attr, deepcopy(default))
        return self

    def update(self, proc, state):
        prev = proc['status']['type']
        if prev and proc in self.procs[prev]:
            self.procs[prev].remove(proc)
        proc['status']['type'] = state
        self.procs[state].append(proc)
        return proc

    def get_highest_proc(self, state):
        if not self.procs[state]:
            return None
        return max(self.procs[state],
                   key=lambda x: x['priority'])

    def get_running_proc(self):
        return self.get_highest_proc('running')

    def preempt(self, preemtee, preemter):
        self.update(preemtee, 'running')
        if preemter and preemter.isnt_blocked():
            self.update(preemter, 'ready')

    def log(self, message):
        self.event_log.append(message)

    def schedule(self):
        running = self.get_running_proc()
        ready = self.get_highest_proc('ready')
        if not running:
            self.update(ready, 'running')
        elif ready and \
            (running['priority'] < ready['priority'] or
             running['status']['type'] != 'running'):
            self.preempt(ready, running)
        out = f"{self.get_running_proc()['pid']}"
        self.log(out)

    def write_log(self, newline=True):
        newline = '\n' if newline else str()
        output = ' '.join(self.event_log)
        output_file = open(f"{self.args['--input']}.out", 'a')
        output_file.write(f"{output}{newline}")
        output_file.close()

    def parse_line(self, line):
        if not line:
            self.write_log()
            return
        if line == 'init':
            raise NewSessionWarning
        command, *opts = line.split(' ')
        if command in ('cr', 'req', 'rel'):
            opts[1] = int(opts[1])
        running = self.get_running_proc()
        dispatch = running.dispatch.get(command, None)
        if dispatch:
            dispatch(*opts)
        else:
            raise IndexError
        self.schedule()

    def parse_file(self):
        while lines:
            line = lines.pop(0)
            print(f"parsing {line}")
            try:
                self.parse_line(line)
            except IndexError:
                self.log('error')
                continue
            except NewSessionWarning:
                self.initialize()
        self.write_log(newline=False)

if __name__ == '__main__':
    args = docopt(__doc__)
    try:
        os.remove(f"{args['--input']}.out")
    except FileNotFoundError:
        pass
    with open(args['--input'], 'r') as input_file:
        lines = [l.replace('\n', '')
                 for l in input_file.readlines()]
    with open('config.yaml', 'r') as yaml_file:
        conf = load(yaml_file)
    scheduler = Scheduler(args)
    scheduler.parse_file()
