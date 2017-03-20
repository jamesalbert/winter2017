from json import dumps, loads

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import NullFormatter


class Regression(object):
    def __init__(self, domain):
        self.domain = domain

    def expo(self):
        return 32666.80339 * np.exp(0.104535465 * self.domain)

    def lin(self):
        return np.array(list(map(
            lambda x: 4287.601038 + 7739.953563 * x,
            self.domain)), np.int32)

    def poly(self):
        return np.array(list(map(
            lambda x: (374.580138 * (x ** 2)) +
            (13279.17888 * x) - 9624.294681,
            self.domain)), np.int32)


if __name__ == '__main__':
    # gather data from main table
    domain = list()
    range_ = list()
    states = dict()
    with open('datasets/table.json', 'r') as tablefile:
        json = loads(tablefile.read())
    for state, data in json.items():
        states[state] = data['x']
        domain.append(data['x'])
        range_.append(data['y'])

    # run simulation 100 times
    occurances = dict()
    probabilities = dict()
    mu_xbar = list()
    for x in sorted(domain):
        occurances[x] = domain.count(x)
        probabilities[x] = occurances[x] / len(domain)
    for i in range(100):
        sim_occurances = np.random.multinomial(
            n=43, pvals=list(probabilities.values()))
        sim_domain = list()
        for var, occ in zip(sorted(set(domain)), sim_occurances):
            sim_domain.extend([var] * occ)
        mu_xbar.append(sum(sim_domain) / len(sim_domain))

    # plot simulation
    plt.scatter(domain, range_, s=2,
                c='red', label='sample')
    plt.scatter(sim_domain, range_, s=2,
                c='blue', label='simulated')
    plt.title('enrollees with pre-existing conditions over insurers')
    plt.ylabel('number of enrollees')
    plt.xlabel('number of insurers')
    plt.legend(handles=[
        patches.Patch(color='red', label='sample data'),
        patches.Patch(color='blue', label='simulated data')
    ])
    plt.show()

    # show simulation animation
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)
    sam = plt.scatter([domain[0]], [range_[0]], s=2,
                      c='red', label='sample')
    sim = plt.scatter([sim_domain[0]], [range_[0]], s=2,
                      c='blue', label='simulated')

    def update(i):
        sam = plt.scatter(domain[:i], range_[:i], s=2,
                          c='red', label='sample')
        sim = plt.scatter(sim_domain[:i], range_[:i], s=2,
                          c='blue', label='simulated')
        return sam, sim
    anim = FuncAnimation(fig, update, frames=np.arange(1, 42), interval=200)
    plt.title('enrollees with pre-existing conditions over insurers')
    plt.ylabel('number of enrollees')
    plt.xlabel('number of insurers')
    plt.legend(handles=[
        patches.Patch(color='red', label='sample data'),
        patches.Patch(color='blue', label='simulated data')
    ])
    # plt.show()
    anim.save('simulation.mp4', fps=5, extra_args=['-vcodec', 'libx264'])
    print('simulation.mp4 was created, run `open simulation.mp4`')

    # plot regression curves
    del sim
    plt.title('enrollees with pre-existing conditions over insurers')
    plt.ylabel('number of enrollees')
    plt.xlabel('number of insurers')
    plt.scatter(domain, range_, s=2, c='red')
    reg_domain = np.arange(0.0, 17.0, 0.01)
    reg = Regression(reg_domain)
    plt.plot(reg_domain, reg.lin(), c='green')
    plt.plot(reg_domain, reg.expo(), c='cyan')
    plt.plot(reg_domain, reg.poly(), c='purple')
    plt.legend(handles=[
        patches.Patch(color='green', label='linear regression'),
        patches.Patch(color='cyan', label='exponential regression'),
        patches.Patch(color='purple', label='polynomail regression')
    ])
    plt.show()

    # plot health and income rates
    def read_dataset(topic):
        '''
        read one of the json dataset files
        topic (string) - name of file minus extension
        '''
        domain = list()
        range_ = list()
        with open('datasets/{0}.json'.format(topic), mode='r') as infile:
            reader = loads(infile.read())
            for state, data in reader.items():
                if not states.get(state):
                    continue
                domain.append(states[state])
                range_.append(data)
        return domain, range_

    cdomain, crange = read_dataset('cancer')
    ddomain, drange = read_dataset('diabetes')
    hdomain, hrange = read_dataset('heart')
    idomain, irange = read_dataset('income')

    plt.subplot(221)
    plt.scatter(idomain, irange, s=2)
    plt.ylabel('income')
    plt.xlabel('insurers')
    plt.subplot(222)
    plt.scatter(cdomain, crange, c='red', s=2)
    plt.ylabel('cancer')
    plt.xlabel('insurers')
    plt.subplot(223)
    plt.scatter(hdomain, hrange, c='purple', s=2)
    plt.ylabel('heart disease')
    plt.xlabel('insurers')
    plt.subplot(224)
    plt.scatter(ddomain, drange, c='green', s=2)
    plt.ylabel('diabetes')
    plt.xlabel('insurers')
    plt.gca().yaxis.set_minor_formatter(NullFormatter())
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10,
                        right=0.95, hspace=0.25, wspace=0.35)
    plt.show()
