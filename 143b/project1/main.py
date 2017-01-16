#!/usr/bin/env python

from copy import deepcopy
from colorama import Fore, init
from json import dumps, loads
from pprint import PrettyPrinter
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from pprint import pformat
from yaml import dump, load
import os
import traceback

from exceptions import (
    EndOfSessionException,
    NewSessionWarning
)


class Process(object):
    def __init__(self, pid, priority=1, status_type='ready'):
        self.pcb = {}
        process_str = dump(conf['process'])
        process_conf = load(process_str % {
            'pid': pid,
            'priority': priority,
            'status_type': status_type
        })
        for attr, default in process_conf.items():
            self.pcb[attr] = default
        self.dispatch = {
            'cr': self.create_proc,
            'de': self.destroy_proc,
            'req': self.request_resource,
            'rel': self.release_resource,
            'to': self.timeout,
        }

    def request_resource(self, rid, quantity):
        if self['pid'] == 'init':
            raise IndexError
        resource = scheduler.resources[rid]
        if resource['capacity'] < quantity:
            raise IndexError  # not enough resource to allocate
        elif resource['available'] < quantity:
            self['status']['list'].append(resource['rid'])
            scheduler.switch_state(self, 'running', 'blocked')
            resource['waiting'].append((self['pid'], quantity))
        else:
            resource['available'] -= quantity
            if resource['available'] is 0:
                resource['status'] = 'allocated'
            self['other'][rid] = quantity
        return conf['request_message'] % {
            'rid': rid,
            'quantity': quantity
        }

    def release_resource(self, rid, quantity=None):
        if self['pid'] == 'init':
            raise IndexError
        resource = scheduler.resources[rid]
        if not self['other'].get(rid, None):
            raise IndexError  # process hasn't requested resource
        quantity = quantity or self['other'][rid]
        print(f"freeing up {quantity}")
        resource['available'] += quantity
        del self['other'][rid]
        if resource['available'] > 0:
            resource['status'] = 'free'
        for waiting in resource['waiting']:
            pid, quantity = waiting
            if resource['available'] - quantity >= 0:
                resource['available'] -= quantity
                proc = scheduler.pid_table[pid]
                print(proc['pid'])
                proc['status'] = {
                    'type': 'ready',
                    'list': scheduler.procs['ready']
                }
                proc['other'][rid] = quantity
                resource['waiting'].remove((proc['pid'], quantity))
                scheduler.switch_state(proc, 'blocked', 'ready')
        print(resource.rcb)
        print(scheduler.resources[rid].rcb)
        return conf['release_message'] % {
            'rid': rid,
            'quantity': quantity
        }

    def destroy_proc(self, pid):
        proc = scheduler.pid_table.get(pid, None)
        if not proc:
            raise Exception('pid {pid} not in pid table')
        child = proc['creation_tree']['child']
        if child:
            self.destroy_proc(child[0]['pid'])
        for rid in list(proc['other']):
            proc.release_resource(rid)
        state = proc['status']['type']
        proc['status']['type'] = None
        scheduler.procs[state].remove(proc)
        return f"process: {pid} was destroyed"

    def create_proc(self, pid, priority):
        proc = Process(pid, priority=priority)
        self['creation_tree']['child'].append(proc)
        proc['creation_tree']['parent'].append(self)
        scheduler.update(proc, 'ready')
        running = scheduler.get_running_proc()['pid']
        response = conf['create_message'] % {
            'pid': pid,
            'running': running,
            'priority': priority
        }
        scheduler.pid_table[pid] = proc
        return response

    def timeout(self):
        scheduler.switch_state(self, 'running', 'ready')
        return f"timeout has been requested"

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
    def __init__(self):
        self.initialize()

    def initialize(self):
        self.clean_state()
        print('creating init process')
        for resource, quantity in conf['resources'].items():
            self.resources[resource] = Resource(resource, 'free', quantity)
        self.init = Process('init', 0, 'running')
        self.procs['running'].append(self.init)
        self.event_log.append('init process has been created')
        self.schedule()
        return self

    def clean_state(self):
        print('clearing settings')
        for attr, default in conf['scheduler'].items():
            print(attr, default)
            setattr(self, attr, deepcopy(default))
        print(self.procs['running'])
        return self

    def save_state(self):
        global lines
        save = conf['save']
        save['lines'] = deepcopy(lines)
        save['line'] = deepcopy(self.line_cache)
        for rid, res in self.resources.items():
            save['resources'][rid] = deepcopy(res)
        for state in self.procs:
            save['processes'][state] = list()
            for proc in self.procs[state]:
                save['processes'][state].append(deepcopy(proc))
                save['pid_table'][proc['pid']] = save['processes'][state][-1]
        self.saves.append(save)

    def load_state(self):
        global lines
        save = self.saves.pop()
        if not self.saves:
            self.saves.append(save)
        lines = deepcopy(save['lines'])
        if len(self.event_log) > 1:
            lines.insert(0, save['line'])
            self.event_log.pop()
        self.resources = dict()
        self.pid_table = dict()
        self.procs = dict()
        for rid, res in save['resources'].items():
            self.resources[rid] = deepcopy(res)
        for state in save['processes']:
            self.procs[state] = list()
            for proc in save['processes'][state]:
                self.procs[state].append(deepcopy(proc))
                self.pid_table[proc['pid']] = self.procs[state][-1]
        return self

    def switch_state(self, proc, state, new_state):
        self.procs[state].remove(proc)
        scheduler.update(proc, new_state)
        return self

    def update(self, proc, state):
        proc['status']['type'] = state
        scheduler.procs[state].append(proc)
        return proc

    def get_highest_proc(self, state):
        if not self.procs[state]:
            return None
        return max(self.procs[state],
                   key=lambda x: x['priority'])

    def get_running_proc(self):
        return self.get_highest_proc('running')

    def preempt(self, preemtee, preemter):
        self.switch_state(preemtee, 'ready', 'running')
        if preemter and preemter['status']['type'] != 'blocked':
            self.switch_state(preemter, 'running', 'ready')

    def pretty_status(self):
        status = dict()
        for rid, res in self.resources.items():
            status[rid] = f"{res['capacity'] - res['available']} allocated, \
                            {res['available']} free"  # res['status']
        for state in self.procs:
            status[state] = dict()
            for proc in self.procs[state]:
                status[state][proc['pid']] = {
                    'status': proc['status']['type'],
                    'other': proc['other'],
                    'priority': proc['priority']
                }
                print(proc['status'])
                if proc['status']['type'] == 'blocked':
                    status[state][proc['pid']]['status'] += \
                        f" by {', '.join(proc['status']['list'])}"
        return status

    def log(self, message):
        output_file = open('output.txt', 'a')
        output_file.write(message)
        output_file.close()

    def say(self, level, message=str()):
        color = {
            'info': Fore.WHITE,
            'error': Fore.RED,
            'warn': Fore.YELLOW
        }[level]
        print(color+str(message))

    def pprint_color(self, obj):
        try:
            json = dumps(obj, indent=4, sort_keys=True)
            print(highlight(json, JsonLexer(), TerminalFormatter()))
        except:
            pp.pprint(obj)
            exit(1)

    def schedule(self):
        running = self.get_running_proc()
        ready = self.get_highest_proc('ready')
        if not running:
            self.switch_state(ready, 'ready', 'running')
        elif ready and \
            (running['priority'] < ready['priority'] or
             running['status']['type'] != 'running'):
            self.preempt(ready, running)
        out = f"{self.get_running_proc()['pid']} "
        self.log(f"{out}")

    def parse_line(self):
        line = self.line_cache
        if not line:
            self.log('\n')
            return 'end of session detected'
        if line == 'init':
            raise NewSessionWarning
        # out = f"{self.get_running_proc()['pid']} "
        # self.log(out)
        command, *opts = line.split(' ')
        if command in ('cr', 'req', 'rel'):
            opts[1] = int(opts[1])
        running = self.get_running_proc()
        dispatch = running.dispatch.get(command, None)
        if dispatch:
            response = dispatch(*opts)
        else:
            response = f"unparsable line: {line}"
        self.schedule()
        return response

    def print_status(self):
        os.system('clear')
        self.say('info', self.event_log[-1])
        self.pprint_color(self.pretty_status())
        self.say('info', f"parsing: {self.line_cache}")

    def parse_file(self):
        self.event_log.append('init process has been created')
        self.save_state()
        while lines:
            self.line_cache = lines.pop(0)
            self.print_status()
            command = input('> ')
            if command == 'b':
                self.load_state()
                continue
            elif command == 'q':
                break
            self.save_state()
            try:
                self.event_log.append(self.parse_line())
            except NewSessionWarning:
                self.initialize()
            except Exception as e:
                self.say('info', conf['loop_error'] % self.__dict__)
                self.say('error')
                traceback.print_tb(e.__traceback__)
                print(f"\n  {e}\n")
                self.say('info', 'reverting back to previous state')
                resp = input('[enter] to revert change, [c] to continue> ')
                if resp == 'c':
                    self.event_log.append('error occurred')
                    self.log('error ')
                    continue
                self.load_state()
                self.load_state()
        self.log('\n')

if __name__ == '__main__':
    init()
    pp = PrettyPrinter(indent=2)
    with open('input.txt', 'r') as input_file:
        lines = [l.replace('\n', '')
                 for l in input_file.readlines()]
    with open('config.yaml', 'r') as yaml_file:
        conf = load(yaml_file)
    scheduler = Scheduler()
    scheduler.parse_file()
