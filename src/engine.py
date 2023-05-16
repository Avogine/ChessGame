class Spielfeld:

    def __init__(self):
        pass

    board = [

        13, 8, 4, 6, 10, 12, 6, 4, 8, 13,
        13, 2, 2, 2, 2 , 2 , 2, 2, 2, 13,
        13, 0, 0, 0, 0 , 0 , 0, 0, 0, 13,
        13, 0, 0, 0, 0 , 0 , 0, 0, 0, 13,
        13, 0, 0, 0, 0 , 0 , 0, 0, 0, 13,
        13, 0, 0, 0, 0 , 0 , 0, 0, 0, 13,
        13, 1, 1, 1, 1 , 1 , 1, 1, 1, 13,
        13, 7, 3, 5,  9, 11, 5, 3, 7, 13,
            ]

    stat_check = False

    white_king_moved = False
    black_king_moved = False

    white_rrook_moved = False
    white_lrook_moved = False
    black_rrook_moved = False
    black_lrook_moved = False


    def is_white(self, piece_num):
        if piece_num%2 == 0:
            return(True)
        else:
            return(False)

    def is_black(self, piece_num):
        if piece_num == 13 or piece_num%2 == 0:
            return(False)
        else:
            return(True)

    def isnt_samecolor(self, piece_num, other_piece_num):
        if other_piece_num != 13:
            if piece_num%2 != other_piece_num%2:
                return(True)
        else:
            return(False)


    def return_figur(self, pos):
        if pos >= 0 and pos <= 63:
            return(self.board[pos])
        else:
            return(13)

    def rocharde(self,):
        pass

    def check_pos_moves(self,pos):
        piece_num = self.return_figur(pos)
        ret = []
        if piece_num == 0: # moves für keine Figur
            pass
        elif piece_num == 1: # moves für w.Bauer
            if self.return_figur(pos-10) == 0: # checkt 1 Feld davor
                ret.append(pos-10)

                if self.return_figur(pos - 20) == 0: # checkt 2 Felder davor
                    ret.append(pos - 20)

            if self.is_white(self.return_figur(pos - 9)): # checkt Feld rechts vorne auf Gegner
                ret.append(pos - 9)

            if self.is_white(self.return_figur(pos - 11)): # checkt Feld links vorne auf Gegner
                ret.append((pos - 11))

        elif piece_num == 2: # moves für b.Bauer
            if self.return_figur(pos + 10) == 0:  # checkt 1 Feld davor
                ret.append((pos + 10))

                if self.return_figur(pos + 20) == 0:  # checkt 2 Felder davor
                    ret.append((pos + 20))

            if self.is_white(self.return_figur(pos + 9)):  # checkt Feld rechts vorne auf Gegner
                ret.append((pos + 9))

            if self.is_white(self.return_figur(pos + 11)):  # checkt Feld links vorne auf Gegner
                ret.append((pos + 11))

        elif piece_num == 3 or piece_num == 4: # moves für knights
            for i in [-20, -19, -12, -8, 8, 12, 19, 21]:
                new_pos = pos
                new_pos = + i
                if self.return_figur(new_pos) == 0 or self.isnt_samecolor(pos, new_pos):
                    ret.append(new_pos)

        elif piece_num == 5 or piece_num == 6: # moves for bishop

            for i in [-11, -9, 9, 11]:
                new_pos = pos
                while self.return_figur(new_pos + i) == 0:
                    ret.append(new_pos + i)
                    new_pos = + i
                if self.isnt_samecolor(self.return_figur(pos), self.return_figur(new_pos + i)):
                    ret.append(new_pos + i)

        elif piece_num == 7 or piece_num == 8: # moves for rook

            for i in [-10, -1, 1, 10]:
                new_pos = pos
                while self.return_figur(new_pos + i) == 0:
                    ret.append(new_pos + i)
                    new_pos =+ i
                if self.isnt_samecolor(self.return_figur(pos),self.return_figur(new_pos+i)):
                    ret.append(new_pos + i)

        elif piece_num == 9 or piece_num == 10: # moves for queens (rook + bishop)

            for i in [-10, -1, 1, 10]: # rook moves copied
                new_pos = pos
                while self.return_figur(new_pos + i) == 0:
                    ret.append(new_pos + i)
                    new_pos =+ i
                if self.isnt_samecolor(self.return_figur(pos), self.return_figur(new_pos + i)):
                    ret.append(new_pos + i)
            for i in [-11, -9, 9, 11]:
                new_pos = pos
                while self.return_figur(new_pos + i) == 0:
                    ret.append(new_pos + i)
                    new_pos =+ i
                if self.isnt_samecolor(self.return_figur(pos), self.return_figur(new_pos + i)):
                    ret.append(new_pos + i)




        else:
            pass
        return(ret)
