'''
Created on 15/07/2013

@author: josanvel
'''
import sys
from PyQt4 import QtGui
from VentanaPrincipal import Ui_Principal

def main():
    aplicacion = QtGui.QApplication(sys.argv)
    #aplicacion.setStyle("fusion")
    Principal = QtGui.QMainWindow()
    ui = Ui_Principal()
    ui.setupUi(Principal)
    Principal.show()
    sys.exit(aplicacion.exec_())

if __name__ == '__main__':
    main()
