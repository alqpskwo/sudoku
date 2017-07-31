from random import sample, shuffle

class NoSolutionError(Exception):
    pass

class Puzzle(object):
    def __init__(self):
        self.values = {(row, col) : 0 for row in range(0, 9)
                                      for col in range(0, 9)}

    def get_row_vals(self, row):
        return [self.values[row, col] for col in range(0, 9)]

    def get_col_vals(self, col):
        return [self.values[row, col] for row in range(0, 9)]

    def get_square_vals(self, ul_row, ul_col):
        return [self.values[row, col] for row in range(ul_row, ul_row + 3)
                                      for col in range(ul_col, ul_col + 3)]

    def get_empty_cells(self):
        return [(row, col) for row in range(0, 9)
                           for col in range(0, 9)
                           if self.values[row, col] == 0]

    def check_consistent(self):
        result = True
        for row in range(0, 9):
            result = result and is_consistent(self.get_row_vals(row))

        for col in range(0, 9):
            result = result and is_consistent(self.get_col_vals(col))

        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                result = result and is_consistent(self.get_square_vals(row, col))
        return result

    def complete(self):
        todo = self.get_empty_cells()
        done = []
        candidates = {}
        for cell in todo:
                candidates[cell] = sample(range(1,10), 9)

        while todo:
            if candidates[todo[-1]]:
                self.values[todo[-1]] = candidates[todo[-1]].pop()
                if self.check_consistent():
                    done.append(todo.pop())
            elif done:
                candidates[todo[-1]] = sample(range(1, 10), 9)
                self.values[todo[-1]] = 0
                todo.append(done.pop())
            else:
                raise NoSolutionError("The puzzle cannot be solved.")

    def generate(self):
        self.complete()
        self.reduce()

    def reduce(self):
        non_empty = [(row, col) for row in range(0, 9)
                           for col in range(0, 9)
                           if self.values[row, col] != 0]
        shuffle(non_empty)
        while non_empty:
            row, col = non_empty.pop()
            if self.is_determined(row, col):
                self.values[row,col] = 0

    def is_determined(self, row, col):
        candidates = list(range(1, 10))
        for r in range(0, 9):
            if r != row:
                try:
                    candidates.remove(self.values[r, col])
                except ValueError:
                    pass

        for c in range(0, 9):
            if c != col:
                try:
                    candidates.remove(self.values[row, c])
                except ValueError:
                    pass

        square =  [(r, c) for r in range(3 * (row // 3), 3 * (row // 3) + 3)
                          for c in range(3 * (col // 3), 3 * (col // 3) + 3)]
        for (r, c) in square:
            if (r, c) != (row, col):
                try:
                    candidates.remove(self.values[r, c])
                except ValueError:
                    pass
        return len(candidates) <= 1


    def render(self):
        string = ""
        for row in range(0, 9):
            for col in range(0, 9):
                string += str(self.values[row, col])
            string += '\n'
        return string


def is_consistent(values):
    stripped = [x for x in values if x != 0]
    return len(stripped) == len(set(stripped))
