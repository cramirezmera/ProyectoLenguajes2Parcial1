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
        
    def toInt(self,cadena):
    ##Convierte un String a Int 
        try:
            print(type(""+cadena))
            return int(cadena)
        except exceptions.ValueError:
            return 0
        
    ## Funcion de crear Tablero con QTextEdit
    def initGui(self): 
        for i in range(9):
            for j in range(9):
                num = (i*9)+j
                celda = QtGui.QTextEdit(self.uiS.gridLayoutWidget)
                self.listaCeldas.append(celda)
                self.listaCeldas[num].setDisabled(True)
                self.uiS.numberPad.addWidget(celda, i,j)
                
                self.listaCeldas[num].textChanged.connect(self.correccionInGame)
                
        self.pintarTablero()


    ##Pintar Tablero
    def pintarTablero(self):
        for i in range(9):
            for j in range(9):
                num = (i*9)+j
                #Si coincide la respuesta se pintara azul sino coincide se pintara de rojo el cuadro
                indi = i / 3
                indj = j / 3
                
                if((indi == indj) or ((indi + indj) == 2)):
                    paleta = self.listaCeldas[num].palette()
                    paleta.setColor(QtGui.QPalette.Base, QtGui.QColor(170, 170, 255))
                    self.listaCeldas[num].setPalette(paleta)
                else:
                    paleta = self.listaCeldas[num].palette()
                    paleta.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 255, 255))
                    self.listaCeldas[num].setPalette(paleta)                
                    
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
        datosCargados = datos
        cuenta = 0
        cont = 33
        valores = datosCargados.split(",")
        
        for i in range(9):
            for j in range(9):
                num = (i*9)+j
                val = ord(str(valores[cuenta]))
                if(int(val) == 33):
                    self.listaCeldas[num].setDisabled(False)
                    self.listaCeldas[num].setText("")
                else:
                    #Desencripta Pantilla del sudoku
                    if(self.toInt(val)%2 == 0):
                        opera = math.sqrt(self.toInt(val) - cont)
                    else:
                        opera = math.sqrt(2 * (self.toInt(val) - cont))
                    
                    self.listaCeldas[num].setTextColor(QtCore.Qt.blue)
                    self.listaCeldas[num].setText(QtCore.QString.number(opera))
                    self.listaCeldas[num].setDisabled(True)
                self.listaCeldas[num].setAlignment(QtCore.Qt.AlignRight)
                cuenta += 1
        self.uiS.textJugador.setText(nombre)
        self.uiS.textJugador.setEnabled(False)
        self.uiS.textNivel.setText(nivel)
        self.uiS.textNivel.setEnabled(False)
        
        valor = cronometro.split(":")
        minutos = self.toInt(valor[0])
        segundos = self.toInt(valor[1])
        milisegundos = self.toInt(valor[2])
        
        self.min = minutos
        self.seg = segundos
        self.miliseg = milisegundos
        
        self.inicialtiempo()
        self.show()      

        ## Boton comprobrar
    def comprobar(self):
        banderavalida = 1
        
        #Validacion numeros del 1 al 9 en las filas
        for i in range(9):
            sumatoriah = 0
            productoh = 1
            for j in range(9):
                sumatoriah = sumatoriah + self.getDisplayValue(i, j)
                productoh = productoh * self.getDisplayValue(i, j)
            if((sumatoriah == 45) and (productoh == 362880)):
                banderavalida = 1
            else:
                banderavalida = 0
                break
        #Validacion numeros del 1 al 9 en las columnas
        for j in range(9):
            sumatoriav = 0
            productov = 1
            for i in range(9):
                sumatoriav += self.getDisplayValue(i, j)
                productov *=  self.getDisplayValue(i, j)
            if((sumatoriav == 45) and (productov == 362880)):
                banderavalida = 1
            else:
                banderavalida = 0
                break
        for x in range(9):
            sumatoriacuad = 0
            productocuad = 1
            despx = (x/3)*3
            despy = (x%3)*3
            
            for i in range(3):
                for j in range(3):
                    sumatoriacuad = sumatoriacuad + self.getDisplayValue(i+despx, j+despy)
                    productocuad = productocuad * self.getDisplayValue(i+despx, j+despy)
            
            if((sumatoriacuad == 45) and (productocuad == 362880)):
                banderavalida = 1
            else:
                self.banderavalida = 0
                break
        
        #comprobacion de validacion en general
        if (banderavalida == 1):
            self.timer.stop()
            QtGui.QMessageBox.information(self,"Respuesta", "La solucion es valida")
        else:
            QtGui.QMessageBox.information(self,"Respuesta", "La solucion no es valida")            
    
    ##Seter un entero al QTextEdit
    def setDisplayValue(self, i, j, v):
        num = (i*9)+j
        self.listaCeldas[num].setText(QString("%1").arg(v))
        self.listaCeldas[num].SetAlignment(QtCore.Qt.AlignRight)

    ##Obtener un entero al QTextEdit
    def getDisplayValue(self, i, j):
        num = (i*9)+j
        obtenervalor = self.toInt((self.listaCeldas[num].toPlainText()))
        return obtenervalor
    
    ##Juego Nuevo
    def iniciarJuego(self):
        self.habilitarBotones()
        cont = 0
        aleatorio = 0
        self.miliseg = 0
        self.seg = 0
        self.min = 0
        
        ##Semilla del aleatorio#
        seed = QtCore.QTime()
        seed.start()
        QtCore.qsrand(seed.msec())
        niveles = self.uiS.textNivel.text()
        
        if(niveles == "Juvenil"):  self.valores = plantilla1.split(",")
        elif(niveles == "Profesional"):  self.valores = plantilla2.split(",")
        elif(niveles == "Experto"):  self.valores = plantilla3.split(",")
        
        for i in range(9):
            for j in range(9):
                num = (i*9)+j
                aleatorio = randint(0,10)
                
                if(niveles == "Juvenil"):
                    if(aleatorio <= 6):
                        self.listaCeldas[num].setTextColor(QtCore.Qt.blue)
                        self.listaCeldas[num].setText(self.valores[cont])
                        self.listaCeldas[num].setDisabled(True)
                    else:
                        self.listaCeldas[num].setDisabled(False)
                        self.listaCeldas[num].setText("")
                elif(niveles == "Profesional"):
                    if(aleatorio <= 4):
                        self.listaCeldas[num].setTextColor(QtCore.Qt.blue)
                        self.listaCeldas[num].setText(self.valores[cont])
                        self.listaCeldas[num].setDisabled(True)
                    else:
                        self.listaCeldas[num].setDisabled(False)
                        self.listaCeldas[num].setText("")
                elif(niveles == "Experto"):
                    if(aleatorio <= 3):
                        self.listaCeldas[num].setTextColor(QtCore.Qt.blue)
                        self.listaCeldas[num].setText(self.valores[cont])
                        self.listaCeldas[num].setDisabled(True)
                    else:
                        self.listaCeldas[num].setDisabled(False)
                        self.listaCeldas[num].setText("")
                self.listaCeldas[num].setAlignment(QtCore.Qt.AlignRight)
                cont += 1
        
        self.inicialtiempo()    #Reemplaza a update

    def resolverJueg(self):
        ######Desabilito el boton Guardar######
        self.uiS.guardarJuego.setDisabled(True)
        #######################################
        
        cont = 0   
        niveles = self.uiS.textNivel.text()
        self.timer.stop()
        
        if(niveles == "Juvenil"):  self.valores = plantilla1.split(",")
        elif(niveles == "Profesional"):  self.valores = plantilla2.split(",")
        elif(niveles == "Experto"):  self.valores = plantilla3.split(",")
        
        for i in range(9):
            for j in range(9):
                num = (i*9)+j
                if(self.listaCeldas[num].isEnabled()):
                    self.listaCeldas[num].setDisabled(True)
                    self.listaCeldas[num].setText(self.valores[cont])
                    self.listaCeldas[num].setAlignment(QtCore.Qt.AlignRight)
                cont +=1        
             
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
        #QtGui.QMessageBox.information(QWidget, QString, QString, buttons=QMessageBox_Ok, defaultButton=QMessageBox_NoButton)
        exit()

    def borrarJueg(self):
        self.desabilitarBotones()
        self.timer.stop()
        
        self.uiS.lcdmin.display(QString("%1").arg("0"))
        self.uiS.lcdseg.display(QString("%2").arg("0"))
        self.uiS.lcdmsg.display(QString("%3").arg("0"))
        
        for i in range(9):
            for j in range(9):
                num = (i*9)+j
                self.listaCeldas[num].setText("")
        
    def CargarJuego(self):
        self.habilitarBotones()
        self.cargarS = MyformCargarSudoku()
        bandera = 0
        nombre = "guardar.txt"
       
        mFilename = QtCore.QString(nombre)
        
        mFile = QtCore.QFile(mFilename)
        if(mFile.exists()):
            mFile.open(QtCore.QIODevice.Text | QtCore.QIODevice.ReadOnly)
            if not(mFile.isOpen()):
                return
            txtstr = QtCore.QTextStream(mFile)
            
            while not(txtstr.atEnd()):
                datosSudoku = txtstr.readLine()
                mFile.flush()
                mFile.close()
                
                valores = datosSudoku.split("/")
                nivelC = valores[1]#Obtengo el Nivel
                
                if (self.uiS.textNivel.text() == nivelC):
                    bandera += 1
            if(bandera != 0):
                self.hide()
                nivel = self.uiS.textNivel.text()
                self.cargarS.ventanaCargar(self)
                self.cargarS.obtenerPartidasGuardadas(nivel)
                self.cargarS.show()
            else:
                QtGui.QMessageBox.information(self, "MENSAJE", "No existen Partidas Guardadas \nde nivel "+self.uiS.textNivel.text(), "ACEPTAR")
        else:
            QtGui.QMessageBox.information(self, "MENSAJE", "No existen Partidas Guardadas", "ACEPTAR")

    #GuardarPartida
    def guardarJueg(self):
        self.timer.stop()
        nomJugador = self.uiS.textJugador.text()
        nivel = self.uiS.textNivel.text()
        sMin = QtCore.QString.number(self.uiS.lcdmin.intValue())
        sSeg = QtCore.QString.number(self.uiS.lcdseg.intValue())
        sMiliseg = QtCore.QString.number(self.uiS.lcdmsg.intValue())
        info = ""
        banderaGuardar = 0
        
        #Actualizar la matriz
        for i in range(9):
            for j in range(9):
                num = (i*9)+j
                
                matrizGuardar.append(self.listaCeldas[num].toPlainText())
                if (matrizGuardar[num] != ""): banderaGuardar = 1
        
        if (banderaGuardar == 0):
            QtGui.QMessageBox.information(self, "Guardar-Sudoku", "No existen datos a GUARDAR", "ACEPTAR")
        else:
            self.encriptarS()
            for i in range(9):
                for j in range(9):
                    num = (i*9)+j
                    info = info+matrizGuardar[num]+","
            
            mFilename = QtCore.QString("guardar.txt")
            mFile = QtCore.QFile(mFilename)
            mFile.open(QtCore.QIODevice.Text | QtCore.QIODevice.Append)
            if not(mFile.isOpen()):    
                return
            
            txtstr = QtCore.QTextStream(mFile)
            txtstr << nomJugador+"/"+nivel+"/"+sMin+":"+sSeg+":"+sMiliseg+"/"+info+"\n"
            mFile.flush()
            mFile.close()
            
            QtGui.QMessageBox.information(self, "Guardar-Sudoku", "La partida ha sido guardada \nJUGADOR: "+nomJugador.toUpper(),"ACEPTAR")
            self.close()
        
    #Verificar (Hacer trampa)
    def verificarJuego(self):
        cont = 0
        niveles  = self.uiS.textNivel.text()
        
        if(niveles == "Juvenil"):  valores = plantilla1.split(",")
        if(niveles == "Profesional"):  valores = plantilla2.split(",")
        if(niveles == "Experto"):  valores = plantilla3.split(",")
        
        for i in range(9):
            for j in range(9):
                num = (i*9)+j
                celda = self.listaCeldas[num]
                if((celda.isEnabled()) and (self.getDisplayValue(i,j) != 0) and (self.getDisplayValue(i,j) != (self.toInt(valores[cont])))):
                    paleta = celda.palette()
                    paleta.setColor(QtGui.QPalette.Base, QtGui.QColor(255,150,150))
                    celda.setPalette(paleta)
                    
                if((celda.isEnabled()) and (self.getDisplayValue(i,j) != 0) and (self.getDisplayValue(i,j) == (self.toInt(valores[cont])))):
                    paleta = celda.palette()
                    paleta.setColor(QtGui.QPalette.Base, QtGui.QColor(120,255,120))
                    celda.setPalette(paleta)
                cont += 1
    
    #Encriptar Partida de Sudoku
    def encriptarS(self):
        cont = 33
        num1 = 0
        numT = 0
        
        for i in range(9):
            for j in range(9):
                num = (i*9)+j
                
                var = self.toInt(matrizGuardar[num])
                num1 = (var * var)
                
                if ((self.toInt( matrizGuardar[num] )%2) == 0 ):
                    numT = (num1/2) + cont 
                else:
                    numT = num1 + cont
                matrizGuardar[num] = (str(chr(numT)))

    #Correccion Cuadrante
    def CorreccionCuadrante(self,i,j):
        num = (i*9)+j
        despy_0 = (i/3) * 3
        despx_0 = (j/3) * 3
        
        for despy in range(despy_0, despy_0 + 3):
            for despx in range(despx_0, despx_0 + 3):
                num1 = (despy * 9) + despx
                if ((despy != i) and (despx != j)):
                    if(self.getDisplayValue(i,j) == self.getDisplayValue(despy, despx)):
                        paleta = self.listaCeldas[num].palette()
                        paleta.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 150, 150))
                        self.listaCeldas[num].setPalette(paleta)
                        self.listaCeldas[num1].setPalette(paleta)
                        QtGui.QMessageBox.information(self, "Advertencia", "Este numero ya fue ingresado en el cuadrante")
                       
                        return
                    else:
                        self.pintarTablero()
                        
    #Correccion Columna                
    def CorreccionColumna(self, i, j):
        num = (i*9)+j
		
        for k in range(9):
            
            if(k != i):
                if(self.getDisplayValue(i,j) == self.getDisplayValue(k,j)):
                    paleta = self.listaCeldas[num].palette()
                    paleta.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 150, 150))
                    self.listaCeldas[num].setPalette(paleta)
				
                    self.listaCeldas[(k*9)+j].setPalette(paleta)
                    QtGui.QMessageBox.information(self, "Advertencia", "Este numero ya fue ingresado en la columna")
               
                    return
                else:
                    self.pintarTablero()
                
    #Correccion Fila
    def CorreccionFila(self, i, j):
        num = (i*9)+j
        for k in range(9):
            num1 = (i*9)+k
            if(k != j):
                if(self.getDisplayValue(i,j) == self.getDisplayValue(i,k)):
                    paleta = self.listaCeldas[num].palette()
                    paleta.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 150, 150))
                    self.listaCeldas[num].setPalette(paleta)
                    self.listaCeldas[num1].setPalette(paleta)
                    QtGui.QMessageBox.information(self, "Advertencia", "Este numero ya fue ingresado en la fila")
                   
                    return
                else:
                    self.pintarTablero()
             

    def correccionInGame(self):

			
			for i in range(9):
				for j in range(9):
					num = (i*9) + j
					if(((self.getDisplayValue(i, j) != 0 or self.listaCeldas[num].toPlainText() != "") and self.listaCeldas[num].isEnabled())):
						if ((self.getDisplayValue(i, j) > 9  or self.getDisplayValue(i, j) < 1)):
							QtGui.QMessageBox.information(self, "Advertencia", "Este numero no esta dentro del rango permitido")
							self.listaCeldas[num].setText("")		
							
					if(((self.getDisplayValue(i, j) != 0) and self.listaCeldas[num].isEnabled())):
						self.CorreccionFila(i, j)
						self.CorreccionColumna(i, j)
						self.CorreccionCuadrante(i, j)
						
                    
            
        