from heapq import heappush, heappop


assignments = []


# lambda function for extrapolating diagonals
parallel_concat = lambda x, y: [''.join(tup) for tup in zip(x, y)]
# cross product of elements in A and elements in B.
cross = lambda A, B: [a + b for a in A for b in B]

ROWS = 'ABCDEFGHI'
COLS = DIGITS = '123456789'

BOXES = cross(ROWS, COLS)
ROW_UNITS = [cross(r, COLS) for r in ROWS]
COLUMN_UNITS = [cross(ROWS, c) for c in COLS]
SQUARE_UNITS = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]
DIAG_UNITS = [parallel_concat(ROWS, COLS),
              parallel_concat(reversed(ROWS), COLS)]

UNITLIST = ROW_UNITS + COLUMN_UNITS + SQUARE_UNITS + DIAG_UNITS
UNITS = dict((s, [u for u in UNITLIST if s in u]) for s in BOXES)
PEERS = dict((s, set(sum(UNITS[s], []))-set([s])) for s in BOXES)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    pass


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value,
                    then the value will be '123456789'.
    """
    # remove all whitespace, \t and \n inclusive
    grid = grid.join(grid.split())
    # assert length of input is valid
    assert len(grid) == 81, "Sudoku grid is an invalid length"

    # process string into dict
    values = {box: grid[index] if grid[index] in DIGITS else
              DIGITS for index, box in enumerate(BOXES)}

    # for index, box in enumerate(boxes):
    #     updated_value = grid[index] if grid[index] in valid_digits \
    #             else valid_digits
    #     values = assign_value(values, box, updated_value)

    return values


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in BOXES)
    line = '+'.join(['-'*(width*3)]*3)
    for row in ROWS:
        print(''.join(values[row+col].center(width) +
                      ('|' if col in '36' else '') for col in COLS))
        if row in 'CF':
            print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for box, value in values.items():
        if len(value) == 1:
            values = assign_value(values, box, value)
            values = remove_peer_choice(box, values)
    return values


def remove_peer_choice(box, values):
    """Remove values of a box from peers' choices.

    Input: String referring to a box, Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after removal.
    """
    for peer in PEERS[box]:
        if values[box] in values[peer]:
            updated_peer_value = values[peer].replace(values[box], "")
            values = assign_value(values, peer, updated_peer_value)
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in UNITLIST:
        for digit in DIGITS:
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                digit_box = dplaces[0]
                values = assign_value(values, digit_box, digit)
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
    box_space = [box for box in BOXES if len(values[box]) > 1]

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


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
