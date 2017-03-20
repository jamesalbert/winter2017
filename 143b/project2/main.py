from sys import argv
from copy import deepcopy


def compute_avg(times):
    avg = round(sum(times) / len(times), 2)
    times.insert(0, avg)


def order_times(timestable):
    times = list()
    while timestable:
        m = str(min(map(int, timestable.keys())))
        times.append(timestable[m])
        del timestable[m]
    return times


def FIFO(procs, time=int(), times=list()):
    while procs:
        pid = min(procs, key=lambda x: int(x))
        if time < procs[pid]['arrival']:
            time += 1
            continue
        time += procs[pid]['service']
        times.append(time - procs[pid]['arrival'])
        del procs[pid]
    compute_avg(times)
    return times


def SJF(procs, time=int(), timestable=dict(), times=list()):
    while procs:
        pid = min(procs, key=lambda x: procs[x]['service']
                  if procs[x]['arrival'] <= time else 10000)
        if time < procs[pid]['arrival']:
            time += 1
            continue
        time += procs[pid]['service']
        timestable[pid] = time - procs[pid]['arrival']
        del procs[pid]
    times = order_times(timestable)
    compute_avg(times)
    return times


def SRT(procs, time=int(), timestable=dict(), times=list()):
    while procs:
        pid = min(procs, key=lambda x: procs[x]['service']
                  if procs[x]['arrival'] <= time else 10000)
        if time < procs[pid]['arrival']:
            time += 1
            continue
        time += 1
        procs[pid]['service'] -= 1
        if not procs[pid]['service']:
            timestable[pid] = time - procs[pid]['arrival']
            del procs[pid]
    times = order_times(timestable)
    compute_avg(times)
    return times


def MLF(procs, time=int(), timestable=dict(), times=list()):
    while procs:
        pid = max(procs, key=lambda x: procs[x]['priority']
                  if procs[x]['arrival'] <= time else -1)
        time += 1
        if time - 1 < procs[pid]['arrival']:
            continue
        procs[pid]['service'] -= 1
        procs[pid]['before_shift'] -= 1
        if not procs[pid]['service']:
            timestable[pid] = time - procs[pid]['arrival']
            del procs[pid]
        elif not procs[pid]['before_shift']:
            if procs[pid]['priority'] > 1:
                procs[pid]['priority'] -= 1
                procs[pid]['allowed'] *= 2
            procs[pid]['before_shift'] = procs[pid]['allowed']
    times = order_times(timestable)
    compute_avg(times)
    return times


if __name__ == '__main__':
    argv.pop(0)
    filename = argv.pop(0)
    dispatch = {
        'FIFO': FIFO,
        'SJF': SJF,
        'SRT': SRT,
        'MLF': MLF
    }
    with open(filename, 'r') as inputfile:
        timestr = inputfile.read().split(' ')
        procs = dict()
        for pid, i in enumerate(range(0, len(timestr), 2)):
            procs[str(pid)] = {
                'arrival': int(timestr[i]),
                'service': int(timestr[i + 1].strip()),
                'priority': 5,
                'allowed': 1,
                'before_shift': 1
            }
        for name, func in dispatch.items():
            res = func(deepcopy(procs))
            print(" ".join(map(str, res)))
