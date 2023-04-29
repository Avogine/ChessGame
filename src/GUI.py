from PyQt5 import QtCore, QtWidgets, QtGui


class GUI(QtWidgets.QApplication):
    def __init__(self):
        super(GUI, self).__init__([])

    print("Created GUI.")
