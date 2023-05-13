from PyQt5 import QtCore, QtWidgets, QtGui, Qt


class GUI(QtWidgets.QApplication):
    def __init__(self):
        super(GUI, self).__init__([])
        self.window = QtWidgets.QWidget()
        self.vboxlayout = QtWidgets.QVBoxLayout()  # storing the top part (board and controls) and bottom (statistics)
        self.hboxlayout = QtWidgets.QHBoxLayout()  # this second layout stores the board and controls
        self.vboxlayout.addLayout(self.hboxlayout)

        # add board to second layout
        self.board = Checkerboard()
        self.hboxlayout.addWidget(self.board)

        self.window.setLayout(self.vboxlayout)
        self.window.show()
        self.exec()


class Board(QtWidgets.QWidget):
    def __init__(self, color_1=QtGui.QColor("#5f8231"), color_2=QtGui.QColor("#ffffff")):
        super(Board, self).__init__()

        # TODO: set minimum width and height for each column

        # add background


        # add draggable items to one frame
        for column in range(0, 8):
            for row in range(0, 8):
                button = SquareButton()
                button.setFlat(True)
                button.setText(str(row) + ", " + str(column))
                palette = button.palette()
                palette.setColor()
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


class Checkerboard(QtWidgets.QWidget):
    def __init__(self, color_bright=QtGui.QColor("#ffffff"), color_dark=QtGui.QColor("#5f8231"), square_size=100):
        super(Checkerboard, self).__init__()

        self.color_bright = color_bright
        self.color_dark = color_dark
        self.square_size = square_size

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        painter.setBrush(Qt.QBrush())
        painter.setPen(Qt.QPen(Qt.QColor(0, 0, 0, 0)))  # HACK: This should theoretically use Qt.NoPen but can't find it

        # draw rects
        for row in range(0, 8):
            for column in range(0, 8):
                is_even = ((row + column) % 2) == 0 # yes I'm very proud of this line right here...

                if is_even:
                    color = self.color_dark
                else:
                    color = self.color_bright

                x = column * self.square_size
                y = row * self.square_size
                w = 100
                h = 100

                painter.setBrush(Qt.QBrush(color))
                painter.drawRect(x, y, w, h)

    def minimumSizeHint(self):
        return Qt.QSize(self.square_size * 8, self.square_size * 8)

    def sizeHint(self):
        return Qt.QSize(self.square_size * 8, self.square_size * 8)