from PyQt4 import QtCore, QtGui
from VentanaPrincipal import Ui_Principal
from codigoPuntajes import MyformPuntaje
from codigoSudoku import MyformSudoku

class Myform(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Principal()
        self.ui.setupUi(self)
        self.niveles()
        
    def niveles(self):
        self.ui.comboBox.addItem("Juvenil")
        self.ui.comboBox.addItem("Profesional")
        self.ui.comboBox.addItem("Experto")
        
        #Entrar para jugar
        self.connect(self.ui.bEntrar, QtCore.SIGNAL("clicked()"), self.abrirEntrar)
        #Puntajes del Juego
        self.connect(self.ui.bPuntajes, QtCore.SIGNAL("clicked()"), self.abrirPuntajes)
        
    def abrirPuntajes(self):
        self.hide()
        self.puntajes = MyformPuntaje()
        self.puntajes.setVentanaPrincipal(self)
        self.puntajes.show()

    def abrirEntrar(self):
        self.hide()
        self.principal = MyformSudoku()
        self.nombre = self.ui.nombreJug.text()
        self.nivel = self.ui.comboBox.currentText()
        self.principal.usuario(self.nombre, self.nivel)
        self.principal.show()       
