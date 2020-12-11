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

    def iterate_q1(self):
        padded = np.pad(self.occupied, (1, 1))
        result = np.zeros(self.occupied.shape)

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

    def iterate_q2(self):
        # very slow, but worked
        result = np.zeros(self.occupied.shape)

        for r in range(self.occupied.shape[0]):
            for c in range(self.occupied.shape[1]):

                N = np.array((-1, 0))
                NE = np.array((-1, 1))
                E = np.array((0, 1))
                SE = np.array((1, 1))
                S = np.array((1, 0))
                SW = np.array((1, -1))
                W = np.array((0, -1))
                NW = np.array((-1, -1))

                flag = 0

                if self.debug:
                    breakpoint()

                for direction in (N, NE, E, SE, S, SW, W, NW):
                    look = np.array((r, c)) + direction

                    looked = False
                    dirflag = 0

                    while not looked:
                        if (look < 0).any():
                            # we don't want python negative indexing in this one!
                            dirflag = 0
                            looked = True
                        else:
                            try:
                                occ = self.occupied[look[0], look[1]]
                                flr = self.floor_mask[look[0], look[1]]
                            except IndexError:
                                dirflag = 0
                                looked = True
                            else:
                                if flr:  # floor_mask is 1 = seat, 0 = floor
                                    dirflag = occ
                                    looked = True

                        look += direction

                    flag += dirflag

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

    print(chart, "\n")

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
