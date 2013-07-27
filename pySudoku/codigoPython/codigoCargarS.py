from CargarSudoku import Ui_CargarSudoku
from PyQt4 import QtGui, QtCore

class MyformCargarSudoku(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.uiCS = Ui_CargarSudoku()
        self.uiCS.setupUi(self)
        self.connect(self.uiCS.bsalirCargarJuego, QtCore.SIGNAL("clicked()"), self.volverSudoku)
        
    def setCargar(self, ventanaCargar):
        self.ventanaC = ventanaCargar
        
    def volverSudoku(self):
        self.hide()
        self.ventanaC.show()