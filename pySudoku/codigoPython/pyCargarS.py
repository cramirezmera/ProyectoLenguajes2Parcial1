from CargarSudoku import Ui_CargarSudoku
from PyQt4 import QtGui, QtCore

class MyformCargarSudoku(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.uiCS = Ui_CargarSudoku()
        self.uiCS.setupUi(self)
        self.connect(self.uiCS.bsalirCargarJuego, QtCore.SIGNAL("clicked()"), self.volverSudoku)
        
    def setCombo(self, comboC, cont, nombreJ, nivel):
        self.nombreJugador = QtCore.QString(nombreJ)
        self.nivelJugador = QtCore.QString(nivel)
        self.comboCb = QtGui.QComboBox()
        for i in range(cont):
            if(self.comboCb.itemText(i) != ""):
                self.uiCS.comboBoxCargar.addItem(self.comboCb.itemText(i))
                    
    def ventanaCargar(self, ventanaCargar):
        self.ventanaC = ventanaCargar
        
    def volverSudoku(self):
        self.hide()
        self.ventanaC.show()