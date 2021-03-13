
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

def get_diagonal_units():
    diagonal_units = []
    diagonal_unit_a = []
    diagonal_unit_b = []
    col = 1
    for row in rows:
        diagonal_unit_a.append(row + str(col))
        col = col + 1

    col = 9
    for row in rows:
        diagonal_unit = row + str(col)
        diagonal_unit_b.append(row + str(col))
        col = col - 1

    diagonal_units.append(diagonal_unit_a)    
    diagonal_units.append(diagonal_unit_b)    

    return diagonal_units

diagonal_units = get_diagonal_units()
unitlist = row_units + column_units + square_units + diagonal_units

units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def get_intersection_peers(peers_box_a, peers_peer_box_value):
    intersection_peers = []
    for peer_box_a in peers_box_a:
        for peer_peer_box_value in peers_peer_box_value:
            if peer_box_a == peer_peer_box_value:
                intersection_peers.append(peer_box_a)

    return intersection_peers                

def clone_dic(source_dict, cloned_dict):
    for key in source_dict:
        cloned_dict[key] = source_dict[key]
    return cloned_dict

def naked_twins(values):
    values_pairs_elimated = {}
    values_pairs_elimated = clone_dic(values, values_pairs_elimated)

    for box_a in values_pairs_elimated:
        peer_boxes = peers[box_a]
        for peer_box in peer_boxes:
            box_a_value = values_pairs_elimated[box_a]
            peer_box_value = values_pairs_elimated[peer_box]
            if box_a_value == peer_box_value and len(box_a_value) == 2:
                intersection_peers = get_intersection_peers(peers[box_a], peers[peer_box])
                for intersection_peer in intersection_peers:
                    for digit_value in values_pairs_elimated[box_a]:
                        intersection_peer_value = values_pairs_elimated[intersection_peer]
                        intersection_peer_values_digits = ''
                        for intersection_peer_value_digit in intersection_peer_value:
                            if intersection_peer_value_digit != digit_value:
                                intersection_peer_values_digits = intersection_peer_values_digits + intersection_peer_value_digit
                        values_pairs_elimated[intersection_peer] = intersection_peer_values_digits                        

    return values_pairs_elimated

def eliminate(values):
    values_cleaned = {}
    values_cleaned = clone_dic(values, values_cleaned)

    solved_values = []
    for key in values_cleaned:
        value = values_cleaned[key]
        if len(value) == 1:
            solved_values.append(key)

    for solved_key in solved_values:
        solved_digit = values_cleaned[solved_key]
        for peer in  peers[solved_key]:
            values_cleaned[peer] = values_cleaned[peer].replace(solved_digit, '')

    return values_cleaned

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values    

def only_choice(values):
    values_only_choice = {}
    
    values_only_choice = {}
    clone_dic(values, values_only_choice)
    
    for i in range(len(unitlist)):
        unit_keys = unitlist[i]        
        for key in unit_keys:
            value = values[key]
            all_values = ''
            for key_comp in unit_keys:
                value_comp = values[key_comp]
                if key_comp != key:
                    all_values = all_values + value_comp

                all_values_no_repeat = ''
                for c in all_values:
                    if c not in all_values_no_repeat:
                        all_values_no_repeat = all_values_no_repeat + c
            
            for c in value:
                if c not in all_values_no_repeat:
                    values_only_choice[key] = c

    return values_only_choice

def reduce_puzzle(values):
    no_progress = False
    while not no_progress:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        no_progress = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
            
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False

    values = naked_twins(values)

    multi_value_found = False
    for key in values:
        value =  values[key]
        if len(value) > 1:
            multi_value_found = True

    if multi_value_found == False:
        return values

    min_len = 10
    for key in values:
        value = values[key]
        value_len = len(value)
        if value_len > 1:
            if min_len > value_len:
                min_len = value_len

        first_search_key = ''
        for key in values:
            value = values[key]
            if len(value) == min_len:
                first_search_key = key

    selected_value = values[first_search_key]
    for value in selected_value:
        new_sudoku = {}
        new_sudoku = clone_dic(values, new_sudoku)
        new_sudoku[first_search_key] = value
        trial_solution = search(new_sudoku)
        if trial_solution:
            return trial_solution

def solve(grid):
    values = grid2values(grid)
    values = search(values)
    return values

if __name__ == "__main__":
    diag_sudoku_grid = '...7.9....85...31.2......7...........1..7.6......8...7.7.........3......85.......'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)
        
    #validate(result)


    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
