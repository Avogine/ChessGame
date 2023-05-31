#import GUI
import engine
import random

#gui = GUI.GUI()

my_board = engine.Chessboard()
"""def ready():
    # create new chess gui
    pass


if __name__ == "__main__":
    ready()"""

def ren(p):
    f = my_board.board[p]
    if f == 0:
        return(" ")
    elif f == 1:
        return("P")
    elif f == 3:
        return("K")
    elif f == 5:
        return("B")
    elif f == 7:
        return("R")
    elif f == 9:
        return("Q")
    elif f == 11:
        return("K")

    elif f == 2:
        return("p")
    elif f == 4:
        return("k")
    elif f == 6:
        return("b")
    elif f == 8:
        return("r")
    elif f == 10:
        return("q")
    elif f == 12:
        return("k")
def term_render():
    print(f"""
   A     B     C     D     E     F     G     H          Check: {my_board.stat_check}
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐       Material: {my_board.material} """)
    for i in (0, 10, 20, 30, 40, 50, 60):
        print(
            f"""│  {ren(i + 1)}  │  {ren(i + 2)}  │  {ren(i + 3)}  │  {ren(i + 4)}  │  {ren(i + 5)}  │  {ren(i + 6)}  │  {ren(i + 7)}  │  {ren(i + 8)}  │  {int((80 - i) /10)}     
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤""")
    print(
        f"""│  {ren(71)}  │  {ren(72)}  │  {ren(73)}  │  {ren(74)}  │  {ren(75)}  │  {ren(76)}  │   {ren(77)} │  {ren(78)}  │  1
└─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘""")

def my_input(inp):
    x, y = list(inp)
    x = x.lower()
    if x == "a":
        return (80 - (int(y) * 10) + 1)
    elif x == "b":
        return (80 - (int(y) * 10) + 2)
    elif x == "c":
        return (80 - (int(y) * 10) + 3)
    elif x == "d":
        return (80 - (int(y) * 10) + 4)
    elif x == "e":
        return (80 - (int(y) * 10) + 5)
    elif x == "f":
        return (80 - (int(y) * 10) + 6)
    elif x == "g":
        return (80 - (int(y) * 10) + 7)
    elif x == "h":
        return (80 - (int(y) * 10) + 8)

def my_output(out): #give int return string
    x = out%10
    y = (out - x)/10
    if x == 1:
        return("a" + str(int(8 - y)))
    elif x == 2:
        return("b" + str(int(8 - y)))
    elif x == 3:
        return("c" + str(int(8 - y)))
    elif x == 4:
        return("d" + str(int(8 - y)))
    elif x == 5:
        return("e" + str(int(8 - y)))
    elif x == 6:
        return("f" + str(int(8 - y)))
    elif x == 7:
        return("g" + str(int(8 - y)))
    elif x == 8:
        return("h" + str(int(8 - y)))




def answer(type):
    ran = random.randrange(3)
    if type == 2:
        ans = ["You can not move enemy pieces, dumass", " That are not your pieces!", "Ah ah ah not that one", "Pls select your own piece"]
        print(f"[T] {ans[ran]}")
    elif type == 3:
        ans = ["There is no piece to select, you boozzo!", "Nice choice ... wait there is no piece?", "You wanna play with air?", "??? ... There is no piece"]
        print(f"[T] {ans[ran]}")


def select(pos):
    if len(pos) == 2:
        r = ""
        pos = int(my_input(pos))
        figur = my_board.return_figur(pos)
        if figur != 0 and figur != 13:
            if figur % 2 == my_board.movecount % 2:
                leg_moves = my_board.check_pos_moves(pos)
                for p in leg_moves:
                    r = my_output(p)+ " " + r

                print(f"[T] Your legal moves are: {str(r)} ")
                move = input(f"[{turn}] Move: ")

                movement(pos, move)

            else:
                answer(2)
                pos = input(f"[{turn}] Select: ")
                select(pos)
        else:
            answer(3)
            pos = input(f"[{turn}] Select: ")
            select(pos)
    else:
        print("[T] Pls select a field.")
        pos = input(f"[{turn}] Select: ")
        select(pos)

def movement(pos, move):
    if len(move) == 2:
        move = my_input(move)
        m = my_board.check_pos_moves(pos)
        if move in m:
            take = my_board.move(pos, move)
            if take != "":
                take = f"You took a {take}."
            print(f"[T] Good move.{take} Next Player ({my_board.movecount})")

        elif my_board.return_figur(move) != 13 and my_board.return_figur(move) != 0 and my_board.return_figur(move)%2 == my_board.return_figur(pos)%2:
            print(f"[T] {my_output(move)} was selected")
            leg_moves = my_board.check_pos_moves(pos)
            r = ""
            for p in leg_moves:
                r = my_output(p) + " " + r

            print(f"[T] Your legal moves are: {str(r)} ")
            move2 = input(f"[{turn}] Move: ")
            movement(move, move2)
        else:
            move = input(f"[{turn}] Move: ")
            movement(pos, move)
    else:
        print("[T] Pls choose a move")
        move = input(f"[{turn}] Move: ")
        movement(pos, move)


print('''A Chess Game by David Walk and Jan Grüninger
Have Fun!!!
''')
while True: #start

    if my_board.movecount%2 == 0:
        turn = "B"
    else:
        turn = "W"

    term_render()
    pos = input(f"[{turn}] Select: ")
    select(pos)







