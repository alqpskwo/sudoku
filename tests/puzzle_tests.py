from nose.tools import *
import sys
sys.path.append('sudoku'); import puzzle
import pickle

print("hi")

with open("sample", 'rb') as f:
    p = pickle.load(f)[0]

with open("sample_solved", 'rb') as f:
    p_solved = pickle.load(f)[0]

with open("sample_inconsistent", 'rb') as f:
    p_inconsistent = pickle.load(f)[0]
def test_empty():
    assert_equal(p.get_empty_cells(),
        [(0, 2), (0, 4), (0, 7), (1, 0), (1, 2), (1, 5), (1, 6), (1, 8),
         (2, 2), (2, 3), (2, 6), (2, 7), (3, 0), (3, 1), (3, 6), (3, 7),
         (3, 8), (4, 1), (4, 4), (4, 8), (5, 2), (5, 3), (5, 4), (5, 5),
         (5, 7), (6, 2), (6, 3), (6, 4), (6, 6), (6, 8), (7, 0), (7, 1),
         (7, 2), (7, 6), (8, 1), (8, 4), (8, 5), (8, 7)]
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
