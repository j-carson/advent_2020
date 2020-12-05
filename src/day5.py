import pandas as pd


def seat_id(spot):
    row, col = spot
    return (row * 8) + col


def trim_low(bounds):
    """Trims off the lower half of the given bounds"""
    bounds_size = bounds[1] - bounds[0] + 1
    return [bounds[0] + bounds_size // 2, bounds[1]]


def trim_high(bounds):
    """Trims off the upper half of the given bounds"""
    bounds_size = bounds[1] - bounds[0] + 1
    return [bounds[0], bounds[1] - bounds_size // 2]


def boarding_pass_to_location(pass_):
    """Find the row and column of the given boarding pass,
    according to the puzzle algorithm
    """
    row_bounds = [0, 127]
    col_bounds = [0, 7]

    for c in pass_:
        if c == "F":
            row_bounds = trim_high(row_bounds)
        elif c == "B":
            row_bounds = trim_low(row_bounds)
        elif c == "L":
            col_bounds = trim_high(col_bounds)
        elif c == "R":
            col_bounds = trim_low(col_bounds)

    return [row_bounds[0], col_bounds[0]]


if __name__ == "__main__":
    with open("boarding_passes.txt") as fp:
        data = fp.read().split()

    # part A = what's the largest seat_id in your input data?
    all_seatids = [seat_id(boarding_pass_to_location(pass_)) for pass_ in data]
    print(max(all_seatids))

    # part B = where's the open seat?
    sorted_seatids = sorted(all_seatids)
    s = pd.Series(index=sorted_seatids, data=sorted_seatids)
    gap = s.diff().idxmax()
    print(gap)
