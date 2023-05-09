class Spielfeld:

    def __init__(self):
        pass

    board = [
        [8, 4, 6, 10, 12, 6, 4, 8],
        [2, 2, 2, 2 , 2 , 2, 2, 2],
        [0, 0, 0, 0 , 0 , 0, 0, 0],
        [0, 0, 0, 0 , 0 , 0, 0, 0],
        [0, 0, 0, 0 , 0 , 0, 0, 0],
        [0, 0, 0, 0 , 0 , 0, 0, 0],
        [1, 1, 1, 1 , 1 , 1, 1, 1],
        [7, 3, 5,  9, 11, 5, 3, 7]
            ]

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


    def return_figur(self, x, y):
        if x >= 0 or x <= 7 or y >= 0 or y <= 7:
            return(self.board[x][y])
        else:
            return(13)
    def pos_move(self,x,y):

    def check_posmoves(self,x,y):
        piece = self.board[x][y]
        ret = []
        if piece == 0: # moves für keine Figur
            return(0)
        if piece == 1: # moves für w.Bauer
            if self.return_figur(x-1,y) == 0: # checkt 1 Feld davor
                ret.append((x-1, y))

                if self.return_figur[x-2][y] == 0: # checkt 2 Felder davor
                    ret.append((x-2, y))

            if self.is_white(self.return_figur(x-1,y+1)): # checkt Feld rechts vorne auf Gegner
                ret.append((x-1,y+1))

            if self.is_white(self.return_figur(x-1,y-1)): # checkt Feld links vorne auf Gegner
                ret.append((x-1,y-1))

        if piece == 2: # moves für b.Bauer
            if self.return_figur(x + 1, y) == 0:  # checkt 1 Feld davor
                ret.append((x + 1, y))

                if self.return_figur[x + 2][y] == 0:  # checkt 2 Felder davor
                    ret.append((x + 2, y))

            if self.is_white(self.return_figur(x + 1, y + 1)):  # checkt Feld rechts vorne auf Gegner
                ret.append((x + 1, y + 1))

            if self.is_white(self.return_figur(x + 1, y - 1)):  # checkt Feld links vorne auf Gegner
                ret.append((x + 1, y - 1))

        if piece == 3: # moves für knights
            if self.return_figur(self,x, y) == 0 or self.isnt_samecolor(self,x,y):
                ret.append((x,y))

    def move(self,x1,y1,x2,y2):
        self.board[x2][y2] = self.board[x1][y1]
        self.board[x1][y1] = 0



test = Spielfeld()

print(test.board)
test.move(6,4,4,4)
print(test.board)