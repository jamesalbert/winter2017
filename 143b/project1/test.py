from glob import glob
import os


for filename in glob('inputs/project1_test/input*.txt'):
    os.system(f"python main.py --input={filename}")

for testname in glob('inputs/project1_test/output*'):
    filename = testname.replace('output', 'input') + '.out'
    test = open(testname, 'r').read().strip()
    mine = open(filename, 'r').read().strip()
    try:
        assert test == mine, f"{testname} and {filename} do not match"
    except AssertionError as e:
        print(e)
