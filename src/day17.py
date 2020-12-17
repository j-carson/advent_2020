from itertools import product


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


class DimensionalSpace:
    def __init__(self, *ranges, ndim):
        self.ranges = list(ranges)
        while len(self.ranges) < ndim:
            self.ranges.append(Range(0, 0))

    def __iter__(self):
        args = (r for r in self.ranges)
        for j in product(*args):
            yield j

    def expand1(self):
        for r in self.ranges:
            r.expand1()


class Grid:
    def __init__(self, my_input, ndim):

        self.grid = set()
        zero_pad = [0 for _ in range(ndim - 2)]

        for row, line in enumerate(my_input.splitlines()):
            for col, ch in enumerate(line):
                if ch == "#":
                    # active
                    self.grid.add(tuple([row, col] + zero_pad))

        x_range = Range(0, row)
        y_range = Range(0, col)
        self.space = DimensionalSpace(x_range, y_range, ndim=ndim)

    def count_neighbors(self, coord):
        count = 0
        search_area = (range(ii - 1, ii + 2) for ii in coord)
        for search_point in product(*search_area):
            if search_point == coord:
                continue
            if search_point in self.grid:
                count += 1
                # only care if is two or three, no sense going past here
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

        self.space.expand1()
        for coord in self.space:
            am_active = coord in self.grid
            neighbors = self.count_neighbors(coord)
            if am_active and (neighbors in (2, 3)):
                new_grid.add(coord)
            elif (not am_active) and (neighbors == 3):
                new_grid.add(coord)

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

    g = Grid(my_input, ndim=3)
    for _ in range(6):
        g.cycle()

    print(len(g.grid))

    g = Grid(my_input, ndim=4)
    for _ in range(6):
        g.cycle()

    print(len(g.grid))
