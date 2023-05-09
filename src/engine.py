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

    def return_figur(self, x, y):
        return(self.board[x][y])

    def check_posmoves(self,x,y):
        piece = self.board[x][y]

        if piece == 0:
            return(0)
        if piece == 1:
            return([(1, 2), (2, 3)])

    def move(self,x1,y1,x2,y2):
        self.board[x2][y2] = self.board[x1][y1]
        self.board[x1][y1] = 0



test = Spielfeld()

print(test.board)
test.move(6,4,4,4)
print(test.board)