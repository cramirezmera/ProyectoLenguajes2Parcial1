from PyQt4 import QtCore, QtGui
from Puntajes import Ui_Puntajes

class MyformPuntaje(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.uiP = Ui_Puntajes()
        self.uiP.setupUi(self)
        self.connect(self.uiP.pVolver, QtCore.SIGNAL("clicked()"), self.volverVentana)
        
    def setVentanaPrincipal(self, v):
        self.principal = v

    def volverVentana(self):
        self.hide()
        self.principal.show()
