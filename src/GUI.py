from PyQt5 import QtCore, QtWidgets, QtGui, Qt

class GUI(QtWidgets.QApplication):
    def __init__(self):
        super().__init__([])
        self.window = QtWidgets.QWidget()
        self.vboxlayout = QtWidgets.QVBoxLayout()  # storing the top part (board and controls) and bottom (statistics)
        self.hboxlayout = QtWidgets.QHBoxLayout()  # this second layout stores the board and controls
        self.vboxlayout.addLayout(self.hboxlayout)

        # add board to second layout
        self.board = Board()
        self.hboxlayout.addWidget(self.board)

        self.window.setLayout(self.vboxlayout)
        self.window.show()
        self.exec()


class Checkerboard(QtWidgets.QWidget):
    def __init__(self, parent=None, color_bright=QtGui.QColor("#ffffff"), color_dark=QtGui.QColor("#5f8231"),
                 square_size=100):
        super().__init__(parent=parent)

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
                is_even = ((row + column) % 2) == 0  # yes I'm very proud of this line right here...

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


class Board(Qt.QWidget):
    def __init__(self, color_1=QtGui.QColor("#5f8231"), color_2=QtGui.QColor("#ffffff"), square_size=Qt.QSize(100, 100)):
        super().__init__()

        # TODO: set minimum width and height for each column

        # add background
        self.checkerboard = Checkerboard(parent=self)
        self.checkerboard.show()

        # add grid layout
        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSizeConstraint(Qt.QGridLayout.SizeConstraint.SetFixedSize)
        self.grid_layout.setVerticalSpacing(0)
        self.grid_layout.setHorizontalSpacing(0)

        # add draggable items
        for column in range(0, 8):
            for row in [0, 1, 6, 7]:
                sprite = QtGui.QPixmap(r'../src/sprites/rook.png')
                button = ChessPiece(square_size, sprite)
                self.grid_layout.addWidget(button, row, column)
                self.grid_layout.setColumnMinimumWidth(column, square_size.width())
                self.grid_layout.setRowMinimumHeight(column, square_size.height())

        self.setAcceptDrops(True)

    def minimumSizeHint(self):
        return self.checkerboard.minimumSizeHint()

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        # action needs to be accepted for dropEvent to be called
        text = event.mimeData().text().split('|', 3)

        if text[0] == 'position':
            event.acceptProposedAction()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        if event.mimeData().hasText():
            string = event.mimeData().text()

            key, x, y = string.split('|', 2)
            print(string)

            pos = [int(x), int(y)]

            new_pos = self.grid_layout.p.pos()

            old_piece = self.grid_layout.itemAtPosition(y, x)
            self.grid_layout.addWidget(old_piece, )


    def dragMoveEvent(self, a0: QtGui.QDragMoveEvent) -> None:
        pass
        # update position

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        # get child from position
        child = self.childAt(event.pos())
        if isinstance(child, ChessPiece):
            # get pixmap
            pixmap = child.pixmap()

            # construct data stream
            mimeData = Qt.QMimeData()
            piece_idx = self.grid_layout.indexOf(child)
            piece_pos = self.grid_layout.getItemPosition(piece_idx)
            piece_pos_string = 'position|' + str(piece_pos[0]) + '|' + str(piece_pos[1])
            mimeData.setText(piece_pos_string)

            # create drag object
            drag = Qt.QDrag(self)
            drag.setMimeData(mimeData)
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos() - child.pos())

            # hide image
            child.hide()

            # execute
            drag.exec()



    print("Created GUI.")


class ChessPiece(QtWidgets.QLabel):
    def __init__(self, fix_size=QtCore.QSize(100, 100), sprite: Qt.QPixmap = None):
        super().__init__()

        # set size policy
        h_policy = QtWidgets.QSizePolicy.Policy.Fixed
        v_policy = QtWidgets.QSizePolicy.Policy.Fixed
        policy = QtWidgets.QSizePolicy(h_policy, v_policy)

        self.setSizePolicy(policy)

        self.fix_size = fix_size

        # set up sprite
        self.setPixmap(sprite.scaled(fix_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.setScaledContents(True)

        # set dragging
        self.setAcceptDrops(True)

    def sizeHint(self) -> QtCore.QSize:
        return self.fix_size
