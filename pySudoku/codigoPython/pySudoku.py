from Sudoku import Ui_sudoku
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTimer, QString
from pyCargarS import MyformCargarSudoku
import exceptions
from random import randint
import math

plantilla1 = QtCore.QString("7,8,4,9,5,2,3,1,6,9,2,6,1,4,3,8,5,7,3,5,1,8,6,7,9,4,2,4,7,8,5,2,1,6,9,3,1,6,5,3,7,9,2,8,4,2,9,3,6,8,4,1,7,5,6,4,9,2,1,5,7,3,8,5,1,2,7,3,8,4,6,9,8,3,7,4,9,6,5,2,1")
plantilla2 = QtCore.QString("5,9,7,4,3,2,6,1,8,2,8,4,1,6,7,3,9,5,6,3,1,8,9,5,2,4,7,4,5,3,6,7,1,9,8,2,8,7,9,2,5,3,4,6,1,1,6,2,9,4,8,5,7,3,9,2,5,7,1,6,8,3,4,7,4,8,3,2,9,1,5,6,3,1,6,5,8,4,7,2,9")
plantilla3 = QtCore.QString("1,7,4,6,8,3,2,9,5,9,5,3,4,1,2,8,6,7,2,8,6,7,9,5,3,4,1,8,6,5,2,7,9,1,3,4,4,3,2,8,6,1,7,5,9,7,1,9,5,3,4,6,8,2,3,9,8,1,4,7,5,2,6,5,4,1,3,2,6,9,7,8,6,2,7,9,5,8,4,1,3")
valores = QtCore.QStringList()
matrizGuardar = []
class MyformSudoku(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.uiS = Ui_sudoku()
        self.uiS.setupUi(self)
        # **********TABLERO**********
        self.listaCeldas = []
        self.initGui()
        # ***************************
        #self.encriptarS()
        self.desabilitarBotones()
        
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
        
    def desabilitarBotones(self):
        #*******Desabilitar todos los Botones*******
        self.uiS.cargarJuego.setDisabled(False)
        self.uiS.guardarJuego.setDisabled(True)
        self.uiS.verificar.setDisabled(True)
        self.uiS.comprobar.setDisabled(True)
        self.uiS.borrarJuego.setDisabled(True)
        self.uiS.resolverJuego.setDisabled(True)

    def habilitarBotones(self):
        #*******Habilitar todos los Botones*******
        self.uiS.cargarJuego.setDisabled(True)
        self.uiS.guardarJuego.setDisabled(False)
        self.uiS.verificar.setDisabled(False)
        self.uiS.comprobar.setDisabled(False)
        self.uiS.borrarJuego.setDisabled(False)
        self.uiS.resolverJuego.setDisabled(False)
        
    def toInt(self,num):
    ##Convierte un String a Int 
        try:
            return int(num)
        except exceptions.ValueError:
            return 0
        
    ## Funcion de crear Tablero con QTextEdit
    def initGui(self): 
        for i in range(9):
            for j in range(9):
                self.num = (i*9)+j
                self.celda = QtGui.QTextEdit(self.uiS.gridLayoutWidget)
                self.listaCeldas.append(self.celda)
                self.uiS.numberPad.addWidget(self.celda, i,j,1,1)
                QtCore.QObject.connect(self.listaCeldas[self.num], QtCore.SIGNAL("textChanged(QString)"), self.correccionInGame)
                
        self.pintarTablero()


    ##Pintar Tablero
    def pintarTablero(self):
        for i in range(9):
            for j in range(9):
                self.num = (i*9)+j
                #Si coincide la respuesta se pintara azul sino coincide se pintara de rojo el cuadro
                self.indi = i / 3
                self.indj = j / 3
                
                if((self.indi == self.indj) or ((self.indi+self.indj) == 2)):
                    self.paleta = self.listaCeldas[self.num].palette()
                    self.paleta.setColor(QtGui.QPalette.Base, QtGui.QColor(170, 170, 255))
                    self.listaCeldas[self.num].setPalette(self.paleta)
                else:
                    self.paleta = self.listaCeldas[self.num].palette()
                    self.paleta.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 255, 255))
                    self.listaCeldas[self.num].setPalette(self.paleta)                
                    
    #Actualizar Cronometro
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

    #Setear datos de Cargar Partida
    def setCargar(self, datos, nivel, cronometro, nombre):
        self.datosCargados = datos
        self.cuenta = 0
        self.cont = 33
        self.valores = self.datosCargados.split(",")
        
        for i in range(9):
            for j in range(9):
                self.num = (i*9)+j
                self.val = ord(str(self.valores[self.cuenta]))
                print(self.val)
                if(int(self.val) == 33):
                    self.listaCeldas[self.num].setDisabled(False)
                    self.listaCeldas[self.num].setText("")
                else:
                    #Desencripta Pantilla del sudoku
                    if(self.toInt(self.val)%2 == 0):
                        self.opera = math.sqrt(self.toInt(self.val) - self.cont)
                    else:
                        self.opera = math.sqrt(2 * (self.toInt(self.val) - self.cont))
                    
                    self.listaCeldas[self.num].setTextColor(QtCore.Qt.blue)
                    self.listaCeldas[self.num].setText(QtCore.QString.number(self.opera))
                    self.listaCeldas[self.num].setDisabled(True)
                self.listaCeldas[self.num].setAlignment(QtCore.Qt.AlignRight)
                self.cuenta += 1
        self.uiS.textJugador.setText(nombre)
        self.uiS.textJugador.setEnabled(False)
        self.uiS.textNivel.setText(nivel)
        self.uiS.textNivel.setEnabled(False)
        
        self.valor = cronometro.split(":")
        self.minutos = self.toInt(self.valor[0])
        self.segundos = self.toInt(self.valor[1])
        self.milisegundos = self.toInt(self.valor[2])
        
        self.min = self.minutos
        self.seg = self.segundos
        self.miliseg = self.milisegundos
        
        self.inicialtiempo()
        self.show()      

    ## Boton comprobrar


    def comprobar(self):
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
            self.timer.stop()
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
        if ( self.obtenervalor == 0):
            return 0
        else:
            return(self.toInt((self.listaCeldas[self.num].toPlainText())))
    
    ##Juego Nuevo
    def iniciarJuego(self):
        self.habilitarBotones()
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
                    if(self.aleatorio <= 3):
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
           
    def obtenerNombreNivel(self, nombre, nivel):
        self.uiS.textJugador.setText(QString("%1").arg(nombre))
        self.uiS.textJugador.setEnabled(False)
        self.uiS.textNivel.setText(QString("%1").arg(nivel))
        self.uiS.textNivel.setEnabled(False) 
    
    def Salir(self):
        exit()

    def borrarJueg(self):
        self.desabilitarBotones()
        self.timer.stop()
        
        self.uiS.lcdmin.display(QString("%1").arg("0"))
        self.uiS.lcdseg.display(QString("%2").arg("0"))
        self.uiS.lcdmsg.display(QString("%3").arg("0"))
        
        for i in range(9):
            for j in range(9):
                self.num = (i*9)+j
                self.listaCeldas[self.num].setText("")
        
    def CargarJuego(self):
        self.cont = 0
        #self.comboB = QtGui.QComboBox()
        self.cargarS = MyformCargarSudoku()
        self.bandera = 0
        self.mFilename = QtCore.QString("guardar.txt")
        
        self.mFile = QtCore.QFile(self.mFilename)
        if(self.mFile.exists()):
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
                
                if (self.uiS.textNivel.text() == self.nivelC):
                    self.bandera += 1#
                    #self.comboB.addItem(self.nomJugador)
                #self.cont +=1
            if(self.bandera != 0):
                self.hide()
            #self.jugador = (self.uiS.textJugador.text())
                self.nivel = self.uiS.textNivel.text()
                print(self.nivel)
            #self.cargarS.setCombo(self.comboB, self.cont, self.jugador, self.nivel)
                self.cargarS.ventanaCargar(self)
                self.cargarS.obtenerPartidasGuardadas(self.nivel)
                self.cargarS.show()
            else:
                QtGui.QMessageBox.information(self, "MENSAJE", "No existen Partidas Guardadas \nde nivel "+self.uiS.textNivel.text(), "ACEPTAR")
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
        
        #Actualizar la matriz
        for i in range(9):
            for j in range(9):
                self.num = (i*9)+j
                
                matrizGuardar.append(self.listaCeldas[self.num].toPlainText())
                if (matrizGuardar[self.num] != ""): self.banderaGuardar = 1
        
        if (self.banderaGuardar == 0):
            QtGui.QMessageBox.information(self, "Guardar-Sudoku", "No existen datos a GUARDAR", "ACEPTAR")
        else:
            self.encriptarS()
            for i in range(9):
                for j in range(9):
                    self.num = (i*9)+j
                    self.info = self.info+matrizGuardar[self.num]+","
            
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
        if(self.niveles == "Profesional"):  self.valores = plantilla2.split(",")
        if(self.niveles == "Experto"):  self.valores = plantilla3.split(",")
        
        for i in range(9):
            for j in range(9):
                self.num = (i*9)+j
                self.celda = self.listaCeldas[self.num]
                if((self.celda.isEnabled()) and (self.getDisplayValue(i,j) != 0) and (self.getDisplayValue(i,j) != (self.toInt(self.valores[self.cont])))):
                    self.paleta = self.celda.palette()
                    self.paleta.setColor(QtGui.QPalette.Base, QtGui.QColor(255,150,150))
                    self.celda.setPalette(self.paleta)
                    
                if((self.celda.isEnabled()) and (self.getDisplayValue(i,j) != 0) and (self.getDisplayValue(i,j) == (self.toInt(self.valores[self.cont])))):
                    self.paleta = self.celda.palette()
                    self.paleta.setColor(QtGui.QPalette.Base, QtGui.QColor(120,255,120))
                    self.celda.setPalette(self.paleta)
                self.cont += 1
    
    #Encriptar Partida de Sudoku
    def encriptarS(self):
        self.cont = 33
        self.num1 = 0
        self.numT = 0
        
        for i in range(9):
            for j in range(9):
                self.num = (i*9)+j
                
                self.var = self.toInt(matrizGuardar[self.num])
                self.num1 = (self.var * self.var)
                
                if ((self.toInt( matrizGuardar[self.num] )%2) == 0 ):
                    self.numT = (self.num1/2) + self.cont 
                else:
                    self.numT = self.num1 + self.cont
                matrizGuardar[self.num] = (str(chr(self.numT)))
                print("Prueba: "+str(chr(self.numT))+"  "+str(self.numT))

    #Correccion Cuadrante
    def CorreccionCuadrante(self,i,j):
        self.num = (i*9)+j
        self.despx = (i/3) * 3
        self.despy = (j/3) * 3
        
        for self.despx in range(self.despx + 3):
            for self.despy in range(self.despy + 3):
                self.num1 = (self.despx * 3) + 3
                if ((self.despy != i) and (self.despx != j)):
                    if(self.getDisplayValue(i, j) == self.getDisplayValue(self.despx, self.despy)):
                        self.paleta = self.listaCeldas[self.num].palette()
                        self.paleta.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 150, 150))
                        self.listaCeldas[self.num].setPalette(self.paleta)
                        self.listaCeldas[self.num1].setPalette(self.paleta)
                        QtGui.QMessageBox.information(self, "Advertencia", "Este numero ya fue ingresado en el cuadrante")
                        return
                    else:
                        self.pintarTablero()
                        
    #Correccion Columna                
    def CorreccionColumna(self, i, j):
        self.num = (i*9)+j
        for k in range(9):
            self.num1 = (k*9)+j
            if(k != i):
                if(self.getDisplayValue(i, j) == self.getDisplayValue(k, j)):
                    self.paleta = self.listaCeldas[self.num].palette()
                    self.paleta.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 150, 150))
                    self.listaCeldas[self.num].setPalette(self.paleta)
                    self.listaCeldas[self.num1].setPalette(self.paleta)
                    QtGui.QMessageBox.information(self, "Advertencia", "Este numero ya fue ingresado en la columna")
                    return
                else:
                    self.pintarTablero()
                
    #Correccion Fila
    def CorreccionFila(self, i, j):
        self.num = (i*9)+j
        for k in range(9):
            self.num1 = (i*9)+k
            if(k != j):
                if(self.getDisplayValue(i, j) == self.getDisplayValue(i, k)):
                    self.paleta = self.listaCeldas[self.num].palette()
                    self.paleta.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 150, 150))
                    self.listaCeldas[self.num].setPalette(self.paleta)
                    self.listaCeldas[self.num1].setPalette(self.paleta)
                    QtGui.QMessageBox.information(self, "Advertencia", "Este numero ya fue ingresado en la fila")
                    return
                else:
                    self.pintarTablero()
             

    def correccionInGame(self):
        self.numberTextTemp = QtGui.QTextEdit()
        self.numberTextTemp = self.sender()
        
        self.inputNumber = self.toInt(self.numberTextTemp.toPlainText())
        if ((self.inputNumber>9  or  self.inputNumber<1) and (self.inputNumber != None)):
            QtGui.QMessageBox.information(self, "Advertencia", "El numero ingresado no es valido esta fuera del rango")
            self.numberTextTemp.setText("")
        
        for  i in range(9):
            for j in range(9):
                self.num = (i*9)+j
                if(((self.getDisplayValue(i, j) != 0) and self.listaCeldas[self.num].isEnabled())):
                    self.CorreccionFila(i, j)
                    self.CorreccionColumna(i, j)
                    self.CorreccionCuadrante(i, j)
                    
            
        