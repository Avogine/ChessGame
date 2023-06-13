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

        # make playboard_engine instance
        self.chess_board = engine.Chessboard()

        # add board to second layout
        self.board = Board(self.chess_board)
        self.hboxlayout.addWidget(self.board)

        self.window.setLayout(self.vboxlayout)
        self.window.show()
        self.window.setWindowTitle('ChessGame')

        # fill board
        self.board.update_from_list(self.chess_board.board)
        
        # run
        self.exec()


class HintGrid(QtWidgets.QWidget):
    def __init__(self, parent, chess_board: engine.Chessboard, square_size=Qt.QSize(50, 50)):
        super().__init__(parent=parent)

        # variables
        self.square_size = square_size
        self.chess_board = chess_board

        # set up grid layout
        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSizeConstraint(Qt.QGridLayout.SizeConstraint.SetFixedSize)
        self.grid_layout.setVerticalSpacing(0)
        self.grid_layout.setHorizontalSpacing(0)

        # set minimum width and height, else the layout just collapses
        for i in range(8):
            self.grid_layout.setColumnMinimumWidth(i, self.square_size.width()) # TODO: use variables for minimum size
            self.grid_layout.setRowMinimumHeight(i, self.square_size.height())

    def sizeHint(self) -> Qt.QSize:
        return self.square_size
    
    def set_hints(self, piece_pos: tuple, selected=True):
        # get all necessary values
        # all even numbers correspond to black moves
        # all uneven numbers are white moves

        movecount = self.chess_board.movecount
        piece_pos_int = helpers.pos_to_engineint(piece_pos[0], piece_pos[1])
        white_moving = bool(movecount % 2)
        piece_type = self.chess_board.return_figur(piece_pos_int)
        print("Type", piece_type)

        # remove all old hints
        for i in range(63):
            row, column = helpers.int_to_rowcolumn(i)
            item = self.grid_layout.itemAtPosition(row, column)
            if item != None:
                self.grid_layout.removeItem(item)
                print("removed", item, row, column)
                item.widget().deleteLater() # not sure if needed but lets hope this works

        if engine.is_white(piece_type) == white_moving:
            legal_moves = self.chess_board.check_pos_moves(piece_pos_int)

            if selected:
                print("Added")
                for move in legal_moves:
                    print(move)

                    widget = Hint()
                    new_row, new_column = helpers.engineint_to_rowcolumn(move)

                    self.grid_layout.addWidget(widget, new_row, new_column)

            


class Checkerboard(QtWidgets.QWidget):
    def __init__(self, parent=None, color_bright=QtGui.QColor("#ffffff"), color_dark=QtGui.QColor("#222222"),
                 square_size=50):
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
                    color = self.color_bright
                else:
                    color = self.color_dark

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
    def __init__(self, chess_board, color_1=QtGui.QColor("#5f8231"), color_2=QtGui.QColor("#ffffff"),
                 square_size=Qt.QSize(50, 50)):
        super().__init__()

        self.square_size = square_size
        self.chess_board = chess_board

        # add background
        self.checkerboard = Checkerboard(parent=self)
        self.checkerboard.show()

        # add grid layout behind true pieces for hints
        self.hint_grid = HintGrid(self, self.chess_board, square_size)

        # add grid layout
        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSizeConstraint(Qt.QGridLayout.SizeConstraint.SetFixedSize)
        self.grid_layout.setVerticalSpacing(0)
        self.grid_layout.setHorizontalSpacing(0)

        #self.grid_layout.setGeometry(QtCore.QRect(0, 0, self.square_size.width(), self.square_size.height())) # not sure if needed
        self.setAcceptDrops(True)

        # set minimum width and height, else the layout just collapses
        for i in range(8):
            self.grid_layout.setColumnMinimumWidth(i, self.square_size.width()) # TODO: use variables for minimum size
            self.grid_layout.setRowMinimumHeight(i, self.square_size.height())

        # variables
        self.selected_piece = (-1, -1)

    def update_from_list(self, board_list=None):
        # remove old pieces
        for i in range(63):
            row, column = helpers.int_to_rowcolumn(i)
            item = self.grid_layout.itemAtPosition(row, column)
            if item != None:
                self.grid_layout.removeItem(item)
                print("removed", item, row, column)
                item.widget().deleteLater() # not sure if needed but lets hope this works

        own_idx = 0
        engine_idx = 0
        if board_list is not None:
            for piece in board_list:
                if piece != 13:
                    # calculate row and column
                    row, column= helpers.int_to_rowcolumn(own_idx)
                    if piece != 0:
                        self.set_piece(row, column, piece)
                    own_idx += 1

                engine_idx += 1

    # this does not check whether the move is allowed or not
    def move_piece(self, origin: tuple, dest: tuple):
        # unpack variables
        old_column, old_row = origin
        new_column, new_row = dest

        old_piece = self.grid_layout.itemAtPosition(old_row, old_column)
        old_piece_widget = old_piece.widget()

		# remove piece at new position, if there is any
        captured_piece = self.grid_layout.itemAtPosition(new_row, new_column)
        if captured_piece != None:
            self.grid_layout.removeItem(captured_piece)
            captured_piece.widget().deleteLater()

        # move item from old to new position
        self.grid_layout.removeItem(old_piece)
        self.grid_layout.addWidget(old_piece_widget, new_row, new_column)

        # tell engine to move piece
        old_pos = helpers.pos_to_engineint(old_column, old_row)
        new_pos = helpers.pos_to_engineint(new_column, new_row)

        self.chess_board.move(old_pos, new_pos)

        # TODO: to account for changes rebuild whole board
        #self.update_from_list(self.chess_board.board)

    def set_piece(self, row=0, column=0, piece_id=0):
        # remove piece
        item = self.grid_layout.itemAtPosition(row, column)
        item_widget = ChessPiece(piece_type=piece_id)

        if item:  # check to avoid None, then remove
            item_widget = item.widget()
            self.grid_layout.removeItem(item)

        else:  # set the piece
            self.grid_layout.addWidget(item_widget, row, column)

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

        # update move hints
        self.hint_grid.set_hints(piece_pos, selected)
        print("selected", selected)

    def invert_piece_selection(self, piece_pos=(0, 0)):
        # check if piece is already selected
        if self.selected_piece == piece_pos:
            self.set_selected_piece(piece_pos, False)
        else:
            self.set_selected_piece(piece_pos, True)

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
            else:  # piece should be moved, deselect
                self.set_selected_piece((0, 0), False)

                # check if move is made from right color
                movecount = self.chess_board.movecount
                piece_pos_int = helpers.pos_to_engineint(old_column, old_row)
                white_moving = bool(movecount % 2)
                piece_type = self.chess_board.return_figur(piece_pos_int)
                right_color = white_moving == engine.is_white(piece_type)

                # check if move is legal
                old_engineint = helpers.pos_to_engineint(old_column, old_row)
                new_engineint = helpers.pos_to_engineint(new_column, new_row)
                legal_moves = self.chess_board.check_pos_moves(old_engineint)
                legal = new_engineint in legal_moves

                print(legal_moves, old_row, old_column, old_engineint)

                if right_color and legal:
                    self.move_piece((old_column, old_row), (new_column, new_row))

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
        else: # normal press action
            pass # TODO: implement press movement
        


    def minimumSizeHint(self):
        return self.checkerboard.minimumSizeHint()


class Hint(QtWidgets.QLabel):
    def __init__(self, fix_size=QtCore.QSize(50, 50)):
        super().__init__()

        # set size policy
        h_policy = QtWidgets.QSizePolicy.Policy.Fixed
        v_policy = QtWidgets.QSizePolicy.Policy.Fixed
        policy = QtWidgets.QSizePolicy(h_policy, v_policy)

        self.setSizePolicy(policy)

        self.fix_size = fix_size

        # set up sprite
        path = helpers.get_marker_sprite_path()
        self.sprite = Qt.QPixmap(str(path))
        self.setPixmap(self.sprite.scaled(self.fix_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                  QtCore.Qt.TransformationMode.SmoothTransformation))
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def sizeHint(self) -> QtCore.QSize:
        return self.fix_size


class ChessPiece(QtWidgets.QLabel):
    def __init__(self, fix_size=QtCore.QSize(50, 50), piece_type=1):
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
            self.setPixmap(self.sprite.scaled(self.fix_size * 0.75, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))

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
                self.setPixmap(self.sprite.scaled(self.fix_size * 0.75, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                  QtCore.Qt.TransformationMode.SmoothTransformation))
            else:
                # scale pixmap to original size
                self.setPixmap(self.sprite.scaled(self.fix_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                  QtCore.Qt.TransformationMode.SmoothTransformation))
