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
    column = int_pos % rowcount

    return (row, column)

def pos_to_int(x: int, y: int, rowcount=8, colcount=8):
    return y * colcount + x