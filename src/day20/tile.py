from collections import defaultdict
from dataclasses import dataclass
from enum import Enum

import numpy as np


class Flip(Enum):
    NoFlip = 0
    Horizontal = 1
    Vertical = 2
    Transpose = 3

    def __repr__(self):
        if self == self.NoFlip:
            return "NoFlip"
        elif self == self.Horizontal:
            return "Horizontal"
        elif self == self.Vertical:
            return "Vertical"
        elif self == self.Transpose:
            return "Transpose"


class Edge(Enum):
    North = 0
    South = 1
    East = 2
    West = 3

    def __invert__(self):
        """tilda operator returns the 180 degree opposide edge"""
        if self == self.North:
            return self.South
        elif self == self.South:
            return self.North
        elif self == self.East:
            return self.West
        elif self == self.West:
            return self.East

    def __repr__(self):
        if self == self.North:
            return "North"
        elif self == self.South:
            return "South"
        elif self == self.East:
            return "East"
        elif self == self.West:
            return "West"


# of the 16 possible combinations of flipping then rotating
# only 8 of them give unique results
# rotating is counter-clockwise per numpy convention
UNIQUE_TRANSFORMS = (
    (Flip.NoFlip, 0),
    (Flip.NoFlip, 1),
    (Flip.NoFlip, 2),
    (Flip.NoFlip, 3),
    (Flip.Horizontal, 0),
    (Flip.Vertical, 0),
    (Flip.Transpose, 0),
    (Flip.Vertical, 1),
)


@dataclass
class Tile:
    data: np.array = None

    def transform(self, flip, rotate):
        if flip == Flip.NoFlip:
            new_data = self.data
        elif flip == Flip.Horizontal:
            new_data = np.fliplr(self.data)
        elif flip == Flip.Vertical:
            new_data = np.flipud(self.data)
        elif flip == Flip.Transpose:
            new_data = self.data.T
        else:
            raise ValueError("Not a valid flip")

        assert 0 <= rotate <= 3
        new_data = np.rot90(new_data, rotate)

        return Tile(new_data)

    def north(self):
        return self.data[0, :]

    def south(self):
        return self.data[-1, :]

    def east(self):
        return self.data[:, -1]

    def west(self):
        return self.data[:, 0]

    def edge(self, edge):
        if edge == Edge.North:
            return self.north()
        elif edge == Edge.South:
            return self.south()
        elif edge == Edge.East:
            return self.east()
        elif edge == Edge.West:
            return self.west()
        raise ValueError("Unknowned edge")

    def match_edges(self, my_side, other):
        """Reorient other tile until it matches self on my_side """
        my_edge = self.edge(my_side)
        other_side = ~my_side

        for transform in UNIQUE_TRANSFORMS:
            xother = other.transform(*transform)
            if (xother.edge(other_side) == my_edge).all():
                return xother

        raise ValueError("edge match failed")

    def append_right(self, right, debug=True):
        data_left = self.trim_edge(Edge.East).data
        data_right = right.trim_edge(Edge.West).data
        return Tile(np.hstack([data_left, data_right]))

    def append_below(self, below, debug=True):
        data_up = self.trim_edge(Edge.South).data
        data_down = below.trim_edge(Edge.North).data
        return Tile(np.vstack([data_up, data_down]))

    def trim_edge(self, edge):
        if edge == Edge.North:
            return Tile(self.data[1:, :])
        elif edge == Edge.South:
            return Tile(self.data[:-1, :])
        elif edge == Edge.East:
            return Tile(self.data[:, :-1])
        elif edge == Edge.West:
            return Tile(self.data[:, 1:])

        raise ValueError("Invalid Edge to trim")

    def trim_all_edges(self):
        return (
            self.trim_edge(Edge.North)
            .trim_edge(Edge.South)
            .trim_edge(Edge.East)
            .trim_edge(Edge.West)
        )

    def count_pattern(self, pattern):
        """Count how many time pattern appears in self"""
        me = self.data
        my_rows, my_cols = me.shape

        other = pattern.data
        other_rows, other_cols = other.shape

        walk_cols = my_cols - other_cols
        walk_rows = my_rows - other_rows

        count = 0
        for row in range(walk_rows):
            for col in range(walk_cols):
                if (
                    other & me[row : row + other_rows, col : col + other_cols] == other
                ).all():
                    count += 1
        return count


@dataclass
class TilePuzzle:
    tiles: dict = None
    layout: np.array = None

    def __post_init__(self):
        if self.layout is None:
            nrow = ncol = int(np.sqrt(len(self.tiles)))
            self.layout = np.empty((nrow, ncol), dtype=np.int64)

    def __getitem__(self, key):
        # return the tile object at layout[key]
        tile_id = self.layout[key]
        return self.tiles[tile_id]

    def __setitem__(self, key, value):
        # update the tile dictionary id at layout[key] to value
        tile_id = self.layout[key]
        self.tiles[tile_id] = value

    def solve(self):
        return self.assemble_tiles().orient_tiles()

    def combine_pieces(self):
        nrow, ncol = self.layout.shape
        rows = []
        for row in range(nrow):
            row_agg = self[row, 0]
            for col in range(1, ncol):
                row_agg = row_agg.append_right(self[row, col])
            rows.append(row_agg)

        row_agg = rows[0]
        for tile in rows[1:]:
            row_agg = row_agg.append_below(tile)

        return row_agg.trim_all_edges()

    def possible_neighbors(self):
        """Return a map of all tileids and the tile ids that could possibly
        neighbor that tile id"""
        # make a reverse map of all possible edges (as-is and flipped)
        # and the tile ids that have that edge"""
        reverse_map = defaultdict(set)
        for tile_id, tile_obj in self.tiles.items():
            for flip, rotate in UNIQUE_TRANSFORMS:
                for e in Edge:
                    edge = tuple(tile_obj.transform(flip, rotate).edge(e))
                    reverse_map[edge].add(tile_id)

        # use the reverse map to make a map from a tile id to
        # the other tiles it could neighbor
        tile_to_neighbors = defaultdict(set)
        for neighbor_set in reverse_map.values():
            for neighbor in neighbor_set:
                tile_to_neighbors[neighbor] = tile_to_neighbors[neighbor].union(
                    neighbor_set - set([neighbor])
                )
        return tile_to_neighbors

    def assemble_tiles(self):
        """Puts the tiles in the right layout, but orientation fixes
        still needed"""

        nrow, ncol = self.layout.shape
        neighs = self.possible_neighbors()

        # Puzzle has "nice inputs"
        # interior tiles have exactly 4 possible neighbors,
        # edges exactly 3, and corners exactly 2
        interiors = []
        edges = []
        corners = []

        for tile_id, neighbor_set in neighs.items():
            if len(neighbor_set) == 4:
                interiors.append(tile_id)
            elif len(neighbor_set) == 3:
                edges.append(tile_id)
            else:
                assert len(neighbor_set) == 2
                corners.append(tile_id)

        # upper left corner
        self.layout[0, 0] = corners.pop()
        self.layout[0, 1] = list(neighs[self.layout[0, 0]])[0]
        edges.remove(self.layout[0, 1])

        # top row
        for col in range(2, ncol - 1):
            prev_coord = (0, col - 1)
            tile_id = [e for e in neighs[self.layout[prev_coord]] if e in edges][0]
            self.layout[0, col] = tile_id
            edges.remove(tile_id)

        # top right corner
        prev_coord = (0, ncol - 2)
        tile_id = [c for c in neighs[self.layout[prev_coord]] if c in corners][0]
        self.layout[0, ncol - 1] = tile_id
        corners.remove(tile_id)

        # left and right edges
        for row in range(1, nrow - 1):
            for col in (0, ncol - 1):
                prev_coord = (row - 1, col)
                tile_id = [e for e in neighs[self.layout[prev_coord]] if e in edges][0]
                self.layout[row, col] = tile_id
                edges.remove(tile_id)

        # bottom left and right corners
        for col in (0, ncol - 1):
            prev_coord = (nrow - 2, col)
            tile_id = [c for c in neighs[self.layout[prev_coord]] if c in corners][0]
            self.layout[nrow - 1, col] = tile_id
            corners.remove(tile_id)

        # bottom row, non-corners
        for col in range(1, ncol - 1):
            prev_coord = (nrow - 1, col - 1)
            tile_id = [e for e in neighs[self.layout[prev_coord]] if e in edges][0]
            self.layout[nrow - 1, col] = tile_id
            edges.remove(tile_id)

        # interior tiles
        for row in range(1, nrow - 1):
            for col in range(1, ncol - 1):
                prev_coord = (row - 1, col)
                tile_id = [
                    i for i in neighs[self.layout[prev_coord]] if i in interiors
                ][0]
                self.layout[row, col] = tile_id
                interiors.remove(tile_id)
        return self

    def orient_tiles(self):
        nrow, ncol = self.layout.shape

        # fix upper left corner
        corner = self[0, 0]
        right = self[0, 1]
        below = self[1, 0]

        for transform in UNIQUE_TRANSFORMS:
            corner = corner.transform(*transform)
            try:
                new_right = corner.match_edges(Edge.East, right)
                new_below = corner.match_edges(Edge.South, below)
            except ValueError:
                pass
            else:
                right = new_right
                below = new_below
                break

        assert (corner.east() == right.west()).all()
        assert (corner.south() == below.north()).all()

        self[0, 0] = corner
        self[0, 1] = right
        self[1, 0] = below

        # top row of puzzle
        for col in range(2, ncol):
            self[0, col] = self[0, col - 1].match_edges(Edge.East, self[0, col])

        # left and right columns
        for col in (0, ncol - 1):
            for row in range(1, nrow):
                self[row, col] = self[row - 1, col].match_edges(
                    Edge.South, self[row, col]
                )

        # bottom edge
        for col in range(1, ncol - 1):
            self[nrow - 1, col] = self[nrow - 1, col - 1].match_edges(
                Edge.East, self[nrow - 1, col]
            )

        # interior tiles
        for row in range(1, nrow - 1):
            for col in range(1, ncol - 1):
                self[row, col] = self[row - 1, col].match_edges(
                    Edge.South, self[row, col]
                )

        return self
