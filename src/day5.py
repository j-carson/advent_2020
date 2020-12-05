import pandas as pd


def seat_id(row, col):
    """Turns row/column into seat id from formula in puzzle"""
    return (row * 8) + col


class SeatSearch:
    def __init__(self, lower_bound, upper_bound):
        self.lower = lower_bound
        self.upper = upper_bound
        self.size = self.upper - self.lower + 1

    def lower_half(self):
        return SeatSearch(self.lower, self.upper - self.size // 2)

    def upper_half(self):
        return SeatSearch(self.lower + self.size // 2, self.upper)

    def final(self):
        """final seat after search - make sure we converged first"""
        assert self.lower == self.upper
        return self.lower


def boarding_pass_to_location(pass_):
    """Find the row and column of the given boarding pass,
    according to the puzzle algorithm"""

    action_decode = {
        "F": lambda row, col: (row.lower_half(), col),
        "B": lambda row, col: (row.upper_half(), col),
        "L": lambda row, col: (row, col.lower_half()),
        "R": lambda row, col: (row, col.upper_half()),
    }

    row_bounds = SeatSearch(0, 127)
    col_bounds = SeatSearch(0, 7)

    for c in pass_:
        row_bounds, col_bounds = action_decode[c](row_bounds, col_bounds)

    return seat_id(row_bounds.final(), col_bounds.final())


if __name__ == "__main__":
    with open("boarding_passes.txt") as fp:
        data = fp.read().split()

    # part A = what's the largest seat_id in your input data?
    all_seatids = [boarding_pass_to_location(pass_) for pass_ in data]
    print(max(all_seatids))

    # part B = where's the open seat?
    # put the seat ids in sorted order, where there's a bump from
    # counting by 1's that's where the gap is - the open seat
    # is one back from the seat next to the gap
    sorted_seatids = sorted(all_seatids)
    ser = pd.Series(index=sorted_seatids, data=sorted_seatids)
    gap = ser.diff().idxmax()
    print(gap - 1)
