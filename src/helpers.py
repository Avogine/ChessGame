from pathlib import Path
from colorama import *

use_linux_paths = True  # TODO: use a better way to handle this

piece_sprite_path = [
    None,
    "wp.svg",
    "bp.svg",
    "wn.svg",
    "bn.svg",
    "wb.svg",
    "bb.svg",
    "wr.svg",
    "br.svg",
    "wq.svg",
    "bq.svg",
    "wk.svg",
    "bk.svg"
]

sprites_path_win = Path(r'~\..\src\sprites')  # windows version
sprites_path_linux = Path(r'../src/sprites')  # linux version

font_path_win = Path(r'~\..\src\fonts\highway_gothic.ttf')  # windows version
font_path_linux = Path(r'../src/fonts/highway_gothic.ttf')  # linux version


"""♙♟♘♞♗♝♖♜♕♛♔♚"""

def get_piece_name(idx=0):
    return piece_sprite_path[idx]


def get_font_path():
    if use_linux_paths:
        return font_path_linux
    else:
        return font_path_win


def get_piece_sprite_path(idx=0):
    if use_linux_paths:
        return Path(sprites_path_linux, get_piece_name(idx))
    else:
        return Path(sprites_path_win, get_piece_name(idx))


def get_stockfish_path():
    if use_linux_paths:
        return r'../src/stockfish/linux/stockfish_15.1_linux_x64/stockfish-ubuntu-20.04-x86-64'
    else:
        return r"C:\Users\david\Desktop\Python\ChessGame\src\stockfish\stockfish_15.1_win_x64_popcnt\stockfish-windows-2022-x86-64-modern.exe" # FIXME


def get_marker_sprite_path():
    if use_linux_paths:
        return Path(sprites_path_linux, "pawn.png")
    else:
        return Path(sprites_path_win, "pawn.png")


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