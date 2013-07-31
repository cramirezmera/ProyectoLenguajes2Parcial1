from CargarSudoku import Ui_CargarSudoku
from PyQt4 import QtGui, QtCore


nombreJugador = QtCore.QString()
nivelJugador = QtCore.QString()
valores = QtCore.QStringList()
nivelJ = QtCore.QString()
class MyformCargarSudoku(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.uiCS = Ui_CargarSudoku()
        self.uiCS.setupUi(self)
        self.connect(self.uiCS.bsalirCargarJuego, QtCore.SIGNAL("clicked()"), self.volverSudoku)              
        self.connect(self.uiCS.bcargarCargarJuego, QtCore.SIGNAL("clicked()"), self.bcargarPartida)

    #Funcion de obtener las partidas guardadas
    def obtenerPartidasGuardadas(self, nivel):
        nivelJ = nivel
        
        self.mFilename = QtCore.QString("guardar.txt")
        
        self.mFile = QtCore.QFile(self.mFilename)
        self.mFile.open(QtCore.QIODevice.Text | QtCore.QIODevice.ReadOnly)
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
            
            if (nivelJ == self.nivelC):
                self.uiCS.comboBoxCargar.addItem(self.nomJugador)
        
    def ventanaCargar(self, ventanaCargar):
        self.ventanaC = ventanaCargar

    def volverSudoku(self):
        self.hide()
        self.ventanaC.show()

    def bcargarPartida(self):
        self.mFilename = QtCore.QString("guardar.txt")
        self.mFile = QtCore.QFile(self.mFilename)
        self.mFile.open(QtCore.QIODevice.Text | QtCore.QIODevice.ReadOnly)
        if not (self.mFile.isOpen()):
            return
        self.txtstr = QtCore.QTextStream(self.mFile)
        
        while not (self.txtstr.atEnd()):
            self.datosSudoku = self.txtstr.readLine()
            self.mFile.flush()
            self.mFile.close()
            
            self.valores = self.datosSudoku.split("/")
            self.nomJugador = self.valores[0]
            self.nivelC = self.valores[1]
            self.cronometro = self.valores[2]
            self.datosSudoku = self.valores[3]
            
            if(self.nomJugador == self.uiCS.comboBoxCargar.currentText()):
                self.datos = self.datosSudoku
        
        self.hide()
        self.ventanaC.setCargar(self.datos, self.nivelC, self.cronometro, self.nomJugador)

