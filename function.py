# -*- coding: utf-8 -*-
"""
   Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from heapq import heappush, heappop
from utils import *
from utils import boxes, peers, row_units, unitlist


def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """

    # remove all whitespace, \t and \n inclusive
    grid = grid.join(grid.split())
    # assert length of input is valid
    assert len(grid) == 81, "Sudoku grid is an invalid length"

    # process string into dict
    # initialize all boxes to empty, represented as '.'
    values = {box: '123456789' for box in boxes}

    for i, row in enumerate(row_units):
        for box in row:
            assert box[1].isdigit()
            character_index = int(box[1]) + 9*i - 1
            if grid[character_index].isdigit():
                values[box] = grid[character_index]

    return values


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for box, box_values in values.items():
        if len(box_values) == 1:
            values = remove_peer_choice(box, values)
    return values


def remove_peer_choice(box, values):
    """Remove values of a box from peers' choices.

    Input: String referring to a box, Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after removal.
    """
    for peer in peers[box]:
        if values[box] in values[peer]:
            values[peer] = values[peer].replace(values[box], "")
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Using depth-first search and propagation, create a search tree and
    solve the sudoku.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:  # failed sanity check
        return False

    # Choose one of the unfilled squares with the fewest possibilities
    heap = []
    box_space = [box for box in boxes if len(values[box]) > 1]

    if not box_space:
        return values
    for box in box_space:
        heappush(heap, (len(values[box]), box))

    # Now use recursion to solve each one of the resulting sudokus,
    # and if one returns a value (not False), return that answer!
    _, temp_box = heappop(heap)
    for value in values[temp_box]:
        temp_sudoku = values.copy()
        temp_sudoku[temp_box] = value
        attempt = search(temp_sudoku)
        if attempt:
            return attempt

    return
