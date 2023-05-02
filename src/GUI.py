from PyQt5 import QtCore, QtWidgets, QtGui

class GUI(QtWidgets.QApplication):
    def __init__(self):
        super(GUI, self).__init__([])
        window = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QPushButton('Top'))

        window.setLayout(layout)
        window.show()
        self.exec()


    print("Created GUI.")
