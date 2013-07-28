'''
Created on 15/07/2013

@author: josanvel
'''
import sys
import Image
from PyQt4 import QtGui
from pyVentanaP import Myform

def main():
    app = QtGui.QApplication(sys.argv)
    myapp = Myform()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
