# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

[1]: ./images/naked-twins.png
[2]: ./images/naked-twins-2.png

With this project, we provide a method for solving sudokus utilizing the
naked twin strategy and include the additional constraints required by
diagonal sudoku puzzles. Our approach regards sudoku puzzles
as an instance of a Constraint Propagation Problem (CSP) and approaches them
as such.

Utilizing constraint propagation requires that we state the constraint(s) 
followed by reducing the search space by identifying the range of values 
that are still valid for a given domain.

In our case, our domain is all of the boxes within the Sudoku puzzle, and
the range for each box is the set of digits from one to nine, inclusive, that
are valid for that space. 

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  

A: We begin by examining each unit, where a unit is
a 3x3 square, a row, or a column of boxes in the sudoku puzzle. The local 
constraint for a given unit &mdash; as it applies to the naked twins strategy
&mdash; is such that, for any pair of boxes within a unit whose range are both
identical and have a cardinality of 2, the possible values for the naked twins
are eliminated from all other boxes the naked twins are unit members of.

Pre-Constraint Propagation | Post-Constraint Propagation 
----- | -------
![NT: Pre-Constraint Propagation][1] | ![NT: Post-Constraint Propagation][2]

Our solution first iterates over all boxes within the puzzle. Any boxes
with only two possible values are then added to the `viable_twins` list. After
all boxes have been examined meeting the constraint of having only two possible
values, we then examine each primary box within the list of `viable_twins` 
against a seconday box pulled from its "peers" (boxes belonging to units of
which the primary box is also a member) using set equality. These matches
are appended to the `actual_twins` list.

For each pair of boxes within `actual_twins`, we form a set representing the
shared values of the twins `twin_vals`, and create a superset `joint_peers`
from the union of the peers of each twin. For each peer within `joint_peers`,
we then update the values of each peer such that no digit within `twin_vals`
is present in the range of values for any peer of either twin.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  

A: Constraint propagation of the diagonal sudoku problem is as trivial as 
adding two new units to the previously mentioned unit list of squares, columns,
and rows. The two diagonal units are defined utilizing a lambda
function, as in the following code snippet:

```python
parallel_concat = lambda x, y: [''.join(tup) for tup in zip(x, y)]

ROWS = 'ABCDEFGHI'
COLS = DIGITS = '123456789'

DIAGONAL_UNITS = [parallel_concat(ROWS, COLS),
                  parallel_concat(reversed(ROWS), COLS)]

UNITLIST = ROW_UNITS + COLUMN_UNITS + SQUARE_UNITS + DIAGONAL_UNITS
```

The constraints previously applied to all units within the unit list are then
applied to the diagonal units, as well. This includes, but is not limited to,
the previously mentioned naked twins strategy.

### Install

This project requires **Python 3**.

It is recommended to install [Anaconda](https://www.continuum.io/downloads), a
pre-packaged Python distribution that contains all of the necessary libraries
and software for this project. Please try using the environment provided in the
Anaconda lesson of Udacity's AI Nanodegree.

From the provided environment, run
```
python solution_test.py
```

If you'd like to see a visualization, download 
Pygame [here](http://www.pygame.org/download.shtml), then run
```
python solution.py
```
