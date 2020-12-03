import numpy as np


class TreeMaze:
    def __init__(self):
        with open("day3_input.txt") as fp:
            text = fp.read()
        lines = text.split("\n")
        self.data = np.array([list(line) for line in lines])
        self.n_rows, self.n_columns = self.data.shape

    def is_tree(self, pos):
        row, col = pos
        if row >= self.n_rows:
            raise Exception("Too low!")
        if col >= self.n_columns:
            col = col % self.n_columns

        char = self.data[row, col]
        return char == "#"

    def count_trees(self, over, down):
        my_pos = np.array((0, 0))
        my_step = np.array((down, over))

        n_trees = 0
        while my_pos[0] < self.n_rows:
            n_trees += self.is_tree(my_pos)
            my_pos += my_step
        return n_trees


game = TreeMaze()
part_a = game.count_trees(3, 1)
print(part_a)

counts = [game.count_trees(*a) for a in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))]

print(np.prod(counts))
