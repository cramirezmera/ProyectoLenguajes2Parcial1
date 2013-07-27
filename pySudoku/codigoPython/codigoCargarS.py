from CargarSudoku import Ui_CargarSudoku
from PyQt4 import QtGui

class MyformCargarSudoku(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.uiCS = Ui_CargarSudoku()
        self.uiCS.setupUi(self)