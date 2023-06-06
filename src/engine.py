def is_black(piece_num):
    if piece_num % 2 == 0 and piece_num != 0 and piece_num != 13:
        return True
    else:
        return False


def is_white(piece_num):
    if piece_num == 13 or piece_num % 2 == 0 or piece_num == 0:
        return False
    else:
        return True


def material(board):
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
            return 101
    return ret


standartborad = (
    13, 8, 4, 6, 10, 12, 6, 4, 8, 13,
    13, 2, 2, 2, 2, 2, 2, 2, 2, 13,
    13, 0, 0, 0, 0, 0, 0, 0, 0, 13,
    13, 0, 0, 0, 0, 0, 0, 0, 0, 13,
    13, 0, 0, 0, 0, 0, 0, 0, 0, 13,
    13, 0, 0, 0, 0, 0, 0, 0, 0, 13,
    13, 1, 1, 1, 1, 1, 1, 1, 1, 13,
    13, 7, 3, 5, 9, 11, 5, 3, 7, 13,
)


class Chessboard:

    # Do do: Enpasent, Casteln, Queen repairer
    def __init__(self, my_board=standartborad):

        self.board = list(my_board)     # board infos
        self.white_king_moved = True
        self.black_king_moved = True
        self.white_rrook_moved = True
        self.white_lrook_moved = True
        self.black_rrook_moved = True
        self.black_lrook_moved = True

        self.speicher = []

        self.stat_check = 0
        self.material = material(self.board)

        self.black_king_pos = 5
        self.white_king_pos = 75


        self.movecount = 1

    def isnt_samecolor(self, piece_num, other_piece_num):   # gib zwei Felder & wenn !gleichfarbige Figuren return "True"
        if self.return_figur(other_piece_num) != 13 and self.return_figur(other_piece_num) != 0:
            if self.return_figur(piece_num) % 2 != self.return_figur(other_piece_num) % 2:
                return True
            else:
                return False
        else:
            return False

    def rocharden_check(self, pos):    # änder Werte falls nötig
        if pos == 1:
            self.black_lrook_moved = False
        elif pos == 8:
            self.black_rrook_moved = False
        elif pos == 5:
            self.black_king_moved = False
        elif pos == 71:
            self.white_lrook_moved = False
        elif pos == 78:
            self.white_rrook_moved = False
        elif pos == 75:
            self.white_king_moved = False
        else:
            pass

    def return_figur(self, pos, my_board=()):
        if not my_board:
            my_board = self.board
        if 0 <= pos <= 79:
            return my_board[pos]
        else:
            return 13

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

            if not ret:  # pwan
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

    def move(self, pos, new_pos):
        self.movecount += 1  # movecount erhöhen
        taken = self.return_figur(new_pos)  # figur auf dem Feld das betreten wurde

        self.board[new_pos] = self.board[pos]  # neue Feld ist gleich der Figur
        self.board[pos] = 0  # Feld der Figur ist jetzt frei(=0)

        self.rocharden_check(pos)  # sollte ein Rook oder ein King bewegt worden sein wird es gespeichert

        if pos == self.white_king_pos:
            self.white_king_pos = new_pos   # um leichter nach checks zu suchen wird die pos des Kings gespeichert
        if pos == self.black_king_pos:
            self.black_king_pos = new_pos

        if self.check_search(self.black_king_pos, False):
            self.stat_check = 1   # Black in check
        elif self.check_search(self.white_king_pos, True):
            self.stat_check = 2    # White in check
        else:
            self.stat_check = 0

        if taken != 0:
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
        else:
            taken = 0

            # datei = pos, new_pos, taken, castlen_white, castlen_black
            # rocharde:
            #    0 = niemand
            #    1 = nur rechts
            #    2 = nur links
            #    3 = alle

        move_datei = [pos, new_pos, taken]
        white_cas = 0
        if self.white_king_moved:
            if self.white_rrook_moved and self.white_lrook_moved:
                white_cas = 3
            elif self.white_rrook_moved:
                white_cas = 1
            elif self.white_lrook_moved:
                white_cas = 2
        black_cas = 0
        if self.black_king_moved:
            if self.black_rrook_moved and self.black_lrook_moved:
                black_cas = 3
            elif self.black_rrook_moved:
                white_cas = 1
            elif self.black_lrook_moved:
                white_cas = 2
        if white_cas or black_cas:
            move_datei.append(white_cas)
            move_datei.append(black_cas)

        self.speicher.append(move_datei)


    def reverse_move(self,my_board=()):
        if not my_board:
            my_board = self.board
        datei = self.speicher.pop(self.movecount - 2)
        w_cas = 0
        b_cas = 0
        if len(datei) == 3:
            old_pos, now_pos, taken = datei
        else:
            old_pos, now_pos, taken, w_cas, b_cas = datei
        self.movecount -= 1  # movecount verringert

        if w_cas:
            self.white_king_moved = True
            if w_cas == 1:
                self.white_rrook_moved = True
                self.white_lrook_moved = False
            elif w_cas == 2:
                self.white_rrook_moved = False
                self.white_lrook_moved = True
            elif w_cas == 3:
                self.white_rrook_moved = True
                self.white_lrook_moved = True
            else:
                print("Fehler 354")
        else:
            self.white_king_moved = False
            self.white_rrook_moved = False
            self.white_lrook_moved = False

        if b_cas:
            self.black_king_moved = True
            if b_cas == 1:
                self.black_rrook_moved = True
                self.black_lrook_moved = False
            elif b_cas == 2:
                self.black_rrook_moved = False
                self.black_lrook_moved = True
            elif b_cas == 3:
                self.black_rrook_moved = True
                self.black_lrook_moved = True
            else:
                print("Fehler 353")
        else:
            self.black_king_moved = False
            self.black_rrook_moved = False
            self.black_lrook_moved = False

        my_board[old_pos] = my_board[now_pos]  # altes Feld ist gleich der Figur
        my_board[now_pos] = taken

        if taken != 0:
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

        if self.check_search(self.black_king_pos, False):
            self.stat_check = 1
        elif self.check_search(self.white_king_pos, True):
            self.stat_check = 2
        else:
            self.stat_check = 0
            # mögliche Problemstelle

    def check_pos_moves(self, pos):
        piece_num = self.return_figur(pos)
        ret = []
        if piece_num == 0:  # moves für keine Figur
            pass
        elif piece_num == 1:  # moves für w.Bauer
            if self.return_figur(pos - 10) == 0:  # checkt 1 Feld davor
                ret.append((pos - 10))

                if self.return_figur(pos - 20) == 0 and 60 <= pos <= 69:  # checkt 2 Felder davor
                    ret.append((pos - 20))

            if is_black(self.return_figur(pos - 9)):  # checkt Feld rechts vorne auf Gegner
                ret.append((pos - 9))

            if is_black(self.return_figur(pos - 11)):  # checkt Feld links vorne auf Gegner
                ret.append((pos - 11))

        elif piece_num == 2:  # moves für b.Bauer
            if self.return_figur(pos + 10) == 0:  # checkt 1 Feld davor
                ret.append((pos + 10))

                if self.return_figur(pos + 20) == 0 and 10 <= pos <= 19:  # checkt 2 Felder davor
                    ret.append((pos + 20))

            if is_white(self.return_figur(pos + 9)):  # checkt Feld rechts vorne auf Gegner
                ret.append((pos + 9))

            if is_white(self.return_figur(pos + 11)):  # checkt Feld links vorne auf Gegner
                ret.append((pos + 11))

        elif piece_num == 3 or piece_num == 4:  # moves für knights

            for i in [-21, -19, -12, -8, 8, 12, 19, 21]:
                new_pos = pos

                new_pos += i
                if self.return_figur(new_pos) == 0 or self.isnt_samecolor(pos, new_pos):
                    ret.append(new_pos)

        elif piece_num == 5 or piece_num == 6:  # moves for bishop

            for i in [-11, -9, 9, 11]:
                new_pos = pos + i
                while self.return_figur(new_pos) == 0:
                    ret.append(new_pos)
                    new_pos += i
                if self.isnt_samecolor(pos, new_pos):
                    ret.append(new_pos)

        elif piece_num == 7 or piece_num == 8:  # moves for rook

            for i in [-10, -1, 1, 10]:
                new_pos = pos + i
                while self.return_figur(new_pos) == 0:
                    ret.append(new_pos)
                    new_pos += i
                if self.isnt_samecolor(pos, new_pos):
                    ret.append(new_pos)

        elif piece_num == 9 or piece_num == 10:  # moves for queens (rook + bishop)
            for i in [-10, -1, 1, 10]:  # rook moves copied
                new_pos = pos + i
                while self.return_figur(new_pos) == 0:
                    ret.append(new_pos)
                    new_pos += i
                if self.isnt_samecolor(pos, new_pos):
                    ret.append(new_pos)

            for i in [-11, -9, 9, 11]:
                new_pos = pos + i
                while self.return_figur(new_pos) == 0:
                    ret.append(new_pos)
                    new_pos += i
                if self.isnt_samecolor(pos, new_pos):
                    ret.append(new_pos)

        elif piece_num == 11:  # moves for the white king
            for i in [1, 9, 10, 11, -11, -10, -9, -1]:
                new_pos = pos + i
                if self.return_figur(new_pos) == 0 or self.isnt_samecolor(self.return_figur(pos),
                                                                          self.return_figur(new_pos)):
                    ret.append(new_pos)

            if self.white_king_moved and self.stat_check == 0:  # castlen
                if self.white_rrook_moved and self.return_figur(76) + self.return_figur(77) == 0:
                    if not self.check_search(76, True) and not self.check_search(77, True):
                        ret.append(77)
                if self.white_lrook_moved and self.return_figur(74) + self.return_figur(73) + self.return_figur(
                        72) == 0:
                    if not self.check_search(72, True) and not self.check_search(73, True) and not self.check_search(74, True):
                        ret.append(73)

        elif piece_num == 12:  # moves for the black king
            for i in [1, 9, 10, 11, -11, -10, -9, -1]:
                new_pos = pos + i
                if self.return_figur(new_pos) == 0 or self.isnt_samecolor(self.return_figur(pos),
                                                                          self.return_figur(new_pos)):
                    ret.append(new_pos)

        else:
            pass

        if self.movecount%2 == 0:  # nur moves die Check stoppen
            new_ret = []
            for i in ret:
                self.move(pos, i)
                if self.stat_check != 1:
                    new_ret.append(i)
                self.reverse_move()
            ret = new_ret

        else:
            new_ret = []
            for i in ret:
                self.move(pos, i)
                if self.stat_check != 2:
                    new_ret.append(i)
                self.reverse_move()
            ret = new_ret
        return ret

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
        return(ret)
