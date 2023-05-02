from PyQt5 import QtCore, QtWidgets, QtGui

class GUI(QtWidgets.QApplication):
    def __init__(self):
        super(GUI, self).__init__([])
        self.window = QtWidgets.QWidget()
        self.vboxlayout = QtWidgets.QVBoxLayout()  # storing the top part (board and controls) and bottom (statistics)
        self.hboxlayout = QtWidgets.QHBoxLayout()  # this second layout stores the board and controls
        self.vboxlayout.addLayout(self.hboxlayout)

        # add board to second layouto
        self.board = Board()
        self.hboxlayout.addLayout(self.board)


        self.window.setLayout(self.vboxlayout)
        self.window.show()
        self.exec()


class Board(QtWidgets.QGridLayout):
    def __init__(self):
        super(Board, self).__init__()

        # TODO: set minimum width and height for each column

        for row in range(0, 10):
            for column in range(0, 10):
                button = QtWidgets.QPushButton('Test')
                button.setFlat(True)
                self.addWidget(button, row, column)




    board = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]

    print("Created GUI.")