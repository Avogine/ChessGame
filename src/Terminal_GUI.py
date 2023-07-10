import engine2


my_board = engine2.Chessboard("7k/5Q2/8/8/8/8/8/4K3 w - - 1 16")
#2bq1k2/2pppp2/8/8/1b6/2B5/2P1P3/3QK3 w - - 0 2
def turn():
    if my_board.movecount % 2 == 0:
        return "B"
    else:
        return "W"


def my_input(inp):  # konvertiert schachsprache zu int
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
        if my_board.w_check:
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
        if my_board.b_check:
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
                                            Material: {my_board.material}""")
    for i in (0, 10, 20, 30, 40, 50, 60, 70):
        print(
            f"""        {ren(i + 1)}{ren(i + 2)}{ren(i + 3)}{ren(i + 4)}{ren(i + 5)}{ren(i + 6)}{ren(i + 7)}{ren(i + 8)}{zahl(i)}""")
    print("\n")
    print(f"| {my_board.conv_to_FEN()} |")
    print("\n")


def movement(position, move, leg_moves):
    print(move)
    my_figur = my_board.return_figur(move)
    if move in leg_moves:  # move ist legal
        stat = my_board.move(position, move)
        take = my_figur
        if take != "":  # keine gegnerische Figur auf move
            take = f"You took a {take}."
        print(f"[T] Good move.{take} Next Player ({my_board.movecount}), {stat}")
    elif 0 < my_figur < 13 and my_figur % 2 == my_board.movecount % 2:  # eine andere Figur wurde ausgewählt
        leg_moves = tuple(my_board.check_pos_moves(move))
        if leg_moves:  # die neue Figur hat legale moves
            r = my_output(leg_moves[0])
            my_legal_moves = list(leg_moves)
            del my_legal_moves[0]
            i = -1
            for p in my_legal_moves:
                i += 1
                r = r + " and " + my_output(p)
            r = r.replace(" and ", " ,", i)
            print(f"[T] {my_output(move)} was selected. Your legal moves are {r}")
            new_move = input(f"[{turn()}] Move: ")
            new_move = my_input(new_move)
            movement(move, new_move, leg_moves)
        else:
            print(f"[T] {my_output(move)} was selected but it has no legal moves")
            new_position = input(f"[{turn()}] Select: ")
            select(new_position)

    else:  # move ist nicht legal
        r = my_output(leg_moves[0])
        my_legal_moves = list(leg_moves)
        del my_legal_moves[0]
        i = -1
        for p in my_legal_moves:
            i += 1
            r = r + " and " + my_output(p)
        r = r.replace(" and ", " ,", i)
        print(f"[T] {my_output(move)} is not a legal move. Your legal moves are {r}.")
        move = my_input(input(f"[{turn()}] Move: "))
        movement(position, move, leg_moves)


def select(position):
    if len(position) == 2:  # eine Position wurde angegeben
        position = int(my_input(position))
        if position == 69:  # die Position ist falsch geschrieben (x9)
            print("[T] That's not a square")
            new_position = input(f"[{turn()}] Select: ")
            select(new_position)
        else:
            figur = my_board.return_figur(position)
            if figur == 0 or figur == 13:  # auf der Position ist keine Figur (20)
                print("[T] You wanna play with air? ")
                new_position = input(f"[{turn()}] Select: ")
                select(new_position)

            elif figur % 2 != my_board.movecount % 2:  # auf der Position ist eine Figur des Gegners
                print("[T] You must select one of your own pieces! ")
                new_position = input(f"[{turn()}] Select: ")
                select(new_position)
            else:
                legal_moves = tuple(my_board.check_pos_moves(position))
                if not legal_moves:  # die Figur hat keine legalen moves (a1)
                    print("[T] That piece has no legal moves")
                    new_position = input(f"[{turn()}] Select: ")
                    select(new_position)
                else:
                    r = my_output(legal_moves[0])
                    my_legal_moves = list(legal_moves)
                    del my_legal_moves[0]
                    i = -1
                    for p in my_legal_moves:
                        i += 1
                        r = r + " and " + str(my_output(p))
                    r = r.replace(" and ", " ,", i)
                    print(f"[T] Your legal moves are {r}")
                    move = input(f"[{turn()}] Move: ")
                    move = int(my_input(move))
                    movement(position, move, legal_moves)
    else:
        if "to" in position:  # es wurde eine Angabe in Form von "pos to move" gemacht (e2 to e4)
            position = position.replace(" ", "")
            my_position, move = position.split("to")
            position = int(my_input(my_position))
            if position == 69:  # die Position ist falsch geschrieben (x9)
                print("[T] That's not a square")
                new_position = input(f"[{turn()}] Select: ")
                select(new_position)
            else:
                figur = my_board.return_figur(position)
                if figur == 0 or figur == 13:  # auf der Position ist keine Figur (20)
                    print("[T] You wanna play with air? ")
                    new_position = input(f"[{turn()}] Select: ")
                    select(new_position)

                elif figur % 2 != my_board.movecount % 2:
                    print("[T] You must select one of your own pieces! ")
                    new_position = input(f"[{turn()}] Select: ")
                    select(new_position)
                else:
                    legal_moves = my_board.check_pos_moves(position)
                    if not legal_moves:  # die Figur hat keine legalen moves (a1)
                        print("[T] That piece has no legal moves")
                        new_position = input(f"[{turn()}] Select: ")
                        select(new_position)
                    else:
                        move = int(my_input(move))
                        movement(position, move, legal_moves)
        elif position.lower() == "back":
            my_board.reverse_move()
        else:
            print("[T] That's not a square")
            new_position = input(f"[{turn()}] Select: ")
            select(new_position)


def start_normal_game():
    print('''A Chess Game by David Walk and Jan Grüninger
    Have Fun!!!
    ''')


    while True:  # start
        term_render()
        checkmate_type = my_board.check_all()
        match checkmate_type:
            case 0:  # no checkmate
                pass
            case 1:  # check because of fifty move rule
                print('Remis: Fifty move rule.')
                break
            case 2:
                print('Remis: Repeated position.')
                break
            case 4:
                print('Remis: Stalemate.')
                break
            case 3:
                print('Checkmate. Congratulations!')
                break


        pos = input(f"[{turn()}] Select: ")
        if pos == "render":
            pass
        else:
            select(pos)

start_normal_game()

