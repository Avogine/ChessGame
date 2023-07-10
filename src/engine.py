from stockfish import Stockfish
import helpers


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

standartboard = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"


# piece types: pawn knight bishop rook queen king
# white:       1    3      5      7    9     11
# black:       2    4      6      8    10    12
# 13: invalid/ wall

# TODO: remis, promotion
class Chessboard:

    def __init__(self, my_board=standartboard):
        self.board, turn, self.w_castle_King, self.w_castle_Queen, self.b_castle_King, self.b_castle_Queen, self.enpassant, self.fifty_move_rule, self.movecount = con_Table(my_board)  # board infos
        self.movecount += 1
        self.speicher = []  # Speicher Züge für def reverse_move()
        self.board_speicher = []  # Speicher gesamtes Spielfeld als FEN falls es sich 3 mal wiederholt
        self.stockfish = Stockfish(helpers.get_stockfish_path())
        self.w_check = False
        self.b_check = False
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

        if self.enpassant: # mögliche enpassents
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
        elif not self.all_moves():
            if self.w_check or self.b_check:
                return 3  # Checkmate
            else:
                return 4  # remis wegen Stealmate

        elif self.board in self.board_speicher:
            i = 0
            for x in self.board_speicher:
                if self.board == x:
                    i += 1
            if i >= 2:
                return 2  # remis wegen wiederholter Stellung
            else:
                return 0
        else:
            return 0



    def move(self, pos, new_pos):
        kind = 0
        #new_pos = int(new_pos)
        # first status change
        save_enpassant = self.enpassant
        self.enpassant = 0
        self.fifty_move_rule += 1

        # kind of move
        if self.return_figur(pos) == 1 or self.return_figur(pos) == 2:  # Pawn
            self.fifty_move_rule = 0
            self.board_speicher.clear()

            if int(new_pos/10) == 0 or int(new_pos/10) == 7:   # promotion
                kind = 1
            elif new_pos == save_enpassant:   # enpassant
                kind = 2
                if pos > new_pos:   # white
                    self.board[new_pos + 10] = 0
                else:   # black
                    self.board[new_pos - 10] = 0
            elif (int(new_pos/10) == 3 and int(pos/10) == 1) or (int(new_pos/10) == 4 and int(pos/10) == 6):
                self.enpassant = int((new_pos + pos)/2)


        elif self.return_figur(pos) == 11:  # white king
            self.white_king_pos = new_pos  # save king position

            if pos == 75 and (new_pos == 77 or new_pos == 78): # castle
                new_pos = 77
                self.board[76] = 7
                self.board[78] = 0
                kind = 3
            elif pos == 75 and (new_pos == 73 or new_pos == 72 or new_pos == 71):
                new_pos = 73
                self.board[74] = 7
                self.board[71] = 0
                kind = 3

        elif self.return_figur(pos) == 12:  # black king
            self.black_king_pos = new_pos

            if pos == 5 and (new_pos == 7 or new_pos == 8):   # castle
                new_pos = 7
                self.board[6] = 8
                self.board[8] = 0
                kind = 3
            elif pos == 5 and (new_pos == 3 or new_pos == 2 or new_pos == 1):
                new_pos = 3
                self.board[4] = 8
                self.board[1] = 0
                kind = 3



        # make move

        taken = self.return_figur(new_pos)  # figur that was taken
        self.board[new_pos] = self.board[pos]  # new place = figur
        self.board[pos] = 0  # old pace is free ( =0 )



        # save move

        # datei = pos, new_pos, taken, castlen_white, castlen_black
        # castlen:
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
            move_datei = [pos, new_pos, taken, white_cas, black_cas]
        else:
            move_datei = [pos, new_pos, taken]
        if save_enpassant and not self.speicher:
            move_datei.append(save_enpassant)
        elif kind == 1:
            move_datei.append(420)
        self.speicher.append(tuple(move_datei))


        # sec status-change


        self.movecount += 1
        self.material = material(self.board)
        if taken:
            self.board_speicher.clear()
            self.fifty_move_rule = 0

        if self.check_search(self.black_king_pos, False):
            self.b_check = True  # Black in check
        elif self.check_search(self.white_king_pos, True):
            self.w_check = True  # White in check
        else:
            self.w_check = False
            self.b_check = False

        self.castle_check(pos)

        # save board
        con_board = self.conv_to_FEN()
        con_board = con_board.split(" ")[0]
        self.board_speicher.append(con_board)
        return(kind)

    def reverse_move(self, my_board=()):
        if not my_board:
            my_board = self.board
        if self.speicher:
            # get save
            datei = self.speicher.pop(len(self.speicher) - 1)   # last saved data get extracted
            w_cas = 0
            b_cas = 0
            enp = 0
            b = 0
            prom = 0
            if len(datei) % 2 == 0:
                datei = list(datei)
                b = datei.pop(len(datei) - 1)
                datei = tuple(datei)

            if len(datei) == 3:
                before_pos, now_pos, taken = datei
            else:
                before_pos, now_pos, taken, w_cas, b_cas = datei

            if b != 420: # if the last move was a promotion
                enp = b
                b = 0
            else:
                if int(now_pos/10) == 0:
                    prom = 1
                elif int(now_pos/10) == 7:
                    prom = 2

            # kind of last move
            if self.return_figur(now_pos) == 1:
                if taken == 0 and now_pos % 10 != before_pos % 10:   # last move was an enpassant
                    self.board[now_pos + 10] = 2
            elif self.return_figur(now_pos) == 2:
                if taken == 0 and now_pos % 10 != before_pos % 10:
                    self.board[now_pos - 10] = 1

            if before_pos == 75 and now_pos == 77:   # last move was castle
                self.board[76] = 0  # neue Feld ist gleich der Figur
                self.board[78] = 7
            elif before_pos == 75 and now_pos == 73:
                self.board[74] = 0
                self.board[71] = 7
            elif before_pos == 5 and now_pos == 7:
                self.board[6] = 0  # neue Feld ist gleich der Figur
                self.board[8] = 8
            elif before_pos == 5 and now_pos == 3:
                self.board[4] = 0
                self.board[1] = 8

            # return move
            self.board[before_pos] = self.board[now_pos]
            self.board[now_pos] = taken
            if prom:
                self.board[before_pos] = prom

            # search for enpassant, must be after return move cause the enp pawn could be moved
            self.enpassant = enp
            if self.speicher:   # search for enpassant by looking at the move before
                sec_datei = self.speicher[len(self.speicher) - 1]
                sbefore_pos = sec_datei[1]
                latest_pos = sec_datei[0]
                if self.return_figur(sbefore_pos) == 1 or self.return_figur(sbefore_pos) == 2:  # search for enpassant
                    if (10 < latest_pos < 19 and 30 < sbefore_pos < 39) or (60 < latest_pos < 69 and 40 < sbefore_pos < 49):
                        self.enpassant = int((sbefore_pos + latest_pos) / 2)  # mögliche enpassents


            # change saves
            if self.board_speicher:
                del self.board_speicher[len(self.board_speicher) - 1]
            if self.fifty_move_rule:
                self.fifty_move_rule -= 1


            # change status
            self.movecount -= 1  # movecount verringert
            self.material = material(self.board)
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

            if now_pos == self.white_king_pos:
                self.white_king_pos = before_pos  # um leichter nach checks zu suchen wird die pos des Kings gespeichert
            if now_pos == self.black_king_pos:
                self.black_king_pos = before_pos

            if self.check_search(self.black_king_pos, False):
                self.b_check = True  # Black in check
            elif self.check_search(self.white_king_pos, True):
                self.w_check = True  # White in check
            else:
                self.w_check = False
                self.b_check = False
        else:
            pass
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
            if abs(self.enpassant + 10 - pos) == 1:
                ret.append(self.enpassant)

        elif piece == 2:  # moves für schwarzen Bauer
            if self.return_figur(pos + 10) == 0:  # checkt 1 Feld davor
                ret.append((pos + 10))

                if self.return_figur(pos + 20) == 0 and 10 <= pos <= 19:  # checkt 2 Felder davor
                    ret.append((pos + 20))

            if is_white(self.return_figur(pos + 9)):  # checkt Feld rechts vorne auf Gegner
                ret.append((pos + 9))

            if is_white(self.return_figur(pos + 11)):  # checkt Feld links vorne auf Gegner
                ret.append((pos + 11))

            if abs(self.enpassant - 10 - pos) == 1:
                ret.append(self.enpassant)

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
                if self.return_figur(new_pos) == 0 or is_black(self.return_figur(new_pos)):
                    ret.append(new_pos)

            if not self.w_check:  # castlen
                if self.w_castle_King and self.return_figur(76) + self.return_figur(77) == 0:
                    if not self.check_search(76, True) and not self.check_search(77, True):
                        ret.append(77)
                        ret.append(78)
                if self.w_castle_Queen and self.return_figur(74) + self.return_figur(73) == 0:
                    if not self.check_search(72, True) and not self.check_search(73, True) and not self.check_search(74,
                                                                                                                     True):
                        ret.append(73)
                        ret.append(71)

        elif piece == 12:  # moves for the black king
            for i in [1, 9, 10, 11, -11, -10, -9, -1]:
                new_pos = pos + i
                if self.return_figur(new_pos) == 0 or is_white(self.return_figur(new_pos)):
                    ret.append(new_pos)

            if not self.b_check:  # castlen
                if self.b_castle_King and self.return_figur(6) + self.return_figur(7) == 0:
                    if not self.check_search(6, False) and not self.check_search(7, False):
                        ret.append(7)
                        ret.append(8)
                if self.b_castle_Queen and self.return_figur(4) + self.return_figur(3) == 0:
                    if not self.check_search(2, False) and not self.check_search(3, False) and not self.check_search(4,
                                                                                                                     False):
                        ret.append(3)
                        ret.append(1)
        else:
            print(f"Fehler 274"
                  f" Figure = {piece}"
                  f" Position = {pos}")
        solution = self.legal_moves(pos, ret)
        return(solution)


    def legal_moves(self, pos, moves):
        if self.return_figur(pos) % 2 == 0:  # nur moves die Check stoppen
            ret = []
            for i in moves:

                self.move(pos, i)

                if not self.b_check:
                    ret.append(i)

                self.reverse_move()

        else:
            ret = []
            for i in moves:
                self.move(pos, i)
                if not self.w_check:
                    ret.append(i)
                self.reverse_move()

        return ret
    def promotion(self, pos, figur):
        self.board[pos] = figur
        self.material = material(self.board)

    def s_move(self, pos, new_pos):
        self.move(pos, new_pos)
        movement = my_output(pos) + my_output(new_pos)
        self.stockfish.make_moves_from_current_position([movement])

    def stockfish_move(self):
        best = self.stockfish.get_best_move()
        a, b, c, d = list(best)
        pose = a + b
        move = c + d

        self.move(my_input(pose), my_input(move))
        self.stockfish.make_moves_from_current_position([pose + move])

    def s_configure(self, skill=0, elo=0, depth=0):
        if skill:
            self.stockfish.set_skill_level(int(skill))
        if elo:
            self.stockfish.set_elo_rating(int(elo))
        if depth:
            self.stockfish.set_depth(int(depth))

    def info(self):
        print(f"""
        {self.board}    board
        {self.w_castle_King}    w_castle_King
        {self.w_castle_Queen}   w_castle_Queen
        {self.b_castle_King}    b_castle_King
        {self.b_castle_Queen}  b_castle_Queen
        {self.fifty_move_rule}  fifty_move_rule
        {self.enpassant}    enpassant
        {self.movecount}    movecount
        {self.speicher}     speicher
        {self.board_speicher}   board_speicher  
        {self.w_check}   white_check
        {self.b_check}   black_check
        {self.material}   material
        {self.black_king_pos}   black_king_pos  
        {self.white_king_pos}   white_king_pos
        {self.conv_to_FEN()} FEN
"""  )