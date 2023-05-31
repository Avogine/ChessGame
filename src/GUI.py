from PyQt5 import QtCore, QtWidgets, QtGui, Qt
import engine
import helpers


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
        self.window.setWindowTitle('ChessGame')
        # make playboard_engine instance
        self.engine_board = engine.Spielfeld()
        self.board.update_from_list(self.engine_board.board)


        # run
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
    def __init__(self, color_1=QtGui.QColor("#5f8231"), color_2=QtGui.QColor("#ffffff"),
                 square_size=Qt.QSize(100, 100)):
        super().__init__()

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
                sprite = QtGui.QPixmap(r'../src/sprites/pawn.png')
                button = ChessPiece(square_size, 3)
                self.grid_layout.addWidget(button, row, column)
                self.grid_layout.setColumnMinimumWidth(column, square_size.width())
                self.grid_layout.setRowMinimumHeight(column, square_size.height())

        self.setAcceptDrops(True)

        # variables
        self.selected_piece = (-1, -1)

    def update_from_list(self, board_list=None):
        own_idx = 0
        engine_idx = 0
        if board_list is not None:
            for piece in board_list:
                if piece != 13 and piece != 0:
                    # calculate row and column
                    row = int(own_idx / 8)
                    column = own_idx % 8
                    print(piece)
                    self.set_piece(row, column, piece)
                    own_idx += 1

                engine_idx += 1

    def set_piece(self, row=0, column=0, piece_id=0):
        # remove piece
        item = self.grid_layout.itemAtPosition(row, column)
        item_widget = ChessPiece(piece_type=piece_id)

        if item:  # check to avoid None
            item_widget = item.widget()
            self.grid_layout.removeItem(item)

        else:  # set the piece
            self.grid_layout.addWidget(item_widget)

    def remove_hints(self, piece_pos):
        pass
        # TODO: remove all hints here

    def update_hints(self, piece_pos):
        pass
        # TODO: first remvove all, then create new hints

    def set_selected_piece(self, piece_pos=(0, 0), selected=True):
        new_selected_widget: ChessPiece = self.grid_layout.itemAtPosition(piece_pos[1], piece_pos[0]).widget()

        # deselect, even if we might select it again
        if self.selected_piece != (-1, -1):
            last_selected_widget: ChessPiece = self.grid_layout.itemAtPosition(self.selected_piece[1], self.selected_piece[0]).widget()
            last_selected_widget.set_select(False)

        # select or deselect new one
        if selected:
            self.selected_piece = piece_pos
            new_selected_widget.set_select(True)
        else:
            self.selected_piece = (-1, -1)
            new_selected_widget.set_select(False)
            print("deselect", new_selected_widget, self.selected_piece)

        # TODO: update move hints
        # update hints on where to move

    def invert_piece_selection(self, piece_pos=(0, 0)):
        # check if piece is already selected
        if self.selected_piece == piece_pos:
            self.set_selected_piece(piece_pos, False)
        else:
            self.set_selected_piece(piece_pos, True)

    def minimumSizeHint(self):
        return self.checkerboard.minimumSizeHint()

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        # action needs to be accepted for dropEvent to be called
        if event.mimeData().hasFormat('application/chessgame-drag'):
            event.acceptProposedAction()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        if event.mimeData().hasFormat('application/chessgame-drag'):
            data = event.mimeData().data('application/chessgame-drag').data()
            string = data.decode('UTF-8')

            key, old_column, old_row = string.split('|', 2)
            old_column = int(old_column)
            old_row = int(old_row)

            # get new position to put in
            # grid_corner = self.grid_layout.geometry()  # not needed, as event position is always relative to widget
            grid_size = self.grid_layout.sizeHint()  # this needs to use sizeHint, as .geometry() sometimes returns zero

            mouse_normalized = event.pos()
            new_column = int(((mouse_normalized.x() / grid_size.width()) * 8))
            new_row = int(((mouse_normalized.y() / grid_size.height()) * 8))

            # check if old position equals new position
            if old_column == new_column and old_row == new_row:  # piece was not moved, but selected
                self.invert_piece_selection((new_column, new_row))
            else:  # other piece was moved, deselect
                self.set_selected_piece((0, 0), False)

                old_piece = self.grid_layout.itemAtPosition(old_row, old_column)
                old_piece_widget = old_piece.widget()
                self.grid_layout.removeItem(old_piece)
                self.grid_layout.addWidget(old_piece_widget, new_row, new_column)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        # get child from position
        child = self.childAt(event.pos())
        if isinstance(child, ChessPiece):
            # get pixmap
            pixmap = child.get_drag_sprite()

            # construct data stream
            mimedata = Qt.QMimeData()
            piece_idx = self.grid_layout.indexOf(child)
            piece_pos = self.grid_layout.getItemPosition(piece_idx)
            piece_pos_string = 'position|' + str(piece_pos[1]) + '|' + str(piece_pos[0])
            piece_pos_bytes = piece_pos_string.encode("UTF-8")
            mimedata.setData('application/chessgame-drag', piece_pos_bytes)

            # create drag object
            drag = Qt.QDrag(self)
            drag.setMimeData(mimedata)
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos() - child.pos())

            # hide image
            child.hide()

            # execute
            drag.exec()

            # clean up
            child.show()

    print("Created GUI.")


class ChessPiece(QtWidgets.QLabel):
    def __init__(self, fix_size=QtCore.QSize(100, 100), piece_type=1):
        super().__init__()

        # set size policy
        h_policy = QtWidgets.QSizePolicy.Policy.Fixed
        v_policy = QtWidgets.QSizePolicy.Policy.Fixed
        policy = QtWidgets.QSizePolicy(h_policy, v_policy)

        self.setSizePolicy(policy)

        self.fix_size = fix_size

        # set up sprite
        self.sprite = None
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # set dragging
        self.setAcceptDrops(True)

        # variables
        self.selected = False
        self.piece_type = piece_type  # piece types have specific format
        self.set_type(piece_type)

        # piece types: pawn knight bishop rook queen king
        # white:       1    3      5      7    9     11
        # black:       2    4      6      8    10    12
        # 13: invalid / wall

    def sizeHint(self) -> QtCore.QSize:
        return self.fix_size

    def get_drag_sprite(self):
        return self.sprite.scaled(self.fix_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)

    def set_select(self, selected=True):
        if self.selected and not selected:
            # scale pixmap to original size
            self.setPixmap(self.sprite.scaled(self.fix_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))
        elif not self.selected and selected:
            # scale pixmap to indicate selection
            self.setPixmap(self.sprite.scaled(self.fix_size * 0.5, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))

        self.selected = selected

    def set_type(self, piece_type=0):
        if 0 <= piece_type <= 12:
            self.piece_type = piece_type

            # set new icon
            path = helpers.get_piece_sprite_path(piece_type)
            self.sprite = Qt.QPixmap(str(path))

            # TODO: maybe remove unnecessary double code (see above, used there too)
            if self.selected:
                # scale pixmap to indicate selection
                self.setPixmap(self.sprite.scaled(self.fix_size * 0.5, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                  QtCore.Qt.TransformationMode.SmoothTransformation))
            else:
                # scale pixmap to original size
                self.setPixmap(self.sprite.scaled(self.fix_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                  QtCore.Qt.TransformationMode.SmoothTransformation))
