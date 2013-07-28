from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTimer
from VentanaPrincipal import Ui_Principal
from pyPuntajes import MyformPuntaje
from pySudoku import MyformSudoku



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
        self.mFilename = QtCore.QString("guardar.txt")
        self.mFile = QtCore.QFile(self.mFilename)
        if(self.mFile.exists()):
            self.hide()
            self.puntajes = MyformPuntaje()
            self.puntajes.setVentanaPrincipal(self)
            self.puntajes.show()
            self.puntajes.setPuntajes()
        else:
            QtGui.QMessageBox.information(self, "MENSAJE", "No existen Puntajes Guardados","ACEPTAR")

    def abrirEntrar(self):
        self.bandera = 0
        self.valores =QtCore.QStringList()
        self.nomJugador = QtCore.QString()
        self.nivelC = QtCore.QString()
        self.crono = QtCore.QString()
        self.datosSudoku = QtCore.QString()
        self.mFilename = QtCore.QString("guardar.txt")
        
        self.mFile = QtCore.QFile(self.mFilename)
        if(self.mFile.exists()):
            self.mFile.open(QtCore.QFile.Text | QtCore.QFile.ReadOnly)
            if not(self.mFile.isOpen()):
                return
            self.txtstr = QtCore.QTextStream(self.mFile)
            while not(self.txtstr.atEnd()):
                self.datosSudoku = self.txtstr.readLine()
                self.mFile.flush()
                self.mFile.close()
                
                self.valores = self.datosSudoku.split("/")
                self.nomJugador = self.valores[0]
                self.nivelC = self.valores[1]
                self.crono = self.valores[2]
                self.datosSudoku = self.valores[3]
                
                if(self.ui.nombreJug.displayText() == self.nomJugador):
                    self.bandera = 1
                    break
                
        if(self.ui.nombreJug.text() == ""):
            QtGui.QMessageBox.information(self, "MENSAJE", "Por favor agregue el\nnombre del JUGADOR","ACEPTAR")
        elif(self.bandera == 1):
            QtGui.QMessageBox.information(self, "MENSAJE", "Por favor ingrese otro \nnombre de JUGADOR","ACEPTAR")
        else :
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
                                
