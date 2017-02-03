from ete3 import Tree, TextFace, TreeStyle, add_face_to_node
from wand.image import Image
import glob
import os
import re


INITIAL_STATE = [3, 3, 1]
GOAL_STATE = [0, 0, 0]


def is_safe(state):
    if state[0] is 0 or state[0] >= state[1]:
        return True
    return False


def apply_action(action, values):
    state = list()
    boat = values[-1]
    for a, v in zip(action, values):
        result = v - a if boat else v + a
        if 0 <= result <= 3:
            state.append(result)
        else:
            state = None
            break
    if state:
        other_side = [3 - state[0], 3 - state[1], int(not state[2])]
        safe = is_safe(state) and is_safe(other_side)
        return state if safe else None


def create_nodes(node):
    state = node.name
    found = False
    for action in actions:
        result = apply_action(action, state)
        if result and result != INITIAL_STATE and \
           seen.count(result) <= 3:
            if result == GOAL_STATE:
                found = True
            seen.append(result)
            child = node.add_child(name=result)
    return node.children


def layout_fn(node):
    face = TextFace(node.name, fsize=25)
    add_face_to_node(face, node, column=0, position="branch-right")


def numerical_sort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

if __name__ == '__main__':
    numbers = re.compile(r'(\d+)')
    actions = [[1, 0, 1],
               [2, 0, 1],
               [0, 1, 1],
               [0, 2, 1],
               [1, 1, 1]]
    seen = [INITIAL_STATE]
    ts = TreeStyle()
    ts.show_leaf_name = False
    ts.layout_fn = layout_fn
    root = Tree(name=INITIAL_STATE)
    children = create_nodes(root)
    root.render("3.1.a.png", w=1500, h=200, tree_style=ts)
    image = 2
    while children:
        next_gen = list()
        for child in children:
            next_gen.extend(create_nodes(child))
        children = next_gen[:]
        root.render("3.%d.a.png" % image, w=1500, h=200, tree_style=ts)
        image += 1
        if GOAL_STATE in [x.name for x in children]:
            break
    with Image() as wand:
        images = sorted(glob.glob('*.png'), key=numerical_sort)
        for image in images:
            vimage = Image(filename=image)
            wand.sequence.append(vimage)
            if image is not images[-1]:
                os.remove(image)
            else:
                os.rename(image, '3.9.a.png')
        for cursor in range(len(images)):
            with wand.sequence[cursor] as frame:
                if cursor == len(images) - 1:
                    frame.delay = 500
                    continue
                frame.delay = 100
        wand.type = 'optimize'
        wand.save(filename='3.9.b.gif')
