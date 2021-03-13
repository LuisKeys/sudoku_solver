
from collections import defaultdict


rows = 'ABCDEFGHI'
cols = '123456789'
boxes = [r + c for r in rows for c in cols]
history = {}  # history must be declared here so that it exists in the assign_values scope

def extract_units(unitlist, boxes):
    units = defaultdict(list)
    for current_box in boxes:
        for unit in unitlist:
            if current_box in unit:
                units[current_box].append(unit)
    return units

def extract_peers(units, boxes):
    peers = defaultdict(set)
    for key_box in boxes:
        for unit in units[key_box]:
            for peer_box in unit:
                if peer_box != key_box:
                    peers[key_box].add(peer_box)
    return peers

def assign_value(values, box, value):
    if values[box] == value:
        return values

    prev = values2grid(values)
    values[box] = value
    if len(value) == 1:
        history[values2grid(values)] = (prev, (box, value))
    return values

def cross(A, B):
    return [x+y for x in A for y in B]

def values2grid(values):
    res = []
    for r in rows:
        for c in cols:
            v = values[r + c]
            res.append(v if len(v) == 1 else '.')
    return ''.join(res)

def grid2values(grid):
    sudoku_grid = {}
    for val, key in zip(grid, boxes):
        if val == '.':
            sudoku_grid[key] = '123456789'
        else:
            sudoku_grid[key] = val
    return sudoku_grid

def display(values):
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print()

def validate(values):
    col_counter = 1
    row_total = 0
    total = 0
    for key in values:
        total = total + int(values[key])
        col_counter = col_counter + 1
        if col_counter == 10:
            col_counter = 1
            if total != 45:
                print('Row:' + key[0])
                print(total)
            total = 0

    for col in cols:
        for row in rows:
            key = row + col
            total = total + int(values[key])

        if total != 45:
            print('Col:' + col)
            print(total)
        total = 0

def reconstruct(values, history):
    path = []
    prev = values2grid(values)
    while prev in history:
        prev, step = history[prev]
        path.append(step)
    return path[::-1]
