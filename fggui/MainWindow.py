# -*- coding: utf-8 -*-

## Here we load Qt commonly across modules
## later need to put "trap" here
## and detect  pyside etc

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

class MainWindow( QtGui.QMainWindow ):
    

    def __init__( self, parent=None, tb_wizz=False, tb_search=False ):
        QtGui.QMainWindow.__init__( self )

        QtGui.QApplication.setStyle( QtGui.QStyleFactory.create( 'Cleanlooks' ) )


        self.setWindowTitle("FG Ajax Tests")
        
        