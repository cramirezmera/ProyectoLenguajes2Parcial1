from Sudoku import Ui_sudoku
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTimer, QString
from codigoCargarS import MyformCargarSudoku


class MyformSudoku(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.uiS = Ui_sudoku()
        self.uiS.setupUi(self)
        self.initGui()
        
        #Cargar Partida
        self.connect(self.uiS.cargarJuego, QtCore.SIGNAL("clicked()"), self.funcionCargar)
        #Salir del sudoku
        self.connect(self.uiS.salir, QtCore.SIGNAL("clicked()"), self.funcionSalir)
        #iniciar juego
        self.connect(self.uiS.nuevoJuego, QtCore.SIGNAL("clicked()"), self.iniciarJuego)
        
    def initGui(self): 
        self.text = []
        for i in range(9):
            for j in range(9):
                
                self.valor = QtGui.QTextEdit(None)
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

    def funcionCargar(self):
        self.hide()
        self.cargarS = MyformCargarSudoku()
        self.cargarS.setCargar(self)
        self.cargarS.show()
