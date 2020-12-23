from itertools import product


class Grid:
    def __init__(self, my_input, ndim):
        
        self.grid = set()
        zero_pad = [0 for _ in range(ndim - 2)]

        for row, line in enumerate(my_input.splitlines()):
            for col, ch in enumerate(line):
                if ch == "#": # active
                    self.grid.add(tuple([row, col] + zero_pad))
                    
                    
    @staticmethod
    def get_neighbors(coord):
        neighbors = (range(ii - 1, ii + 2) for ii in coord)
        for nn in product(*neighbors):
            if nn != coord: # coord is not it's own neighbor
                yield nn

                
    def count_neighbors(self, coord):
        "counts active neighbors"
        count = 0
        for search_point in self.get_neighbors(coord):
            if search_point in self.grid:
                count += 1
        return count
    

    def cycle(self):
        """
        If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.
                Otherwise, the cube becomes inactive.
        If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active.
                Otherwise, the cube remains inactive.
        """
        
        # cubes that are active or that are neighbors of an active
        # point are the only ones that might possibly change
        must_consider = self.grid.copy()
        for coord in self.grid:
            for nn in self.get_neighbors(coord):
                must_consider.add(nn)
        
        new_grid = set()

        for coord in must_consider:
            
            am_active = coord in self.grid
            active_neighbors = self.count_neighbors(coord)
            
            if am_active and (active_neighbors in (2, 3)):
                new_grid.add(coord)
                
            elif (not am_active) and (active_neighbors == 3):
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
