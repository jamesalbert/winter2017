from sys import argv


def read_output(filename):
    response = dict()
    with open(filename, 'r') as outfile:
        lines = outfile.readlines()
        response['inputs'] = len(lines)
        response['width'] = len(lines[0].split(' '))
        response['output'] = map(
            lambda x: x.strip(), ' '.join(lines).split(' '))
    return response


if __name__ == '__main__':
    argv.pop(0)
    bodies = dict()
    for filename in argv:
        bodies[filename] = read_output(filename)
    output = (bodies[argv[0]]['output'],
              bodies[argv[1]]['output'])
    line = 0
    column = int()
    error = False
    wrong = int()
    for i, (yours, mine) in enumerate(zip(*output)):
        column = i % bodies[argv[0]]['width']
        if column == 0:
            line += 1
        if yours != mine:
            error = True
            wrong += 1
            print('failed: {0} != {1}, line {2} column {3}'.format(
                yours, mine, line, column + 1))
    if not error:
        print('passed')
    print('You are {0:.2f}% similar to the compared output'.format(
        float(len(output[0]) - wrong) / float(len(output[0])) * 100))
