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


class Chessboard:

    # Do do: Enpasent, Casteln, Queen repairer
    def __init__(self):
        self.board = [
            13, 8, 4, 6, 10, 12, 6, 4, 8, 13,
            13, 2, 2, 2, 2, 2, 2, 2, 2, 13,
            13, 0, 0, 0, 0, 0, 0, 0, 0, 13,
            13, 0, 0, 0, 0, 0, 0, 0, 0, 13,
            13, 0, 0, 0, 0, 0, 0, 0, 0, 13,
            13, 0, 0, 0, 0, 0, 0, 0, 0, 13,
            13, 1, 1, 1, 1, 1, 1, 1, 1, 13,
            13, 7, 3, 5, 9, 11, 5, 3, 7, 13,
        ]

        self.stat_check = 0
        self.material = 0

        self.white_king_moved = True
        self.white_king_pos = 75

        self.black_king_moved = True
        self.black_king_pos = 5

        self.white_rrook_moved = True
        self.white_lrook_moved = True
        self.black_rrook_moved = True
        self.black_lrook_moved = True
        self.movecount = 1

    def isnt_samecolor(self, piece_num, other_piece_num):
        if self.return_figur(other_piece_num) != 13 and self.return_figur(other_piece_num) != 0:
            if self.return_figur(piece_num) % 2 != self.return_figur(other_piece_num) % 2:
                return True
            else:
                return False
        else:
            return False

    def rocharden_check(self, pos):
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

    def check_search(self, pos, color):
        ret = False
        if color:  # white king
            for i in [-11, -9, 9, 11]:  # bishop
                new_pos = pos + i
                while self.return_figur(new_pos) == 0:
                    new_pos += i
                if self.return_figur(new_pos) == 6 or self.return_figur(new_pos) == 10:
                    ret = True

            if not ret:  # knight
                for i in [-21, -19, -12, -8, 8, 12, 19, 21]:
                    new_pos = pos + i
                    if self.return_figur(new_pos) == 4:
                        ret = True

            if not ret:  # rook
                for i in [-10, -1, 1, 10]:
                    new_pos = pos + i
                    while self.return_figur(new_pos) == 0:
                        new_pos += i
                    if self.return_figur(new_pos) == 8 or self.return_figur(new_pos) == 10:
                        ret = True

            if not ret:  # pwan
                if self.return_figur(pos - 9) == 2 or self.return_figur(pos - 11) == 2:
                    ret = True
        else:
            for i in [-11, -9, 9, 11]:  # bishop
                new_pos = pos + i
                while self.return_figur(new_pos) == 0:
                    new_pos += i
                if self.return_figur(new_pos) == 5 or self.return_figur(new_pos) == 9:
                    ret = True

            if not ret:  # knight
                for i in [-21, -19, -12, -8, 8, 12, 19, 21]:
                    new_pos = pos + i
                    if self.return_figur(new_pos) == 3:
                        ret = True

            if not ret:  # rook
                for i in [-10, -1, 1, 10]:
                    new_pos = pos + i
                    while self.return_figur(new_pos) == 0:
                        new_pos += i
                    if self.return_figur(new_pos) == 7 or self.return_figur(new_pos) == 9:
                        ret = True

            if not ret:  # pwan
                if self.return_figur(pos + 9) == 1 or self.return_figur(pos + 11) == 1:
                    ret = True

        return ret

    def move(self, pos, new_pos):
        self.movecount += 1
        taken = self.return_figur(new_pos)
        self.board[new_pos] = self.board[pos]
        self.board[pos] = 0

        self.rocharden_check(pos)

        if self.movecount % 2 == 0:
            if pos == self.white_king_pos:
                self.white_king_pos = new_pos
            if self.check_search(self.black_king_pos, False):
                self.stat_check = 1
                print("[T] Black king in check")
            else:
                self.stat_check = 0
        else:
            if pos == self.black_king_pos:
                self.black_king_pos = new_pos
            if self.check_search(self.white_king_pos, True):
                self.stat_check = 2
                print(f"[T] White king in check")
            else:
                self.stat_check = 0
        if taken != 0:
            if taken == 1:
                self.material -= 1
                return "Pawn"
            elif taken == 2:
                self.material += 1
                return "Pawn"
            elif taken == 3:
                self.material -= 3
                return "Knight"
            elif taken == 4:
                self.material += 3
                return "Knight"
            elif taken == 5:
                self.material -= 3
                return "Bishop"
            elif taken == 6:
                self.material += 3
                return "Bishop"
            elif taken == 7:
                self.material -= 5
                return "Rook"
            elif taken == 8:
                self.material += 5
                return "Rook"
            elif taken == 9:
                self.material -= 9
                return "Queen"
            elif taken == 10:
                self.material += 9
                return "Queen"
        else:
            return ""

    def return_figur(self, pos):
        if 0 <= pos <= 79:
            return self.board[pos]
        else:
            return 13

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

            if self.white_king_moved:  # rocharde
                if self.white_rrook_moved and self.return_figur(76) + self.return_figur(77) == 0:
                    ret.append(78)
                if self.white_lrook_moved and self.return_figur(74) + self.return_figur(73) + self.return_figur(
                        72) == 0:
                    ret.append(71)
        elif piece_num == 12:  # moves for the black king
            for i in [1, 9, 10, 11, -11, -10, -9, -1]:
                new_pos = pos + i
                if self.return_figur(new_pos) == 0 or self.isnt_samecolor(self.return_figur(pos),
                                                                          self.return_figur(new_pos)):
                    ret.append(new_pos)

        else:
            pass
        return ret
