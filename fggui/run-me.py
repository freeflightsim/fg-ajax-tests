#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Peter Morgan <pete@freeflightsim.org>

"""

import sys
import os
from PyQt4 import QtGui, QtCore

import MainWindow



if __name__ == '__main__':


    app = QtGui.QApplication( sys.argv )


    app.processEvents()


    window = MainWindow.MainWindow()
    window.show()

    sys.exit( app.exec_() )
