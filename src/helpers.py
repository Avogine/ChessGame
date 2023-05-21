from pathlib import Path

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
]

sprites_path = Path(r'../src/sprites')


def get_piece_name(idx=0):
    return piece_sprite_path[idx]


def get_piece_sprite_path(idx=0):
    return Path(sprites_path, get_piece_name(idx))
