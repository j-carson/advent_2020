class Range:
    def __init__(self, low=0, high=0):
        self.low = low
        self.high = high

    def __repr__(self):
        return f"Range(low={self.low},high={self.high})"

    def expand1(self):
        self.low -= 1
        self.high += 1

    def __iter__(self):
        for i in range(self.low, self.high + 1):
            yield i


class Grid:
    def __init__(self, my_input):
        self.grid = set()
        for row, line in enumerate(my_input.splitlines()):
            for col, ch in enumerate(line):
                if ch == "#":
                    # active
                    self.grid.add((row, col, 0))

        self.x_range = Range(0, row)
        self.y_range = Range(0, col)
        self.z_range = Range(0, 0)

    def count_neighbors(self, x, y, z):
        count = 0
        for ix in range(x - 1, x + 2):
            for iy in range(y - 1, y + 2):
                for iz in range(z - 1, z + 2):
                    if all((ix == x, iy == y, iz == z)):
                        continue
                    if (ix, iy, iz) in self.grid:
                        count += 1
        return count

    def cycle(self):
        """
        If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.
                Otherwise, the cube becomes inactive.
        If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active.
                Otherwise, the cube remains inactive.
        """
        new_grid = set()

        self.x_range.expand1()
        self.y_range.expand1()
        self.z_range.expand1()

        for x in self.x_range:
            for y in self.y_range:
                for z in self.z_range:
                    am_active = (x, y, z) in self.grid
                    neighbors = self.count_neighbors(x, y, z)
                    if am_active and (neighbors in (2, 3)):
                        new_grid.add((x, y, z))
                    elif (not am_active) and (neighbors == 3):
                        new_grid.add((x, y, z))

        self.grid = new_grid


class Grid4D:
    def __init__(self, my_input):
        self.grid = set()
        for row, line in enumerate(my_input.splitlines()):
            for col, ch in enumerate(line):
                if ch == "#":
                    # active
                    self.grid.add((row, col, 0, 0))

        self.x_range = Range(0, row)
        self.y_range = Range(0, col)
        self.z_range = Range(0, 0)
        self.w_range = Range(0, 0)

    def count_neighbors(self, x, y, z, w):
        count = 0
        for ix in range(x - 1, x + 2):
            for iy in range(y - 1, y + 2):
                for iz in range(z - 1, z + 2):
                    for iw in range(w - 1, w + 2):
                        if all((ix == x, iy == y, iz == z, iw == w)):
                            continue
                        if (ix, iy, iz, iw) in self.grid:
                            count += 1
                            if count > 3:
                                return count
        return count

    def cycle(self):
        """
        If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.
                Otherwise, the cube becomes inactive.
        If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active.
                Otherwise, the cube remains inactive.
        """
        new_grid = set()

        self.x_range.expand1()
        self.y_range.expand1()
        self.z_range.expand1()
        self.w_range.expand1()

        for x in self.x_range:
            for y in self.y_range:
                for z in self.z_range:
                    for w in self.w_range:
                        am_active = (x, y, z, w) in self.grid
                        neighbors = self.count_neighbors(x, y, z, w)
                        if am_active and (neighbors in (2, 3)):
                            new_grid.add((x, y, z, w))
                        elif (not am_active) and (neighbors == 3):
                            new_grid.add((x, y, z, w))

        self.grid = new_grid


if __name__ == "__main__":

    my_input = """.#.#.#..
..#....#
#####..#
#####..#
#####..#
###..#.#
#..##.##
#.#.####"""

    g = Grid(my_input)
    for _ in range(6):
        g.cycle()

    print(len(g.grid))

    g = Grid4D(my_input)
    for _ in range(6):
        g.cycle()

    print(len(g.grid))
