from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTimer
from VentanaPrincipal import Ui_Principal
from codigoPuntajes import MyformPuntaje
from codigoSudoku import MyformSudoku



class Myform(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Principal()
        self.ui.setupUi(self)
        self.niveles()        
        
        #Entrar para jugar
        self.connect(self.ui.bEntrar, QtCore.SIGNAL("clicked()"), self.abrirEntrar)
        #Puntajes del Juego
        self.connect(self.ui.bPuntajes, QtCore.SIGNAL("clicked()"), self.abrirPuntajes)
    
    def niveles(self):
        self.ui.comboBox.addItem("Juvenil")
        self.ui.comboBox.addItem("Profesional")
        self.ui.comboBox.addItem("Experto")
        
    def abrirPuntajes(self):
        self.hide()
        self.puntajes = MyformPuntaje()
        self.puntajes.setVentanaPrincipal(self)
        self.puntajes.show()

    def abrirEntrar(self):
        self.inicialBarra()   
        self.timer.start(30)
    
    
    def inicialBarra(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start(10)
        self.valor = 0
        self.timer.timeout.connect(self.tiempoBarra)        
        
    def tiempoBarra(self):
        self.ui.barra.setValue(self.valor)
        self.valor = self.valor + 1
               
        if self.valor == 101:
            self.timer.stop()
            self.nombre = self.ui.nombreJug.text()
            self.nivel = self.ui.comboBox.currentText()
            
            self.hide()
            self.principal = MyformSudoku()
            self.principal.obtenerNombreNivel(self.nombre, self.nivel)
            self.principal.show()
                                
