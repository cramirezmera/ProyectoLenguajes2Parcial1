from Sudoku import Ui_sudoku, _fromUtf8
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTimer, QString
from pyCargarS import MyformCargarSudoku
import exceptions
import random
from random import randint

plantilla1 = QtCore.QString("7,8,4,9,5,2,3,1,6,9,2,6,1,4,3,8,5,7,3,5,1,8,6,7,9,4,2,4,7,8,5,2,1,6,9,3,1,6,5,3,7,9,2,8,4,2,9,3,6,8,4,1,7,5,6,4,9,2,1,5,7,3,8,5,1,2,7,3,8,4,6,9,8,3,7,4,9,6,5,2,1")
plantilla2 = QtCore.QString("5,9,7,4,3,2,6,1,8,2,8,4,1,6,7,3,9,5,6,3,1,8,9,5,2,4,7,4,5,3,6,7,1,9,8,2,8,7,9,2,5,3,4,6,1,1,6,2,9,4,8,5,7,3,9,2,5,7,1,6,8,3,4,7,4,8,3,2,9,1,5,6,3,1,6,5,8,4,7,2,9")
plantilla3 = QtCore.QString("1,7,4,6,8,3,2,9,5,9,5,3,4,1,2,8,6,7,2,8,6,7,9,5,3,4,1,8,6,5,2,7,9,1,3,4,4,3,2,8,6,1,7,5,9,7,1,9,5,3,4,6,8,2,3,9,8,1,4,7,5,2,6,5,4,1,3,2,6,9,7,8,6,2,7,9,5,8,4,1,3")
valores = QtCore.QStringList()

class MyformSudoku(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.uiS = Ui_sudoku()
        self.uiS.setupUi(self)
        # **********TABLERO**********
        self.listaCeldas = []
        self.initGui()
        # ***************************
        
        #Cargar Partida
        self.connect(self.uiS.cargarJuego, QtCore.SIGNAL("clicked()"), self.CargarJuego)
        #Salir del sudoku
        self.connect(self.uiS.salir, QtCore.SIGNAL("clicked()"), self.Salir)
        #iniciar juego
        self.connect(self.uiS.nuevoJuego, QtCore.SIGNAL("clicked()"), self.iniciarJuego)
        #comprobar juego
        self.connect(self.uiS.comprobar, QtCore.SIGNAL("clicked()"), self.comprobar)
        #Limpiar tablero
        self.connect(self.uiS.borrarJuego, QtCore.SIGNAL("clicked()"), self.borrarJueg)
        #Resolver Juego
        self.connect(self.uiS.resolverJuego, QtCore.SIGNAL("clicked()"), self.resolverJueg)
        #Verificar (HACER TRAMPA)
        self.connect(self.uiS.verificar, QtCore.SIGNAL("clicked()"), self.verificarJuego)
        #Guardar
        self.connect(self.uiS.guardarJuego, QtCore.SIGNAL("clicked()"), self.guardarJueg)
        
    ##Convierte un String a Int 
    def toInt(self,num):
        try:
            return int(num)
        except exceptions.ValueError:
            return None
        
    ## Funcion de crear Tablero con QTextEdit
    def initGui(self): 
        for i in range(9):
            for j in range(9):
                self.celda = QtGui.QTextEdit(self.uiS.gridLayoutWidget)
                self.listaCeldas.append(self.celda)
                self.uiS.numberPad.addWidget(self.celda, i,j,1,1)
                
    ## Boton comprobrar
    def comprobar(self):
        self.sumatoriah = 0
        self.productoh = 1
        self.sumatoriav = 0
        self.productov = 1
        self.sumatoriacuad = 0
        self.productocuad = 1
        self.despx = 0
        self.despy = 0
        self.banderavalida = 1
        
        #Validacion numeros del 1 al 9 en las filas
        for i in range(9):
            self.sumatoriah = 0
            self.productoh = 1
            for j in range(9):
                self.sumatoriah = self.sumatoriah + self.getDisplayValue(i, j)
                self.productoh = self.productoh * self.getDisplayValue(i, j)
            if((self.sumatoriah == 45) and (self.productoh == 362880)):
                self.banderavalida = 1
            else:
                self.banderavalida = 0
                break
        #Validacion numeros del 1 al 9 en las columnas
        for j in range(9):
            self.sumatoriav = 0
            self.productov = 1
            for i in range(9):
                self.sumatoriav = self.sumatoriav + self.getDisplayValue(i, j)
                self.productov = self.productov * self.getDisplayValue(i, j)
            if((self.sumatoriav == 45) and (self.productov == 362880)):
                self.banderavalida = 1
            else:
                self.banderavalida = 0
                break
        for x in range(9):
            self.sumatoriacuad = 0
            self.productocuad = 1
            self.despx = (x/3)*3
            self.despy = (x%3)*3
            
            for i in range(3):
                for j in range(3):
                    self.sumatoriacuad = self.sumatoriacuad + self.getDisplayValue(i+self.despx, j+self.despy)
                    self.productocuad = self.productocuad * self.getDisplayValue(i+self.despx, j+self.despy)
            
            if((self.sumatoriacuad == 45) and (self.productocuad == 362880)):
                self.banderavalida = 1
            else:
                self.banderavalida = 0
                break
        
        #comprobacion de validacion en general
        if (self.banderavalida == 1):
            QtGui.QMessageBox.information(self,"Respuesta", "La solucion es valida")
        else:
            QtGui.QMessageBox.information(self,"Respuesta", "La solucion no es valida")            
    
    ##Seter un entero al QTextEdit
    def setDisplayValue(self, i, j, v):
        self.num = (i*9)+j
        self.listaCeldas[self.num].setText(QString("%1").arg(v))
        self.listaCeldas[self.num].SetAlignment(QtCore.Qt.AlignRight)
    
    ##Obtener un entero al QTextEdit
    def getDisplayValue(self, i, j):
        self.num = (i*9)+j
        self.obtenervalor = self.toInt((self.listaCeldas[self.num].toPlainText()))
        if ( self.obtenervalor == None):
            return 0
        else:
            return(self.toInt((self.listaCeldas[self.num].toPlainText())))
    
    ##Juego Nuevo
    def iniciarJuego(self):
        self.cont = 0
        self.aleatorio = 0
        self.miliseg = 0
        self.seg = 0
        self.min = 0
        
        ##Semilla del aleatorio#
        self.seed = QtCore.QTime()
        self.seed.start()
        QtCore.qsrand(self.seed.msec())
        self.niveles = self.uiS.textNivel.text()
        
        if(self.niveles == "Juvenil"):  self.valores = plantilla1.split(",")
        elif(self.niveles == "Profesional"):  self.valores = plantilla2.split(",")
        elif(self.niveles == "Experto"):  self.valores = plantilla3.split(",")
        
        for i in range(9):
            for j in range(9):
                self.num = (i*9)+j
                self.aleatorio = randint(0,10)
                
                if(self.niveles == "Juvenil"):
                    if(self.aleatorio <= 6):
                        self.listaCeldas[self.num].setTextColor(QtCore.Qt.blue)
                        self.listaCeldas[self.num].setText(self.valores[self.cont])
                        self.listaCeldas[self.num].setDisabled(True)
                    else:
                        self.listaCeldas[self.num].setDisabled(False)
                        self.listaCeldas[self.num].setText("")
                elif(self.niveles == "Profesional"):
                    if(self.aleatorio <= 4):
                        self.listaCeldas[self.num].setTextColor(QtCore.Qt.blue)
                        self.listaCeldas[self.num].setText(self.valores[self.cont])
                        self.listaCeldas[self.num].setDisabled(True)
                    else:
                        self.listaCeldas[self.num].setDisabled(False)
                        self.listaCeldas[self.num].setText("")
                elif(self.niveles == "Experto"):
                    if(self.aleatorio <= 2):
                        self.listaCeldas[self.num].setTextColor(QtCore.Qt.blue)
                        self.listaCeldas[self.num].setText(self.valores[self.cont])
                        self.listaCeldas[self.num].setDisabled(True)
                    else:
                        self.listaCeldas[self.num].setDisabled(False)
                        self.listaCeldas[self.num].setText("")
                self.listaCeldas[self.num].setAlignment(QtCore.Qt.AlignRight)
                self.cont += 1
        
        self.inicialtiempo()    #Reemplaza a update

    def resolverJueg(self):
        self.cont = 0   
        self.niveles = self.uiS.textNivel.text()
        self.timer.stop()
        
        if(self.niveles == "Juvenil"):  self.valores = plantilla1.split(",")
        elif(self.niveles == "Profesional"):  self.valores = plantilla2.split(",")
        elif(self.niveles == "Experto"):  self.valores = plantilla3.split(",")
        
        for i in range(9):
            for j in range(9):
                self.num = (i*9)+j
                if(self.listaCeldas[self.num].isEnabled()):
                    self.listaCeldas[self.num].setDisabled(True)
                    self.listaCeldas[self.num].setText(self.valores[self.cont])
                    self.listaCeldas[self.num].setAlignment(QtCore.Qt.AlignRight)
                self.cont +=1        
             
    #Inicializar las variables para el cronometro
    def inicialtiempo(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start(10)
        self.min=0
        self.seg=0
        self.miliseg=0
        self.timer.timeout.connect(self.update)
        
    def update(self):
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
    
    def Salir(self):
        exit()

    def borrarJueg(self):
        for i in range(9):
            for j in range(9):
                self.num = (i*9)+j
                self.listaCeldas[self.num].setText("")
        
    def CargarJuego(self):
        self.cont = 0
        self.comboB = QtGui.QComboBox()
        self.cargarS = MyformCargarSudoku()
        self.cargarS.ventanaCargar(self)
              
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
                self.cont +=1
            self.hide()
            self.jugador = QtCore.QString(self.uiS.textJugador.text())
            self.nivel = QtCore.QString(self.uiS.textNivel.text())
            self.cargarS.setCombo(self.comboB, self.cont, self.jugador, self.nivel)
            self.cargarS.show()
        else:
            QtGui.QMessageBox.information(self, "MENSAJE", "No existen Partidas Guardadas", "ACEPTAR")

    #GuardarPartida
    def guardarJueg(self):
        self.timer.stop()
        self.nomJugador = self.uiS.textJugador.text()
        self.nivel = self.uiS.textNivel.text()
        self.sMin = QtCore.QString.number(self.uiS.lcdmin.intValue())
        self.sSeg = QtCore.QString.number(self.uiS.lcdseg.intValue())
        self.sMiliseg = QtCore.QString.number(self.uiS.lcdmsg.intValue())
        self.info = ""
        self.banderaGuardar = 0
        self.matrizGuardar = []
        #Actualizar la matriz
        for i in range(9):
            for j in range(9):
                self.num = (i*9)+j
                
                self.matrizGuardar.append(self.listaCeldas[self.num].toPlainText())
                if (self.matrizGuardar[self.num] != ""): self.banderaGuardar = 1
        
        if (self.banderaGuardar == 0):
            QtGui.QMessageBox.information(self, "Guardar-Sudoku", "No existen datos a GUARDAR", "ACEPTAR")
        else:
            #encriptarS()
            for i in range(9):
                for j in range(9):
                    self.num = (i*9)+j
                    self.info = self.info+self.matrizGuardar[self.num]+","
            
            self.mFilename = QtCore.QString("guardar.txt")
            self.mFile = QtCore.QFile(self.mFilename)
            self.mFile.open(QtCore.QIODevice.Text | QtCore.QIODevice.Append)
            if not(self.mFile.isOpen()):    
                return
            
            self.txtstr = QtCore.QTextStream(self.mFile)
            self.txtstr << self.nomJugador+"/"+self.nivel+"/"+self.sMin+":"+self.sSeg+":"+self.sMiliseg+"/"+self.info+"\n"
            self.mFile.flush()
            self.mFile.close()
            
            QtGui.QMessageBox.information(self, "Guardar-Sudoku", "La partida ha sido guardada \nJUGADOR: "+self.nomJugador.toUpper(),"ACEPTAR")
            self.hide()
        
    #Verificar (Hacer trampa)
    def verificarJuego(self):
        self.cont = 0
        self.niveles  = self.uiS.textNivel.text()
        
        if(self.niveles == "Juvenil"):  self.valores = plantilla1.split(",")
        elif(self.niveles == "profesional"):  self.valores = plantilla2.split(",")
        elif(self.niveles == "Experto"):  self.valores = plantilla3.split(",")
        
        for i in range(9):
            for j in range(9):
                self.num = (i*9)+j
                self.celda = self.listaCeldas[self.num]
                if((self.celda.isEnabled()) and (self.getDisplayValue(i, j) != 0) and (self.getDisplayValue(i, j) != (self.valores[self.cont].toLong()))):
                    self.paleta = self.listaCeldas[self.num].palette()
                    self.paleta.setColor(QtGui.QPalette.Base, QtGui.QColor(255,150,150))
                    self.listaCeldas[self.num].setPalette(self.paleta)
                    
                if((self.celda.isEnabled()) and (self.getDisplayValue(i, j) != 0) and (self.getDisplayValue(i, j) == (self.valores[self.cont].toLong()))):
                    self.paleta = self.listaCeldas[self.num].palette()
                    self.paleta.setColor(QtGui.QPalette.Base, QtGui.QColor(255,150,120))
                    self.listaCeldas[self.num].setPalette(self.paleta)
                self.cont += 1
        
        
        