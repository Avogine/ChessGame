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

    def check_posmoves(self,x,y):
        piece = self.return_figur(x, y)
        ret = []
        if piece == 0: # moves für keine Figur
            pass
        if piece == 1: # moves für w.Bauer
            if self.return_figur(x-1,y) == 0: # checkt 1 Feld davor
                ret.append((x-1, y))

                if self.return_figur(x-2,y) == 0: # checkt 2 Felder davor
                    ret.append((x-2, y))

            if self.is_white(self.return_figur(x-1,y+1)): # checkt Feld rechts vorne auf Gegner
                ret.append((x-1,y+1))

            if self.is_white(self.return_figur(x-1,y-1)): # checkt Feld links vorne auf Gegner
                ret.append((x-1,y-1))

        if piece == 2: # moves für b.Bauer
            if self.return_figur(x + 1, y) == 0:  # checkt 1 Feld davor
                ret.append((x + 1, y))

                if self.return_figur(x + 2, y) == 0:  # checkt 2 Felder davor
                    ret.append((x + 2, y))

            if self.is_white(self.return_figur(x + 1, y + 1)):  # checkt Feld rechts vorne auf Gegner
                ret.append((x + 1, y + 1))

            if self.is_white(self.return_figur(x + 1, y - 1)):  # checkt Feld links vorne auf Gegner
                ret.append((x + 1, y - 1))

        if piece == 3 or piece == 4: # moves für knights
            for i in [-2,-1,1,2]:
                new_x = x + i
                new_y = -abs(i) + 3
                if self.return_figur(new_x, y - new_y) == 0 or self.isnt_samecolor(new_x, y - new_y):
                    ret.append((new_x,y - new_y))

                if self.return_figur(new_x, y + new_y) == 0 or self.isnt_samecolor(new_x,y + new_y):
                    ret.append((new_x,y + new_y))

        if piece == 5 or piece == 6: # moves for bishop

            for i in [-1,1]:
                new_x = x
                new_y = y
                for n in [-1,1]:
                    new_x =+ i
                    new_y =+ n
                    while self.return_figur(new_x,new_y) == 0:
                        ret.append((x+i, y+n))
                        new_x = + i
                        new_y = + n
                    if self.isnt_samecolor(self.return_figur(x,y), self.return_figur(new_x, new_y)):
                        ret.append((new_x,new_y))

        if piece == 7 or piece == 8: # moves for rook
            for i in [-1,1]:
                new_x = x
                new_y = y
                while self.return_figur(new_x+i,new_y) == 0:
                    ret.append((new_x+i,new_y))
                    new_x =+ i
                if self.isnt_samecolor(self.return_figur(x,y),self.return_figur(new_x+i,new_y)):
                    ret.append((new_x+i,new_y))
            for i in [-1,1]:
                new_x = x
                new_y = y
                while self.return_figur(new_x,new_y+i) == 0:
                    ret.append((new_x,new_y+i))
                    new_y =+ i
                if self.isnt_samecolor(self.return_figur(x,y),self.return_figur(new_x,new_y+i)):
                    ret.append((new_x,new_y+i))

        else:
            pass
        return(ret)


    def move(self,x1,y1,x2,y2):
        self.board[x2][y2] = self.board[x1][y1]
        self.board[x1][y1] = 0



test = Spielfeld()

print(test.board)
test.move(6,4,4,4)
print(test.board)