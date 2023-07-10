import random
from PyQt5 import QtCore, QtWidgets, QtGui, Qt
import engine
import helpers
from random import randrange
import time


class GUI(QtWidgets.QApplication):
    def __init__(self):
        super().__init__([])
        # register fonts
        Qt.QFontDatabase.addApplicationFont(str(helpers.get_font_path()))

        # set default font
        self.setFont(Qt.QFont('Highway Gothic', 30))

        # add start window
        self.menu_window = StartMenu()
        self.menu_window.start_button.clicked.connect(self.start_game)
        self.menu_window.stockfish_button.clicked.connect(self.start_stockfish_game)

        # run
        self.exec()

    def start_stockfish_game(self):
        # hide start menu
        self.menu_window.hide()

        # add main window
        self.game_window = GameWindowStockfish()
        self.game_window.stop_button.clicked.connect(self.stop_game)

    def start_game(self):
        # hide start menu
        self.menu_window.hide()

        # add main window
        self.game_window = GameWindow()
        self.game_window.stop_button.clicked.connect(self.stop_game)
        self.game_window.gamecontroller.game_over.connect(self.show_gameover_window)

    def show_gameover_window(self, gameover_message=''):
        # add gameover window
        self.gameover_window = GameOverWindow(gameover_message)

        self.gameover_window.back_button.clicked.connect(self.stop_game)

    def stop_game(self):
        # remove old window instances
        self.game_window.deleteLater()
        if hasattr(self, 'gameover_window'):
            self.gameover_window.deleteLater()
            del self.gameover_window

        # show menu window
        self.menu_window.show()


class StartMenu(Qt.QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(100, 100, 100, 100)
        self.main_layout.setSpacing(50)
        self.setWindowTitle('ChessGame - Start Menu')

        # add buttons and labels
        self.icon = RandomPiece(size=QtCore.QSize(100, 100))
        self.main_layout.addWidget(self.icon, 100)
        self.main_layout.setAlignment(self.icon, QtCore.Qt.AlignmentFlag.AlignCenter)

        self.main_label = QtWidgets.QLabel('ChessGame\n-\nChess in Python by David Walk and Jan Grüninger.')
        self.main_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.main_label)

        self.start_button = QtWidgets.QPushButton("Start local game.")
        self.start_button.setSizePolicy(Qt.QSizePolicy.Maximum, Qt.QSizePolicy.Minimum)
        self.start_button.setMinimumSize(400, 100)
        self.main_layout.addWidget(self.start_button)
        self.main_layout.setAlignment(self.start_button, QtCore.Qt.AlignmentFlag.AlignHCenter)

        # add stockfish button
        self.stockfish_button = QtWidgets.QPushButton("Start local stockfish game.")
        self.stockfish_button.setSizePolicy(Qt.QSizePolicy.Maximum, Qt.QSizePolicy.Minimum)
        self.stockfish_button.setMinimumSize(600, 100)
        self.main_layout.addWidget(self.stockfish_button)
        self.main_layout.setAlignment(self.stockfish_button, QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.show()


class GameWindowStockfish(Qt.QWidget):
    def __init__(self):
        super().__init__()
        # variables
        self.margin = 5
        self.button_size = Qt.QSize(100 - self.margin, 100 - self.margin)

        # make playboard_engine instance
        self.chess_board = engine.Chessboard()

        self.vboxlayout = QtWidgets.QVBoxLayout()  # storing the top part (board and controls) and bottom (statistics)
        self.vboxlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.hboxlayout = QtWidgets.QHBoxLayout()  # this second layout stores the board and controls
        self.vboxlayout.addLayout(self.hboxlayout)

        self.controllayout = QtWidgets.QVBoxLayout()  # stores controls on left side of screen
        self.controllayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.hboxlayout.addLayout(self.controllayout)

        # TODO: implement other playable colors with stockfish
        # add board to second layout
        self.board = Board(self.chess_board, square_size=QtCore.QSize(100, 100),
                           use_stockfish_move=True)  # FIXME: hardcode
        self.hboxlayout.addWidget(self.board)

        # add gamecontroller
        self.gamecontroller = GameControllerStockish(self.board, self.chess_board)

        # configure stockfish
        self.chess_board.s_configure(15, 3200, 10)

        # add stop button
        self.stop_button = Qt.QPushButton('Stop')
        self.stop_button.setSizePolicy(Qt.QSizePolicy.Maximum, Qt.QSizePolicy.Maximum)
        self.stop_button.setMinimumSize(self.button_size)
        self.controllayout.addWidget(self.stop_button)

        # add revert button
        self.revert_button = Qt.QPushButton('<-')
        self.revert_button.setSizePolicy(Qt.QSizePolicy.Maximum, Qt.QSizePolicy.Maximum)
        self.revert_button.setMinimumSize(self.button_size)
        # self.controllayout.addWidget(self.revert_button)  # FIXME: reversing moves not possible
        # self.revert_button.clicked.connect(self.controllayout.reversemove)

        # add debug info button
        self.debug_info_button = Qt.QPushButton('DInfo')
        self.debug_info_button.setSizePolicy(Qt.QSizePolicy.Maximum, Qt.QSizePolicy.Maximum)
        self.debug_info_button.setMinimumSize(self.button_size)
        #self.controllayout.addWidget(self.debug_info_button)
        self.debug_info_button.clicked.connect(lambda: print(self.chess_board.info()))

        self.setLayout(self.vboxlayout)
        self.showFullScreen()
        self.setWindowTitle('ChessGame - Game')

        # fill board
        self.board.update_from_list(self.chess_board.board)


class GameWindow(Qt.QWidget):
    def __init__(self):
        super().__init__()
        # variables
        self.margin = 5
        self.button_size = Qt.QSize(100 - self.margin, 100 - self.margin)

        # make playboard_engine instance
        self.chess_board = engine.Chessboard()

        self.vboxlayout = QtWidgets.QVBoxLayout()  # storing the top part (board and controls) and bottom (statistics)
        self.vboxlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.hboxlayout = QtWidgets.QHBoxLayout()  # this second layout stores the board and controls
        self.vboxlayout.addLayout(self.hboxlayout)

        self.controllayout = QtWidgets.QVBoxLayout()  # stores controls on left side of screen
        self.controllayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.hboxlayout.addLayout(self.controllayout)

        # add board to second layout
        self.board = Board(self.chess_board, square_size=QtCore.QSize(100, 100))
        self.hboxlayout.addWidget(self.board)

        # add gamecontroller
        self.gamecontroller = GameController(self.board, self.chess_board)

        # add stop button
        self.stop_button = Qt.QPushButton('Stop')
        self.stop_button.setSizePolicy(Qt.QSizePolicy.Maximum, Qt.QSizePolicy.Maximum)
        self.stop_button.setMinimumSize(self.button_size)
        self.controllayout.addWidget(self.stop_button)

        # add revert button
        self.revert_button = Qt.QPushButton('<-')
        self.revert_button.setSizePolicy(Qt.QSizePolicy.Maximum, Qt.QSizePolicy.Maximum)
        self.revert_button.setMinimumSize(self.button_size)
        self.controllayout.addWidget(self.revert_button)
        self.revert_button.clicked.connect(self.gamecontroller.reverse_move)

        # add debug info button
        self.debug_info_button = Qt.QPushButton('DInfo')
        self.debug_info_button.setSizePolicy(Qt.QSizePolicy.Maximum, Qt.QSizePolicy.Maximum)
        self.debug_info_button.setMinimumSize(self.button_size)
        #self.controllayout.addWidget(self.debug_info_button)
        self.debug_info_button.clicked.connect(lambda: print(self.chess_board.info()))

        self.setLayout(self.vboxlayout)
        self.showFullScreen()
        self.setWindowTitle('ChessGame - Game')

        # fill board
        self.board.update_from_list(self.chess_board.board)


class GameOverWindow(QtWidgets.QWidget):
    def __init__(self, gameover_message=''):
        super().__init__()

        # add main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(100, 100, 100, 100)
        self.main_layout.setSpacing(50)
        self.setWindowTitle('ChessGame - Start Menu')

        # add buttons and labels
        self.main_label = QtWidgets.QLabel('Game Over\n-\nReason:\n ' + gameover_message)
        self.main_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.main_label)

        self.back_button = QtWidgets.QPushButton("Return to main menu.")
        self.back_button.setSizePolicy(Qt.QSizePolicy.Maximum, Qt.QSizePolicy.Minimum)
        self.back_button.setMinimumSize(400, 100)
        self.main_layout.addWidget(self.back_button)
        self.main_layout.setAlignment(self.back_button, QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.show()



class PromotingWindow(QtWidgets.QWidget):
    promote = QtCore.pyqtSignal(int, int)

    def __init__(self, parent, color='black', piece_pos_int=0, square_size=QtCore.QSize(100, 100), position=QtCore.QPoint(0, 0)):
        super().__init__()
        self.color = color
        self.piece_pos_int = piece_pos_int
        self.square_size = square_size

        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)

        # set up vboxlayout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # load sprites
        self.queen_icon = Qt.QIcon(str(helpers.get_piece_sprite_path(9 + int(self.color == 'black'))))
        self.rook_icon = Qt.QIcon(str(helpers.get_piece_sprite_path(7 + int(self.color == 'black'))))
        self.bishop_icon = Qt.QIcon(str(helpers.get_piece_sprite_path(5 + int(self.color == 'black'))))
        self.knight_icon = Qt.QIcon(str(helpers.get_piece_sprite_path(3 + int(self.color == 'black'))))

        # add possible pieces as buttons
        self.queen_button = QtWidgets.QPushButton()
        self.queen_button.setIcon(self.queen_icon)
        self.queen_button.setIconSize(self.square_size)
        self.queen_button.clicked.connect(self.promote_queen)
        self.main_layout.addWidget(self.queen_button)
        self.rook_button = QtWidgets.QPushButton()
        self.rook_button.setIcon(self.rook_icon)
        self.rook_button.setIconSize(self.square_size)
        self.rook_button.clicked.connect(self.promote_rook)
        self.main_layout.addWidget(self.rook_button)
        self.bishop_button = QtWidgets.QPushButton()
        self.bishop_button.setIcon(self.bishop_icon)
        self.bishop_button.setIconSize(self.square_size)
        self.bishop_button.clicked.connect(self.promote_bishop)
        self.main_layout.addWidget(self.bishop_button)
        self.knight_button = QtWidgets.QPushButton()
        self.knight_button.setIcon(self.knight_icon)
        self.knight_button.setIconSize(self.square_size)
        self.knight_button.clicked.connect(self.promote_knight)
        self.main_layout.addWidget(self.knight_button)

        self.move(position)
        self.show()

    def promote_queen(self):
        self.promote.emit(self.piece_pos_int, 9 + int(self.color == 'black'))

    def promote_rook(self):
        self.promote.emit(self.piece_pos_int, 7 + int(self.color == 'black'))

    def promote_bishop(self):
        self.promote.emit(self.piece_pos_int, 5 + int(self.color == 'black'))

    def promote_knight(self):
        self.promote.emit(self.piece_pos_int, 3 + int(self.color == 'black'))

    def sizeHint(self) -> Qt.QSize:
        return Qt.QSize(self.square_size.width(), self.square_size.height() * 4)
    def minimumSizeHint(self) -> Qt.QSize:
        return Qt.QSize(self.square_size.width(), self.square_size.height() * 4)


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
            self.grid_layout.setColumnMinimumWidth(i, self.square_size.width())  # TODO: use variables for minimum size
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

        # remove all old hints
        for i in range(63):
            row, column = helpers.int_to_rowcolumn(i)
            item = self.grid_layout.itemAtPosition(row, column)
            if item != None:
                self.grid_layout.removeItem(item)
                item.widget().deleteLater()  # not sure if needed but lets hope this works

        if engine.is_white(piece_type) == white_moving:
            legal_moves = self.chess_board.check_pos_moves(piece_pos_int)

            if selected:
                for move in legal_moves:
                    widget = Hint(fix_size=self.square_size)
                    new_row, new_column = helpers.engineint_to_rowcolumn(move)

                    self.grid_layout.addWidget(widget, new_row, new_column)


class Checkerboard(QtWidgets.QWidget):
    def __init__(self, parent=None, color_bright=QtGui.QColor("#eeeed2"), color_dark=QtGui.QColor("#769656"),
                 square_size=QtCore.QSize(50, 50)):
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

                x = column * self.square_size.width()
                y = row * self.square_size.height()
                w = self.square_size.width()
                h = self.square_size.height()

                painter.setBrush(Qt.QBrush(color))
                painter.drawRect(x, y, w, h)

    def minimumSizeHint(self):
        return Qt.QSize(self.square_size.width() * 8, self.square_size.height() * 8)

    def sizeHint(self):
        return Qt.QSize(self.square_size.width() * 8, self.square_size.height() * 8)


class Board(Qt.QWidget):
    # signals
    move_done = QtCore.pyqtSignal()

    def __init__(self, chess_board, color_1=QtGui.QColor("#5f8231"), color_2=QtGui.QColor("#ffffff"),
                 square_size=Qt.QSize(50, 50), use_stockfish_move=False):
        super().__init__()

        self.square_size = square_size
        self.chess_board = chess_board
        self.use_stockfish_move = use_stockfish_move

        # add background
        self.checkerboard = Checkerboard(parent=self, square_size=self.square_size)
        self.checkerboard.show()

        # add grid layout
        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSizeConstraint(Qt.QGridLayout.SizeConstraint.SetFixedSize)
        self.grid_layout.setVerticalSpacing(0)
        self.grid_layout.setHorizontalSpacing(0)

        self.setAcceptDrops(True)

        # add grid layout in front of true pieces for hints
        self.hint_grid = HintGrid(self, self.chess_board, square_size)

        # set minimum width and height, else the layout just collapses
        for i in range(8):
            self.grid_layout.setColumnMinimumWidth(i, self.square_size.width())
            self.grid_layout.setRowMinimumHeight(i, self.square_size.height())

        # variables
        self.selected_piece = (-1, -1)
        self.current_turn_type = 'white'  # can either be white, black, or external
        self.promotion_window = None

    def allow_next_move(self, turn_type: str):
        match turn_type:
            case 'black':
                self.current_turn_type = 'black'
            case 'white':
                self.current_turn_type = 'white'

    def compare_board(self, engine_board):
        equal = True
        own_idx = 0
        for engine_piece in engine_board:
            if engine_piece != 13:
                row, column = helpers.int_to_rowcolumn(own_idx)
                own_piece = self.grid_layout.itemAtPosition(row, column)

                # check if there is no piece
                if engine_piece == 0:
                    if own_piece is not None:
                        if own_piece.widget().piece_type != engine_piece:
                            equal = False
                else:  # if there should be a piece
                    if own_piece is None:
                        equal = False
                    elif own_piece.widget().piece_type != engine_piece:
                        equal = False

                own_idx += 1

        return equal

    def update_from_list(self, board_list=None):
        # deselect all selected pieces
        self.hint_grid.set_hints((-1, -1))

        # remove old pieces
        for i in range(64):  # range 64 means including only 63
            row, column = helpers.int_to_rowcolumn(i)
            item = self.grid_layout.itemAtPosition(row, column)
            if item != None:
                self.grid_layout.removeItem(item)
                item.widget().deleteLater()  # not sure if needed but lets hope this works

        own_idx = 0
        engine_idx = 0
        if board_list is not None:
            for piece in board_list:
                if piece != 13:
                    # calculate row and column
                    row, column = helpers.int_to_rowcolumn(own_idx)
                    if piece != 0:
                        self.set_piece(row, column, piece)
                    own_idx += 1

                engine_idx += 1

    def allow_promotion(self, color: str, piece_pos_int: int, window_pos: Qt.QSize):
        # set to no playable color
        self.current_turn_type = ''

        # open promotion window
        self.promotion_window = PromotingWindow(self.parentWidget(), color, piece_pos_int, self.square_size, window_pos)
        self.promotion_window.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, True)
        self.promotion_window.setWindowFlag(QtCore.Qt.WindowType.WindowMinimizeButtonHint, False)
        self.promotion_window.setWindowFlag(QtCore.Qt.WindowType.WindowMaximizeButtonHint, False)
        self.promotion_window.setWindowFlag(QtCore.Qt.WindowType.WindowTitleHint, False)
        self.promotion_window.setWindowTitle('Promotion')
        self.promotion_window.show()

        # connect necessary signal
        self.promotion_window.promote.connect(self.finalize_promotion)

    @QtCore.pyqtSlot(int, int)
    def finalize_promotion(self, piece_pos_int: int, piece_type: int):
        self.chess_board.promotion(piece_pos_int, piece_type)
        self.promotion_window.deleteLater()

        self.update_from_list(self.chess_board.board)

        self.move_done.emit()

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

        if not self.use_stockfish_move:
            move_kind = self.chess_board.move(old_pos, new_pos)
        else:
            move_kind = self.chess_board.s_move(old_pos, new_pos)

        # to account for specific changes (en passant, rochade, ...) rebuild whole board
        if not self.compare_board(self.chess_board.board):
            self.update_from_list(self.chess_board.board)

        # emit signal if not promoting
        if move_kind != 1:  # normal move
            self.move_done.emit()
        elif move_kind == 1:
            window_pos = self.mapToGlobal(QtCore.QPoint(new_column * self.square_size.width(), new_row * self.square_size.height()))

            self.allow_promotion(self.current_turn_type, new_pos, window_pos)

    def set_piece(self, row=0, column=0, piece_id=0):
        # remove piece
        item = self.grid_layout.itemAtPosition(row, column)
        item_widget = ChessPiece(piece_type=piece_id, fix_size=self.square_size)

        if item:  # check to avoid None, then remove
            item_widget = item.widget()
            self.grid_layout.removeItem(item)

        else:  # set the piece
            self.grid_layout.addWidget(item_widget, row, column)

    def set_selected_piece(self, piece_pos=(0, 0), selected=True):
        new_selected_widget: ChessPiece = self.grid_layout.itemAtPosition(piece_pos[1], piece_pos[0]).widget()

        # deselect, even if we might select it again
        if self.selected_piece != (-1, -1):
            last_selected_item: ChessPiece = self.grid_layout.itemAtPosition(self.selected_piece[1],
                                                                             self.selected_piece[0])
            if self.grid_layout.itemAtPosition(self.selected_piece[1], self.selected_piece[0]) is not None:
                last_selected_item.widget().set_select(False)

        # select or deselect new one
        if selected:
            self.selected_piece = piece_pos
            new_selected_widget.set_select(True)
        else:
            self.selected_piece = (-1, -1)
            new_selected_widget.set_select(False)

        # update move hints
        self.hint_grid.set_hints(piece_pos, selected)

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

                # check if move is made from right color # TODO
                piece_pos_int = helpers.pos_to_engineint(old_column, old_row)
                piece_type = self.chess_board.return_figur(piece_pos_int)
                moving_allowed = False
                if self.current_turn_type == 'white' and engine.is_white(piece_type):
                    moving_allowed = True
                elif self.current_turn_type == 'black' and not engine.is_white(piece_type):
                    moving_allowed = True

                # check if move is legal
                old_engineint = helpers.pos_to_engineint(old_column, old_row)
                new_engineint = helpers.pos_to_engineint(new_column, new_row)
                legal_moves = self.chess_board.check_pos_moves(old_engineint)
                legal = new_engineint in legal_moves

                if moving_allowed and legal:
                    self.move_piece((old_column, old_row), (new_column, new_row))

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        # get child from position
        child = self.childAt(event.pos())
        if isinstance(child, ChessPiece):
            # get piece position
            grid_size = self.grid_layout.sizeHint()
            mouse_normalized = event.pos()
            column = int(((mouse_normalized.x() / grid_size.width()) * 8))
            row = int(((mouse_normalized.y() / grid_size.height()) * 8))

            # get piece color
            piece_pos_int = helpers.pos_to_engineint(column, row)
            piece_type = self.chess_board.return_figur(piece_pos_int)

            # check if move from that color is allowed
            moving_allowed = False
            if self.current_turn_type == 'white' and engine.is_white(piece_type):
                moving_allowed = True
            elif self.current_turn_type == 'black' and not engine.is_white(piece_type):
                moving_allowed = True

            if moving_allowed:
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
        else:  # normal press action
            pass  # TODO: implement # press movement

        # possibilities:
        # click on empty square:
        # -> own piece is selected:
        # -> -> move own piece
        # click on square with piece:
        # -> own piece is currently selected:
        # -> -> target square has opponent piece:
        # -> -> -> take piece
        # -> -> target square is empty:
        # -> -> -> if move is legal: move piece
        #
        # -> no piece is selected:
        # -> -> select own piece and show possible moves
        # -> own piece is selected:
        # -> -> deselect own piece

    def minimumSizeHint(self):
        return self.checkerboard.minimumSizeHint()


class GameControllerStockish(QtCore.QObject):
    game_over = QtCore.pyqtSignal(str)

    def __init__(self, board: Board, engine_chess_board: engine.Chessboard, player_color='white'):
        super().__init__()
        self.board = board
        self.engine_chess_board = engine_chess_board
        self.board.move_done.connect(self.on_move_done)

        self.player_color = player_color

    def on_move_done(self):
        # check if there is a checkmate
        checkmate_type = self.engine_chess_board.check_all()
        print(checkmate_type)
        match checkmate_type:
            case 0:  # no checkmate
                movecount = self.engine_chess_board.movecount
                white_moving = white_moving = bool(movecount % 2)

                if (self.player_color == 'white') == white_moving:
                    self.board.allow_next_move(self.player_color)
                else:  # let stockfish make a move
                    self.engine_chess_board.stockfish_move()
                    self.board.update_from_list(self.engine_chess_board.board)

            case 1:  # check because of fifty move rule
                self.game_over.emit('Remis: Fifty move rule.')
            case 2:
                self.game_over.emit('Remis: Repeated position.')
            case 4:
                self.game_over.emit('Remis: Stalemate.')
            case 3:
                self.game_over.emit('Checkmate. Congratulations!')

    def reverse_move(self):
        pass
        '''
        self.engine_chess_board.reverse_move()
        self.board.update_from_list(self.engine_chess_board.board)

        white_moving = bool(self.engine_chess_board.movecount % 2)

        if white_moving:
            next_color = 'white'
        else:
            next_color = 'black'

        self.board.allow_next_move(next_color)
        '''


class GameController(QtCore.QObject):
    game_over = QtCore.pyqtSignal(str)

    def __init__(self, board: Board, engine_chess_board: engine.Chessboard):
        super().__init__()
        self.board = board
        self.engine_chess_board = engine_chess_board
        self.board.move_done.connect(self.on_move_done)

    def on_move_done(self):
        # check if there is a checkmate
        checkmate_type = self.engine_chess_board.check_all()

        match checkmate_type:
            case 0:  # no checkmate
                movecount = self.engine_chess_board.movecount
                white_moving = white_moving = bool(movecount % 2)

                if white_moving:
                    next_color = 'white'
                else:
                    next_color = 'black'

                self.board.allow_next_move(next_color)
            case 1:  # check because of fifty move rule
                self.game_over.emit('Remis: Fifty move rule.')
            case 2:
                self.game_over.emit('Remis: Repeated position.')
            case 4:
                self.game_over.emit('Remis: Stalemate.')
            case 3:
                self.game_over.emit('Checkmate. Congratulations!')

    def reverse_move(self):
        self.engine_chess_board.reverse_move()
        self.board.update_from_list(self.engine_chess_board.board)

        white_moving = bool(self.engine_chess_board.movecount % 2)

        if white_moving:
            next_color = 'white'
        else:
            next_color = 'black'

        self.board.allow_next_move(next_color)


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
        return self.sprite.scaled(self.fix_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                  QtCore.Qt.TransformationMode.SmoothTransformation)

    def set_select(self, selected=True):
        if self.selected and not selected:
            # scale pixmap to original size
            self.setPixmap(self.sprite.scaled(self.fix_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                              QtCore.Qt.TransformationMode.SmoothTransformation))
        elif not self.selected and selected:
            # scale pixmap to indicate selection
            self.setPixmap(self.sprite.scaled(self.fix_size * 0.75, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                              QtCore.Qt.TransformationMode.SmoothTransformation))

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


class RandomPiece(ChessPiece):
    def __init__(self, size=Qt.QSize(50, 50)):
        # generate random piece type
        rand = random.randrange(1, 13)

        super().__init__(piece_type=rand, fix_size=size)

        # needs to be unset because of ChessPiece behaviour
        self.setAcceptDrops(False)
