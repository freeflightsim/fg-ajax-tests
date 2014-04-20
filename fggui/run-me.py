#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Peter Morgan <pete@freeflightsim.org>

"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "../"))


from PyQt4 import QtGui, QtCore



import MainWindow



if __name__ == '__main__':


    app = QtGui.QApplication( sys.argv )
    app.processEvents()
    
    QtGui.QApplication.setStyle( QtGui.QStyleFactory.create( 'Cleanlooks' ) )


    window = MainWindow.MainWindow()
    window.show()

    sys.exit( app.exec_() )
