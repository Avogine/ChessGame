# static functions:
def material(board):  # gibt den aktuellen Materialwert (Weis als + und Schwarz als - int)
    ret = 0
    for i in board:
        if i == 0 or i == 13 or i == 11 or i == 12:
            pass
        elif i == 1:
            ret += 1
        elif i == 2:
            ret -= 1
        elif i == 3 or i == 5:
            ret += 3
        elif i == 4 or i == 6:
            ret -= 3
        elif i == 7:
            ret += 5
        elif i == 8:
            ret -= 5
        elif i == 9:
            ret += 9
        elif i == 10:
            ret -= 9
        else:
            print("Fehler 542")
    return ret


def my_output(inp):  # konvertiert int zu schachsprache
    x = inp % 10
    y = (inp - x) / 10
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


def is_black(piece):
    if piece % 2 == 0 and piece != 0 and piece != 13:
        return True
    else:
        return False


def is_white(piece):
    if piece == 13 or piece % 2 == 0 or piece == 0:
        return False
    else:
        return True


def con_Table(fen):   # r1bqkbnr/ppp2ppp/2np4/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 1
    if fen == "":
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"

    board, turn, cas, enpassant, fif, count = fen.split(" ")

    wkc = False
    wqc = False
    bkc = False
    bqc = False
    my_board = [13]
    for i in list(board):
        if i == "/":
            my_board.append(13)
            my_board.append(13)
        elif i == "P":
            my_board.append(1)
        elif i == "p":
            my_board.append(2)
        elif i == "N":
            my_board.append(3)
        elif i == "n":
            my_board.append(4)
        elif i == "B":
            my_board.append(5)
        elif i == "b":
            my_board.append(6)
        elif i == "R":
            my_board.append(7)
        elif i == "r":
            my_board.append(8)
        elif i == "Q":
            my_board.append(9)
        elif i == "q":
            my_board.append(10)
        elif i == "K":
            my_board.append(11)
        elif i == "k":
            my_board.append(12)
        else:
            for r in range(int(i)):
                my_board.append(0)
    my_board.append(13)
    if cas != "-":
        for i in tuple(cas):
            if i == "K":
                wkc = True
            elif i == "Q":
                wqc = True
            elif i == "k":
                bkc = True
            elif i == "q":
                bqc = True
    if enpassant == "-":
        enpassant = 0
    else:
        enpassant = my_input(enpassant)
    return list(my_board), turn, wkc, wqc, bkc, bqc, enpassant, int(fif), int(count)

# static variables:

standartborad = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"

# piece types: pawn knight bishop rook queen king
# white:       1    3      5      7    9     11
# black:       2    4      6      8    10    12
# 13: invalid/ wall

# TODO: enpassent, remis,
class Chessboard:

    def __init__(self, my_board=standartborad):
        self.board, turn, self.w_castle_King, self.w_castle_Queen, self.b_castle_King, self.b_castle_Queen, self.enpassant, self.fifty_move_rule, self.movecount = con_Table(my_board)  # board infos
        self.movecount += 1
        self.speicher = []  # Speicher Züge für def reverse_move()
        self.board_speicher = []  # Speicher gesamtes Spielfeld als FEN falls es sich 3 mal wiederholt

        self.stat_check = 0
        self.material = material(self.board)

        self.black_king_pos = 5  # traced die Position des Kings um leichter nach Checks zu suchen
        self.white_king_pos = 75  # wird in move geändert

    # Hilfsmethoden
    def return_figur(self, pos, my_board=()):
        if not my_board:
            my_board = self.board
        if 0 <= pos <= 79:
            return my_board[pos]
        else:
            return 13

    def not_same_colour(self, piece, other_piece):  # gib zwei Felder & wenn !gleichfarbige Figuren return "True"
        if self.return_figur(other_piece) != 13 and self.return_figur(other_piece) != 0:
            if self.return_figur(piece) % 2 != self.return_figur(other_piece) % 2:
                return True
            else:
                return False
        else:
            return False

    def check_search(self, pos, color, my_board=()):
        ret = False
        if not my_board:
            my_board = self.board
        if color:  # white king
            for i in [-11, -9, 9, 11]:  # bishop
                new_pos = pos + i
                while self.return_figur(new_pos, my_board) == 0:
                    new_pos += i
                if self.return_figur(new_pos, my_board) == 6 or self.return_figur(new_pos, my_board) == 10:
                    ret = True

            if not ret:  # knight
                for i in [-21, -19, -12, -8, 8, 12, 19, 21]:
                    new_pos = pos + i
                    if self.return_figur(new_pos, my_board) == 4:
                        ret = True

            if not ret:  # rook
                for i in [-10, -1, 1, 10]:
                    new_pos = pos + i
                    while self.return_figur(new_pos, my_board) == 0:
                        new_pos += i
                    if self.return_figur(new_pos, my_board) == 8 or self.return_figur(new_pos, my_board) == 10:
                        ret = True

            if not ret:  # pawn
                if self.return_figur(pos - 9, my_board) == 2 or self.return_figur(pos - 11, my_board) == 2:
                    ret = True
        else:
            for i in [-11, -9, 9, 11]:  # bishop
                new_pos = pos + i
                while self.return_figur(new_pos, my_board) == 0:
                    new_pos += i
                if self.return_figur(new_pos, my_board) == 5 or self.return_figur(new_pos, my_board) == 9:
                    ret = True

            if not ret:  # knight
                for i in [-21, -19, -12, -8, 8, 12, 19, 21]:
                    new_pos = pos + i
                    if self.return_figur(new_pos, my_board) == 3:
                        ret = True

            if not ret:  # rook
                for i in [-10, -1, 1, 10]:
                    new_pos = pos + i
                    while self.return_figur(new_pos, my_board) == 0:
                        new_pos += i
                    if self.return_figur(new_pos, my_board) == 7 or self.return_figur(new_pos, my_board) == 9:
                        ret = True

            if not ret:  # pawn
                if self.return_figur(pos + 9, my_board) == 1 or self.return_figur(pos + 11, my_board) == 1:
                    ret = True

        return ret

    def conv_to_FEN(self):
        output = ""
        x = 0
        for i in self.board:  # konvertiert das Feld
            if i == 0:
                x += 1
            elif i == 1:
                if x > 0:
                    output += str(x)
                    x = 0
                output += "P"
            elif i == 2:
                if x > 0:
                    output += str(x)
                    x = 0
                output += "p"
            elif i == 3:
                if x > 0:
                    output += str(x)
                    x = 0
                output += "N"
            elif i == 4:
                if x > 0:
                    output += str(x)
                    x = 0
                output += "n"
            elif i == 5:
                if x > 0:
                    output += str(x)
                    x = 0
                output += "B"
            elif i == 6:
                if x > 0:
                    output += str(x)
                    x = 0
                output += "b"
            elif i == 7:
                if x > 0:
                    output += str(x)
                    x = 0
                output += "R"

            elif i == 8:
                if x > 0:
                    output += str(x)
                    x = 0
                output += "r"
            elif i == 9:
                if x > 0:
                    output += str(x)
                    x = 0
                output += "Q"
            elif i == 10:
                if x > 0:
                    output += str(x)
                    x = 0
                output += "q"
            elif i == 11:
                if x > 0:
                    output += str(x)
                    x = 0
                output += "K"
            elif i == 12:
                if x > 0:
                    output += str(x)
                    x = 0
                output += "k"
            elif i == 13:
                if x > 0:
                    output += str(x)
                    x = 0
                output += "/"
        output = output.replace("//", "/")
        v = len(output) - 1
        output = output[1:v]
        # Zusatz Informationen
        if self.movecount % 2 == 0:  # welcher Spieler an der Reihe ist
            output += " b "
        else:
            output += " w "

        cas = ""  # ob jmd castlen kann
        if self.w_castle_King:
            cas += "K"
        if self.w_castle_Queen:
            cas += "Q"
        if self.b_castle_King:
            cas += "k"
        if self.b_castle_Queen:
            cas += "q"
        if not cas:
            cas += "-"
        output += cas

        if self.enpassant:  # mögliche enpassents
            output += f" {my_output(self.enpassant)} "
        else:
            output += " - "
        output += f"{str(self.fifty_move_rule)} {str(self.movecount - 1)}"
        return output

    def castle_check(self, pos):  # änder Werte falls nötig
        if pos == 1:
            self.b_castle_Queen = False
        elif pos == 8:
            self.b_castle_King = False
        elif pos == 5:
            self.b_castle_King = False
            self.b_castle_Queen = False
        elif pos == 71:
            self.w_castle_Queen = False
        elif pos == 78:
            self.w_castle_King = False
        elif pos == 75:
            self.w_castle_King = False
            self.w_castle_Queen = False

    def all_moves(self):
        ret = []
        for i in range(80):
            if 0 < self.return_figur(i) < 13:
                if self.return_figur(i) % 2 == self.movecount % 2:
                    d = self.check_pos_moves(i)
                    if d:
                        for m in d:
                            ret.append(m)
            else:
                pass
        return (ret)

    # Methoden

    def check_all(self):
        if self.fifty_move_rule == 50:
            return 1  # remis wegen 50-Move Rule
        elif self.board in self.board_speicher:
            i = 0
            for x in self.board_speicher:
                if self.board == x:
                    i += 1
            if i >= 2:
                return 2  # remis wegen wiederholter Stellung
        elif not self.all_moves:
            if self.stat_check:
                return 3  # remis wegen Stealmate
            else:
                return 4  # Checkmate
        else:
            return 0

    # TODO: Checkmat erkennen

    def move(self, pos, new_pos):
        self.enpassant = 0
        taken = self.return_figur(new_pos)  # figur auf dem Feld das betreten wurde

        con_board = self.conv_to_FEN()
        self.board_speicher.append(con_board)
        # FIXME: der letzte Teil der FEN muss abgeschitten werden da der movcount und die fifty move. immer geändert werden

        self.fifty_move_rule += 1
        self.movecount += 1  # move-count erhöhen

        if self.return_figur(pos) == 1 or self.return_figur(pos) == 2:  # wenn die bewegte Figur ein Bauer ist
            self.fifty_move_rule = 0  # die Variable für die Fifty Move Rule wird zurückgesetzt
            self.board_speicher.clear()
            if (10 < pos < 19 and 30 < new_pos < 39) or (60 < pos < 69 and 40 < new_pos < 49):
                self.enpassant = new_pos  # mögliche enpassents
        elif self.return_figur(pos) == 11:  # wenn die bewegte Figur der weiße König ist
            self.white_king_pos = new_pos  # die Position des Königs wird gespeichert
        elif self.return_figur(pos) == 12:  # wenn die bewegte Figur der schwarze König ist
            self.black_king_pos = new_pos

        self.board[new_pos] = self.board[pos]  # neue Feld ist gleich der Figur
        self.board[pos] = 0  # Feld der Figur ist jetzt frei(=0)

        if self.check_search(self.black_king_pos, False):
            self.stat_check = 1  # Black in check

        elif self.check_search(self.white_king_pos, True):
            self.stat_check = 2  # White in check

        else:
            self.stat_check = 0


        if pos == 75 and (new_pos == 77):
            self.board[76] = 7  # neue Feld ist gleich der Figur
            self.board[78] = 0
        elif pos == 75 and (new_pos == 73):
            self.board[74] = 7
            self.board[71] = 0
        elif pos == 5 and (new_pos == 7):
            self.board[6] = 8  # neue Feld ist gleich der Figur
            self.board[8] = 0
        elif pos == 5 and (new_pos == 3):
            self.board[4] = 8
            self.board[1] = 0

        if taken != 0:
            self.fifty_move_rule = 0
            self.board_speicher.clear()
            if taken == 1:
                self.material -= 1
            elif taken == 2:
                self.material += 1
            elif taken == 3:
                self.material -= 3
            elif taken == 4:
                self.material += 3
            elif taken == 5:
                self.material -= 3
            elif taken == 6:
                self.material += 3
            elif taken == 7:
                self.material -= 5
            elif taken == 8:
                self.material += 5
            elif taken == 9:
                self.material -= 9
            elif taken == 10:
                self.material += 9

            # datei = pos, new_pos, taken, castlen_white, castlen_black
            # rocharde:
            #    0 = niemand
            #    1 = nur rechts
            #    2 = nur links
            #    3 = alle

        white_cas = 0
        if self.w_castle_King and self.w_castle_Queen:
            white_cas = 3
        elif self.w_castle_King:
            white_cas = 1
        elif self.w_castle_Queen:
            white_cas = 2

        black_cas = 0
        if self.b_castle_King and self.b_castle_Queen:
            black_cas = 3
        elif self.b_castle_King:
            white_cas = 1
        elif self.b_castle_Queen:
            white_cas = 2
        if white_cas or black_cas:
            move_datei = (pos, new_pos, taken, white_cas, black_cas)
        else:
            move_datei = (pos, new_pos, taken)

        self.speicher.append(move_datei)

        self.castle_check(pos)  # sollte ein Rook oder ein King bewegt worden sein wird es gespeichert

    def reverse_move(self, my_board=()):
        if not my_board:
            my_board = self.board
        if not self.speicher:
            pass
        else:
            if self.board_speicher:
                del self.board_speicher[len(self.board_speicher) - 1]
            if self.fifty_move_rule:
                self.fifty_move_rule -= 1

            datei = self.speicher.pop(len(self.speicher) - 1)
            w_cas = 0
            b_cas = 0
            if len(datei) == 3:
                old_pos, now_pos, taken = datei
            else:
                old_pos, now_pos, taken, w_cas, b_cas = datei

            self.movecount -= 1  # movecount verringert
            if w_cas:  # ändert die castle Variablen
                if w_cas == 1:
                    self.w_castle_King = True
                    self.w_castle_Queen = False
                elif w_cas == 2:
                    self.w_castle_Queen = True
                    self.w_castle_King = False
                elif w_cas == 3:
                    self.w_castle_King = True
                    self.w_castle_Queen = True
                else:
                    print("Fehler 354")
            else:
                self.w_castle_Queen = False
                self.w_castle_King = False
            if b_cas:
                if b_cas == 1:
                    self.b_castle_King = True
                    self.b_castle_Queen = False
                elif b_cas == 2:
                    self.b_castle_King = False
                    self.b_castle_Queen = True
                elif b_cas == 3:
                    self.b_castle_King = True
                    self.b_castle_Queen = True
                else:
                    print("Fehler 353")
            else:
                self.b_castle_Queen = False
                self.b_castle_King = False

            if taken != 0:  # material wird zurückgesetzt
                if taken == 1:
                    self.material += 1
                elif taken == 2:
                    self.material -= 1
                elif taken == 3:
                    self.material += 3
                elif taken == 4:
                    self.material -= 3
                elif taken == 5:
                    self.material += 3
                elif taken == 6:
                    self.material -= 3
                elif taken == 7:
                    self.material += 5
                elif taken == 8:
                    self.material -= 5
                elif taken == 9:
                    self.material += 9
                elif taken == 10:
                    self.material -= 9
            if now_pos == self.white_king_pos:
                self.white_king_pos = old_pos  # um leichter nach checks zu suchen wird die pos des Kings gespeichert
            if now_pos == self.black_king_pos:
                self.black_king_pos = old_pos

            if self.speicher:
                sec_datei = self.speicher[len(self.speicher) - 1]
                pre_pos = sec_datei[0]
                pre_new_pos = sec_datei[1]
                if self.return_figur(pre_new_pos) == 1 or self.return_figur(pre_new_pos) == 2:  # wenn die bewegte Figur ein Bauer ist
                    if (10 < pre_pos < 19 and 30 < pre_new_pos < 39) or (60 < pre_pos < 69 and 40 < pre_new_pos < 49):
                        self.enpassant = pre_new_pos  # mögliche enpassents

            my_board[old_pos] = my_board[now_pos]  # altes Feld ist gleich der Figur
            my_board[now_pos] = taken

            if self.check_search(self.black_king_pos, False):
                self.stat_check = 1
            elif self.check_search(self.white_king_pos, True):
                self.stat_check = 2
            else:
                self.stat_check = 0

            if old_pos == 75 and now_pos == 77:
                self.board[76] = 0  # neue Feld ist gleich der Figur
                self.board[78] = 7
            elif old_pos == 75 and now_pos == 73:
                self.board[74] = 0
                self.board[71] = 7
            elif old_pos == 5 and now_pos == 7:
                self.board[6] = 0  # neue Feld ist gleich der Figur
                self.board[8] = 8
            elif old_pos == 5 and now_pos == 3:
                self.board[4] = 0
                self.board[1] = 8

    def check_pos_moves(self, pos):
        piece = self.return_figur(pos)
        ret = []
        if piece == 0:  # moves für keine Figur
            pass
        elif piece == 1:  # moves für weißen Bauer
            if self.return_figur(pos - 10) == 0:  # checkt 1 Feld davor
                ret.append((pos - 10))

                if self.return_figur(pos - 20) == 0 and 60 <= pos <= 69:  # checkt 2 Felder davor
                    ret.append((pos - 20))

            if is_black(self.return_figur(pos - 9)):  # checkt Feld rechts vorne auf Gegner
                ret.append((pos - 9))

            if is_black(self.return_figur(pos - 11)):  # checkt Feld links vorne auf Gegner
                ret.append((pos - 11))

        elif piece == 2:  # moves für schwarzen Bauer
            if self.return_figur(pos + 10) == 0:  # checkt 1 Feld davor
                ret.append((pos + 10))

                if self.return_figur(pos + 20) == 0 and 10 <= pos <= 19:  # checkt 2 Felder davor
                    ret.append((pos + 20))

            if is_white(self.return_figur(pos + 9)):  # checkt Feld rechts vorne auf Gegner
                ret.append((pos + 9))

            if is_white(self.return_figur(pos + 11)):  # checkt Feld links vorne auf Gegner
                ret.append((pos + 11))

        elif piece == 3 or piece == 4:  # moves für knights

            for i in [-21, -19, -12, -8, 8, 12, 19, 21]:
                new_pos = pos

                new_pos += i
                if self.return_figur(new_pos) == 0 or self.not_same_colour(pos, new_pos):
                    ret.append(new_pos)

        elif piece == 5 or piece == 6:  # moves for bishop

            for i in [-11, -9, 9, 11]:
                new_pos = pos + i
                while self.return_figur(new_pos) == 0:
                    ret.append(new_pos)
                    new_pos += i
                if self.not_same_colour(pos, new_pos):
                    ret.append(new_pos)

        elif piece == 7 or piece == 8:  # moves for rook

            for i in [-10, -1, 1, 10]:
                new_pos = pos + i
                while self.return_figur(new_pos) == 0:
                    ret.append(new_pos)
                    new_pos += i
                if self.not_same_colour(pos, new_pos):
                    ret.append(new_pos)

        elif piece == 9 or piece == 10:  # moves for queens (rook + bishop)
            for i in [-10, -1, 1, 10]:  # rook moves copied
                new_pos = pos + i
                while self.return_figur(new_pos) == 0:
                    ret.append(new_pos)
                    new_pos += i
                if self.not_same_colour(pos, new_pos):
                    ret.append(new_pos)

            for i in [-11, -9, 9, 11]:
                new_pos = pos + i
                while self.return_figur(new_pos) == 0:
                    ret.append(new_pos)
                    new_pos += i
                if self.not_same_colour(pos, new_pos):
                    ret.append(new_pos)

        elif piece == 11:  # moves for the white king
            for i in [1, 9, 10, 11, -11, -10, -9, -1]:
                new_pos = pos + i
                if self.return_figur(new_pos) == 0 or is_white(self.return_figur(new_pos)):
                    ret.append(new_pos)

            if self.stat_check != 2:  # castlen
                if self.w_castle_King and self.return_figur(76) + self.return_figur(77) == 0:
                    if not self.check_search(76, True) and not self.check_search(77, True):
                        ret.append(77)
                if self.w_castle_Queen and self.return_figur(74) + self.return_figur(73) + self.return_figur(
                        72) == 0:
                    if not self.check_search(72, True) and not self.check_search(73, True) and not self.check_search(74,
                                                                                                                     True):
                        ret.append(73)

        elif piece == 12:  # moves for the black king
            for i in [1, 9, 10, 11, -11, -10, -9, -1]:
                new_pos = pos + i
                if self.return_figur(new_pos) == 0 or is_white(self.return_figur(new_pos)):
                    ret.append(new_pos)

            if self.stat_check != 1:  # castlen
                if self.b_castle_King and self.return_figur(6) + self.return_figur(7) == 0:
                    if not self.check_search(6, False) and not self.check_search(77, False):
                        ret.append(7)
                if self.b_castle_Queen and self.return_figur(4) + self.return_figur(3) + self.return_figur(
                        2) == 0:
                    if not self.check_search(2, False) and not self.check_search(3, False) and not self.check_search(4,
                                                                                                                     False):
                        ret.append(3)

        else:
            print("Fehler 274")

        return (self.leagl_moves(pos, ret))
    def leagl_moves(self, pos, moves):
        if self.return_figur(pos) % 2 == 0:  # nur moves die Check stoppen
            ret = []
            for i in moves:
                self.move(pos, i)
                if self.stat_check != 1:
                    ret.append(i)

                self.reverse_move()

        else:
            ret = []
            for i in moves:
                self.move(pos, i)
                if self.stat_check != 2:
                    ret.append(i)
                self.reverse_move()

        return ret

    def info(self):
        print(f"""
        {self.board}
        {self.w_castle_King}
        {self.w_castle_Queen}
        {self.b_castle_King}
        {self.b_castle_Queen }
        {self.fifty_move_rule}
        {self.enpassant}
        {self.movecount}
        {self.speicher}  
        {self.board_speicher}  
        {self.stat_check}
        {self.material}
        {self.black_king_pos}  
        {self.white_king_pos}"""  )