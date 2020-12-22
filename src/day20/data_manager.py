import numpy as np
from pathlib import Path
from tile import Tile

test_input = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""

def personal_input():
    return Path('tiles.txt').read_text()

    
def data_reader(text):
    all_tiles = {}        
    for tile in text.split("\n\n"):
        lines = tile.splitlines()
        header = lines[0]
        tile_data = lines[1:]
        
        # validate we got a header
        assert header.startswith("Tile")
        tile_id = int(header.split()[1][:-1])
        this_tile = (np.array(
            [
                list(k) for k in tile_data
            ]
        ) == '#').astype(np.int)
        all_tiles[tile_id] = Tile(this_tile)
    return all_tiles


def load_test_data():
    return data_reader(test_input)

def load_problem_data():
    return data_reader(personal_input())

sea_monster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """

def load_sea_monster():
    lines = sea_monster.splitlines()
    return Tile(
        (np.array(
            [ list(k) for k in lines ]
        ) == '#').astype(np.int)
    )
    