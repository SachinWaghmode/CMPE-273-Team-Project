import sys
from PyQt4 import QtGui, Qtcore


class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(0,0,1000,800)
        self.setWindowTitle("Image Detection Screen")
        self.home()

    def home(self)
        comparebutton = QtGui.QPushButton("Compare", self)
        comparebutton.clicked.connect()
        self.show()


def run()
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

