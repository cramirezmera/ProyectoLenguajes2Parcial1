from PyQt4 import QtCore, QtGui
from Puntajes import Ui_Puntajes

class MyformPuntaje(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.uiP = Ui_Puntajes()
        self.uiP.setupUi(self)
        self.connect(self.uiP.pVolver, QtCore.SIGNAL("clicked()"), self.volverVentana)
        
    def setPuntajes(self):
        self.valores = QtCore.QStringList()
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
                
                self.valorC =QtCore.QStringList()
                self.valorC = self.crono.split(":")
                self.mim = self.valorC[0].toDouble()
                self.seg = self.valorC[1].toDouble()
                self.mseg = self.valorC[2].toDouble()
                
                self.puntaje = 0
                
                if (self.nivelC == "Juvenil"):
                    self.puntaje = 90*(self.min+self.seg+self.mseg)/3
                elif (self.nivelC == "Profesional"):
                    self.puntaje = 90*(self.min+self.seg+self.mseg)/2
                elif (self.nivelC == "Experto"):
                    self.puntaje = 90*(self.min+self.seg+self.mseg)
                
                self.str = QtCore.QString(self.puntaje)
                self.uiP.textPuntajes.toPlainText(self.nomJugador.toUpper()+"\t"+self.nivelC+"\t\t"+self.str+"\n")
                self.uiP.textPuntajes.setDisabled(True)
            
    def setVentanaPrincipal(self, v):
        self.principal = v

    def volverVentana(self):
        self.hide()
        self.principal.show()
