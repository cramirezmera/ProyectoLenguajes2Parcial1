from Sudoku import Ui_sudoku
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTimer, QString
from pyCargarS import MyformCargarSudoku


class MyformSudoku(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.uiS = Ui_sudoku()
        self.uiS.setupUi(self)
        self.initGui()
        
        #Cargar Partida
        self.connect(self.uiS.cargarJuego, QtCore.SIGNAL("clicked()"), self.CargarJuego)
        #Salir del sudoku
        self.connect(self.uiS.salir, QtCore.SIGNAL("clicked()"), self.funcionSalir)
        #iniciar juego
        self.connect(self.uiS.nuevoJuego, QtCore.SIGNAL("clicked()"), self.iniciarJuego)
        
    def initGui(self): 
        self.text = [[]]
        for i in range(9):
            for j in range(9):
                self.valor = QtGui.QTextEdit()
                self.text.append(self.valor)
                self.uiS.numberPad.addWidget(self.valor, i, j)   
              
        
    def iniciarJuego(self):
        self.inicialtiempo()
        
    def inicialtiempo(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start(10)
        self.min=0
        self.seg=0
        self.miliseg=0
        self.timer.timeout.connect(self.tiempoFuera)
        
    def tiempoFuera(self):
        self.miliseg= self.miliseg+1
        if self.seg < 60:
            if self.miliseg >= 100:
                self.miliseg = 0
                self.seg = self.seg+1
        elif self.seg >= 60:
            self.seg = 0
            self.min = self.min+1
        
        self.uiS.lcdmin.display(QString("%1").arg(self.min))
        self.uiS.lcdseg.display(QString("%2").arg(self.seg))
        self.uiS.lcdmsg.display(QString("%3").arg(self.miliseg))    
    
    def obtenerNombreNivel(self, nombre, nivel):
        self.uiS.textJugador.setText(QString("%1").arg(nombre))
        self.uiS.textJugador.setEnabled(False)
        self.uiS.textNivel.setText(QString("%1").arg(nivel))
        self.uiS.textNivel.setEnabled(False)
        
    def funcionSalir(self):
        exit()

    def CargarJuego(self):
        self.cont = 0
        self.comboB = QtGui.QComboBox()
        self.cargarS = MyformCargarSudoku()
        self.cargarS.ventanaCargar(self)
        
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
                
                if (self.uiS.textNivel.text() == self.nivelC):
                    self.comboB.addItem(self.nomJugador)
                self.cont = self.cont+1
            self.hide()
            self.jugador = QtCore.QString(self.uiS.textJugador.text())
            self.nivel = QtCore.QString(self.uiS.textNivel.text())
            self.cargarS.setCombo(self.comboB, self.cont, self.jugador, self.nivel)
            self.cargarS.show()
        else:
            QtGui.QMessageBox.information(self, "MENSAJE", "No existen Partidas Guardadas", "ACEPTAR")
