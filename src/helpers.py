from pathlib import Path
from colorama import *
from platform import system

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

sprites_path = Path(r'src/sprites')  # linux version

font_path = Path(r'src/fonts/highway_gothic.ttf')

stockfish_path_linux_x64 = Path(r'src/stockfish/linux_x64/stockfish-ubuntu-x86-64-avx2')
stockfish_path_windows_x64 = Path(r'src/stockfish/windows_x64/stockfish-windows-x86-64-avx2.exe')

"""♙♟♘♞♗♝♖♜♕♛♔♚"""

def get_piece_name(idx=0):
    return piece_sprite_path[idx]


def get_font_path():
    return Path(Path.cwd(), font_path)


def get_piece_sprite_path(idx=0):
    return Path(Path.cwd(), sprites_path, get_piece_name(idx))


def get_stockfish_path():
    # get current os type
    if system() == 'Windows':
        return Path(Path.cwd(), stockfish_path_windows_x64)
    elif system() == 'Linux':
        return Path(Path.cwd(), stockfish_path_linux_x64)
    else:
        print('Error trying to load stockfish binary for system type: ', system())
        print('What system are you on? - Currently no binary for this operating system included in our game.')



def get_marker_sprite_path():
    return Path(sprites_path, "pawn.png")


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