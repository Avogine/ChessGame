from pathlib import Path
from colorama import *

piece_sprite_path = [
    None,
    "white_pawn.png",
    "black_pawn.png",
    "white_knight.png",
    "black_knight.png",
    "white_bishop.png",
    "black_bishop.png",
    "white_rook.png",
    "black_rook.png",
    "white_queen.png",
    "black_queen.png",
    "white_king.png",
    "black_king.png"
]

sprites_path = Path(r'../src/sprites')


"""♙♟♘♞♗♝♖♜♕♛♔♚"""

def get_piece_name(idx=0):
    return piece_sprite_path[idx]


def get_piece_sprite_path(idx=0):
    return Path(sprites_path, get_piece_name(idx))


def get_marker_sprite_path():
    return Path(sprites_path, "marker.png")


def int_to_rowcolumn(int_pos=0, rowcount=8, colcount=8) -> tuple:
    row = int(int_pos / colcount) # rows and columns start at 0
    column = int_pos % colcount

    return (row, column)


def pos_to_int(x: int, y: int, rowcount=8, colcount=8):
    return y * colcount + x


def engineint_to_rowcolumn(engine_int: int):
    #rowcount = 8 # also not needed
    colcount = 10

    row = int(engine_int / colcount)
    column = engine_int % colcount - 1

    return (row, column)


def pos_to_engineint(x: int, y: int):
    #rowcount = 8 # not needed here
    colcount = 10
    return (y * colcount + x + 1)


# BROKEN FIXME
def int_engine2gui(int_pos: int):
    # convert to uniform x y system
    y, x = int_to_rowcolumn(int_pos, 8, 10)

    # convert to gui system
    return pos_to_int(x, y, 8, 8)