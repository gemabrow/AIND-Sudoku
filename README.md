# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

[1]: ./images/naked-twins.png
[2]: ./images/naked-twins-2.png

With this project, we provide a method for solving sudokus utilizing the
naked twin strategy and include the additional constraints required by
diagonal sudoku puzzles. Our approach regards sudoku puzzles
as an instance of a Constraint Propagation Problem (CSP) and .

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
constraint for a given unit -- as it applies to the naked twins strategy -- is
such that, for any pair of boxes within a unit whose range are both identical
and have a cardinality of 2, the possible values for the naked twins are
eliminated from all other boxes the naked twins are unit members of.

Naked Twins: Pre-Constraint Propagation | Post-Constraint Propagation 
----- | -------
![Naked Twins: Pre-Constraint Propagation][1] | ![Post-Constraint Propagation][2]

Our solution first iterates over all boxes within the puzzle. Any boxes
with only two possible values are then added to a `viable_twins` list. After
all boxes have been examined meeting the constraint of having only two possible
values, we then examine each primary box within the list of `viable_twins` 
against a seconday box pulled from its "peers" (boxes belonging to units of
which the primary box is also a member) using set equality. These matches
are appended to a list `actual_twins`.

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


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

From the provided environment, run
'python solution_test.py'

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

