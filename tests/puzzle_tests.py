from nose.tools import *
from sudoku import puzzle
import pickle

with open("sample", 'rb') as f:
    p = pickle.load(f)

with open("sample_solved", 'rb') as f:
    p_solved = pickle.load(f)

with open("sample_inconsistent", 'rb') as f:
    p_inconsistent = pickle.load(f)
def test_empty():
    assert_equal(p.get_empty_cells(),
        [(0, 0), (0, 5), (0, 6), (0, 8), (1, 1), (1, 3), (1, 4), (1, 5),
         (1, 7), (2, 0), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (3, 0),
         (3, 1), (3, 2), (3, 3), (3, 7), (3, 8), (4, 0), (4, 1), (4, 3),
         (4, 5), (4, 6), (5, 0), (5, 1), (5, 2), (5, 4), (5, 6), (6, 2),
         (6, 5), (6, 6), (6, 7), (6, 8), (7, 0), (7, 4), (7, 6), (7, 7),
         (7, 8), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]
)



def test_rows():
    assert puzzle.is_consistent(p.get_row_vals(0))
    assert puzzle.is_consistent(p.get_row_vals(4))
    assert puzzle.is_consistent(p.get_row_vals(7))

def test_cols():
    assert puzzle.is_consistent(p.get_col_vals(1))
    assert puzzle.is_consistent(p.get_col_vals(3))
    assert puzzle.is_consistent(p.get_col_vals(5))

def test_squares():
    assert puzzle.is_consistent(p.get_square_vals(0, 0))
    assert puzzle.is_consistent(p.get_square_vals(3, 0))
    assert puzzle.is_consistent(p.get_square_vals(6, 3))

def test_complete():
    p.complete()
    assert_equal(p.values, p_solved.values)
    assert_raises(puzzle.NoSolutionError, p_inconsistent.complete)

def test_reduce():
    p = puzzle.Puzzle()
    p.complete()
    print(p.render())
    values = p.render()
    p.reduce()
    p.complete()
    print(p.render())
    assert_equal(values, p.render())
