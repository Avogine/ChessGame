import engine


my_board = engine.Chessboard("r2qk2r/ppp2ppp/2n1b3/1BbpP3/8/2P1B1Q1/PPP3PP/R3K1NR w KQkq d6 0 2")

def turn():
    if my_board.movecount % 2 == 0:
        return "B"
    else:
        return "W"


def my_input(inp):  # konvertiert schachsprache zu int
    inp.replace(" ", "")
    x, y = list(inp)
    x = x.lower()
    if x == "a":
        return 80 - (int(y) * 10) + 1
    elif x == "b":
        return 80 - (int(y) * 10) + 2
    elif x == "c":
        return 80 - (int(y) * 10) + 3
    elif x == "d":
        return 80 - (int(y) * 10) + 4
    elif x == "e":
        return 80 - (int(y) * 10) + 5
    elif x == "f":
        return 80 - (int(y) * 10) + 6
    elif x == "g":
        return 80 - (int(y) * 10) + 7
    elif x == "h":
        return 80 - (int(y) * 10) + 8
    else:
        return 69


def my_output(out):  # konvertiert int zu schachsprache
    x = out % 10
    y = (out - x) / 10
    if x == 1:
        return "a" + str(int(8 - y))
    elif x == 2:
        return "b" + str(int(8 - y))
    elif x == 3:
        return "c" + str(int(8 - y))
    elif x == 4:
        return "d" + str(int(8 - y))
    elif x == 5:
        return "e" + str(int(8 - y))
    elif x == 6:
        return "f" + str(int(8 - y))
    elif x == 7:
        return "g" + str(int(8 - y))
    elif x == 8:
        return "h" + str(int(8 - y))


def zahl(i):  # gibt die Zahl rechts am Rand des Felds (1,2,3,4,...8)
    x = int((80 - i) / 10)
    return "\33[0;8m" + " " + str(x)


def ren(p):  # rendert das übergebene Feld(p)
    f = my_board.board[p]
    q = 0
    for z in str(p):
        q += int(z)
    if q % 2 == 0:
        back = True
    else:
        back = False
    if f == 0:
        if back:  # \33[48;5;238m = schwarzer Hintergrund
            return "\33[48;5;238m" + "\33[38;5;238m" + " ♟ "  # \33[48;5;248m = weißer Hintergrund
        else:  # \33[38;5;0m = schwarze Figuren
            return "\33[48;5;248m" + "\33[38;5;248m" + " ♟ "  # \33[38;5;255m = weiße Figuren
    elif f == 1:
        if back:
            return "\33[48;5;238m" + "\33[38;5;255m" + " ♟ "
        else:
            return "\33[48;5;248m" + "\33[38;5;255m" + " ♟ "
    elif f == 3:
        if back:
            return "\33[48;5;238m" + "\33[38;5;255m" + " ♞ "
        else:
            return "\33[48;5;248m" + "\33[38;5;255m" + " ♞ "
    elif f == 5:
        if back:
            return "\33[48;5;238m" + "\33[38;5;255m" + " ♝ "
        else:
            return "\33[48;5;248m" + "\33[38;5;255m" + " ♝ "
    elif f == 7:
        if back:
            return "\33[48;5;238m" + "\33[38;5;255m" + " ♜ "
        else:
            return "\33[48;5;248m" + "\33[38;5;255m" + " ♜ "
    elif f == 9:
        if back:
            return "\33[48;5;238m" + "\33[38;5;255m" + " ♛ "
        else:
            return "\33[48;5;248m" + "\33[38;5;255m" + " ♛ "
    elif f == 11:
        if my_board.stat_check == 2:
            if back:
                return "\33[48;5;238m" + "\33[38;5;1m" + " ♚ "
            else:
                return "\33[48;5;248m" + "\33[38;5;1m" + " ♚ "
        else:
            if back:
                return "\33[48;5;238m" + "\33[38;5;255m" + " ♚ "
            else:
                return "\33[48;5;248m" + "\33[38;5;255m" + " ♚ "
    elif f == 2:
        if back:
            return "\33[48;5;238m" + "\33[38;5;0m" + " ♟ "
        else:
            return "\33[48;5;248m" + "\33[38;5;0m" + " ♟ "
    elif f == 4:
        if back:
            return "\33[48;5;238m" + "\33[38;5;0m" + " ♞ "
        else:
            return "\33[48;5;248m" + "\33[38;5;0m" + " ♞ "
    elif f == 6:
        if back:
            return "\33[48;5;238m" + "\33[38;5;0m" + " ♝ "
        else:
            return "\33[48;5;248m" + "\33[38;5;0m" + " ♝ "
    elif f == 8:
        if back:
            return "\33[48;5;238m" + "\33[38;5;0m" + " ♜ "
        else:
            return "\33[48;5;248m" + "\33[38;5;0m" + " ♜ "
    elif f == 10:
        if back:
            return "\33[48;5;238m" + "\33[38;5;0m" + " ♛ "
        else:
            return "\33[48;5;248m" + "\33[38;5;0m" + " ♛ "
    elif f == 12:
        if my_board.stat_check == 1:
            if back:
                return "\33[48;5;238m" + "\33[38;5;1m" + " ♚ "
            else:
                return "\33[48;5;248m" + "\33[38;5;1m" + " ♚ "
        else:
            if back:
                return "\33[48;5;238m" + "\33[38;5;0m" + " ♚ "
            else:
                return "\33[48;5;248m" + "\33[38;5;0m" + " ♚ "


def term_render():  # rendert das aktuelle Chessboard
    print(f"""
                                            Material: {my_board.material}
                                            Check: {my_board.stat_check}""")
    for i in (0, 10, 20, 30, 40, 50, 60, 70):
        print(
            f"""        {ren(i + 1)}{ren(i + 2)}{ren(i + 3)}{ren(i + 4)}{ren(i + 5)}{ren(i + 6)}{ren(i + 7)}{ren(i + 8)}{zahl(i)}""")
    print("\n")
    print(f"| {my_board.conv_to_FEN()} |")
    print("\n")

speicher = [my_board.conv_to_FEN()]

while True:
    term_render()
    print(my_output(my_board.enpassant))
    pos = input("1: ")
    if pos == "back":
        my_board.reverse_move()
        sp = speicher.pop(len(speicher) - 2)
        if my_board.conv_to_FEN() == sp:
            print(True)
        else:
            print(False)
            print(sp)
            print(my_board.conv_to_FEN())

    elif pos == "render":
        pass
    else:
        #p_m = my_board.check_pos_moves(my_input(pos))
        #print(p_m)
        mov = input("2: ")
        if mov == "render":
            pass
        else:
            stat = my_board.move(my_input(pos), my_input(mov))
            print(stat)
            speicher.append(my_board.conv_to_FEN())
