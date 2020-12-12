import numpy as np


class SeatChart:
    
    def __repr__(self):
        rep = np.empty(self.occupied.shape, dtype=str)
        rep[:, :] = "L"
        rep[self.occupied == 1] = "#"
        rep[self.floor_mask == 0] = "."
        rows = ["".join(rep[r, :]) for r in range(rep.shape[0])]
        result = "\n".join(rows)
        return result

    def __init__(self, data):
        lines = data.splitlines()
        chart = np.array([list(row) for row in lines])
        self.floor_mask = (chart != ".").astype(np.int)
        self.occupied = np.zeros(chart.shape).astype(np.int)
        self.debug = False
        self.q2_neighbors = None
        
    def iterate_q1(self):
        padded = np.pad(self.occupied, (1, 1))
        result = np.zeros(self.occupied.shape, dtype=np.int)

        for r in range(self.occupied.shape[0]):
            for c in range(self.occupied.shape[1]):
                if self.debug:
                    breakpoint()
                surrounding = padded[r : r + 3, c : c + 3]
                flag = surrounding.sum() - surrounding[1, 1]
                if flag == 0:
                    result[r, c] = 1
                elif flag >= 4:
                    result[r, c] = 0
                else:
                    result[r, c] = self.occupied[r, c]

        result = result * self.floor_mask
        changed = not (result == self.occupied).all()
        self.occupied = result
        return changed
    
    def cache_neighbor_locations(self):
        if self.q2_neighbors is None:
            
            nrows, ncols = self.occupied.shape
            
            self.q2_neighbors = np.empty(self.occupied.shape, dtype=list)
            
            # what to add to a row/column location to get the one just above,
            # above/right diagonal, right, etc.
            N = (-1, 0)
            NE = (-1, 1)
            E = (0, 1)
            SE = (1, 1)
            S = (1, 0)
            SW =(1, -1)
            W = (0, -1)
            NW =(-1, -1)
            directions = (N, NE, E, SE, S, SW, W, NW)
            
            def legal_pos(r,c):
                # python accepts negative indices, but don't want 
                # those so check indices by hand
                return ((r >= 0) and 
                        (r < nrows) and
                        (c >= 0) and
                        (c < ncols)
                       )
            
            for r in range(self.occupied.shape[0]):
                for c in range(self.occupied.shape[1]):
                    
                    self.q2_neighbors[r,c] = list()
                    
                    # if there's no chair, don't need this
                    if self.floor_mask[r,c] == 0:
                        continue
                        
                    for vdir in directions:
                        done = False
                        pos_r = r + vdir[0]
                        pos_c = c + vdir[1]
                        
                        while not done:
                            if not legal_pos(pos_r,pos_c):
                                # ran off edge, no neighbor to look at
                                done = True
                            elif self.floor_mask[pos_r,pos_c] != 0:
                                # found a neighborly chair
                                self.q2_neighbors[r,c].append(tuple([pos_r, pos_c]))
                                done = True
                            else:
                                # else keep stepping in current direction
                                pos_r += vdir[0]
                                pos_c += vdir[1]
                            

    def iterate_q2(self):
        self.cache_neighbor_locations()
        result = np.zeros(self.occupied.shape)

        for r in range(self.occupied.shape[0]):
            for c in range(self.occupied.shape[1]):
                
                flag = 0
                for neighbor in self.q2_neighbors[r, c]:
                     flag += self.occupied[neighbor[0], neighbor[1]]
                
                if flag == 0:
                    result[r, c] = 1
                elif flag >= 5:
                    result[r, c] = 0
                else:
                    result[r, c] = self.occupied[r, c]

        result = result * self.floor_mask
        changed = not (result == self.occupied).all()
        self.occupied = result
        return changed


if __name__ == "__main__":

    test_case = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

    with open("seats.txt") as fp:
        my_data = fp.read()

    #####
    # my_data = test_case

    chart = SeatChart(my_data)

    # print(chart, "\n")

    changed = True
    count = 0
    while changed:
        changed = chart.iterate_q2()
        # print(changed)
        # print(chart, "\n")
        count += 1
        if count > 1000:
            print("oops")
            break

    print(chart.occupied.sum())
