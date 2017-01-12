#!/usr/bin/env python


class Process(object):
    def __init__(self, pid, priority=1):
        self.pcb = {
            'pid': pid,
            'memory': {},
            'other': {},
            'status': {
                'type': None,
                'list': []
            },
            'creation_tree': {
                'parent': None,
                'child': None
            },
            'priority': priority
        }
        self.dispatch = {
            'cr': self.create_proc,
            'de': self.destroy_proc,
            'req': self.request_resource,
            'rel': self.release_resource,
            'to': self.timeout,
            'init': self.deinit
        }

    def request_resource(self, rid, quantity):
        resource = scheduler.resources[rid]
        if resource['status'] == 'free':
            resource['status'] = 'allocated'
            self.pcb['other'][rid] = resource
        else:
            self.pcb['status'] = {
                'type': 'blocked',
                'list': r
            }
            scheduler.procs['running'].remove(self)
            resource['waiting'].append(self.pcb)
        return f"resource: {quantity} units of {name} has been requested"

    def release_resource(self, name, quantity):
        resource = scheduler.resources[rid]
        del self['other'][rid]
        if not resource['waiting']:
            resource['status'] = 'free'
        else:
            proc = resource['waiting'].pop(0)
            proc['status'] = {
                'type': 'ready',
                'list': scheduler.procs['running']
            }
            scheduler.procs['running'].append(proc)
        return f"resource: {quantity} units of {name} has been released"

    def destroy_proc(self, name):
        if name in scheduler.procs['running']:
            del scheduler.procs['running'][name]
        return f"process: {name} was destroyed"

    def create_proc(self, name, priority):
        scheduler.procs[name] = self.new_pcb(name, priority=priority)
        return f"process: {name} was created with priority {priority}"

    def schedule(self):
        proc = max(scheduler.procs['ready'],
                   key=lambda x: x['priority'])
        if self.pcb['priority'] < proc.pcb['priority'] or \
           self.pcb['status']['type'] != 'running' or \
           self is None:
            preempt(proc, self)


class Resource(object):
    def __init__(self, rid, status, quantity):
        self.rcb = {
            'status': status,
            'quantity': quantity,
            'waiting': []
        }


class Scheduler(object):
    def __init__(self, input_file):
        self.procs = {
            'ready': [],
            'running': [],
            'blocked': []
        }
        self.resources = {}
        self.input_file = input_file

    def init(self):
        return self

    def deinit(self):
        self.destroy_proc('init')
        return "init process has been destroyed"

    def timeout(self):
        return f"timeout has been requested"

    def new_rcb(self, rid, status='free', waiting=[]):
        self.resources[rid] = {
            'status': status,
            'waiting': waiting
        }
        return self

    def parse_line(self, line):
        try:
            if not line or line == '...':
                return str()
            command = line.split(' ')
            return self.dispatch[command.pop(0)](*command)
        except KeyError as e:
            return f"error: '{command}' from '{line}' not found"

    def parse_file(self):
        with open(self.input_file, 'r') as input_file:
            lines = [l.replace('\n', '') for l in input_file.readlines()]
        for line in lines:
            print(self.parse_line(line))

if __name__ == '__main__':
    scheduler = Scheduler('input.txt')
    # scheduler.parse_file()
