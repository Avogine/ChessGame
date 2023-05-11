from PyQt5 import QtCore, QtWidgets, QtGui


class GUI(QtWidgets.QApplication):
    def __init__(self):
        super(GUI, self).__init__([])
        self.window = QtWidgets.QWidget()
        self.vboxlayout = QtWidgets.QVBoxLayout()  # storing the top part (board and controls) and bottom (statistics)
        self.hboxlayout = QtWidgets.QHBoxLayout()  # this second layout stores the board and controls
        self.vboxlayout.addLayout(self.hboxlayout)

        # add board to second layout
        self.board = Board()
        self.hboxlayout.addLayout(self.board)

        self.window.setLayout(self.vboxlayout)
        self.window.show()
        self.exec()


class Board(QtWidgets.QGridLayout):
    def __init__(self, color_1=QtGui.QColor("#5f8231"), color_2=QtGui.QColor("#ffffff")):
        super(Board, self).__init__()

        # TODO: set minimum width and height for each column

        for row in range(0, 10):
            for column in range(0, 10):
                button = SquareButton()
                button.setFlat(True)
                self.addWidget(button, row, column)

    print("Created GUI.")


class SquareButton(QtWidgets.QPushButton):
    def __init__(self, min_size=QtCore.QSize(50, 50)):
        super(SquareButton, self).__init__()

        # set size policy
        h_policy = QtWidgets.QSizePolicy.Policy.Fixed
        v_policy = QtWidgets.QSizePolicy.Policy.Fixed
        policy = QtWidgets.QSizePolicy(h_policy, v_policy, QtWidgets.QSizePolicy.ControlType.PushButton)

        self.setSizePolicy(policy)

        self.setFixedSize(min_size)
