# -*- coding: utf-8 -*-


from PyQt4 import QtCore, QtGui, QtNetwork
from PyQt4.QtCore import Qt

class MainWindow( QtGui.QMainWindow ):
	

	def __init__( self, parent=None):
		QtGui.QMainWindow.__init__( self )

		
		self.setWindowTitle("FG Ajax Tests")
		
		
		self.netMan = QtNetwork.QNetworkAccessManager(self)
		
		
		## ========================================================
		## Top Toolbar
		self.topToolBar = QtGui.QToolBar()
		self.addToolBar(Qt.TopToolBarArea, self.topToolBar)
		
		## Server Addredd
		self.topToolBar.addWidget(QtGui.QLabel("fgms host:"))
		self.txtHost = QtGui.QLineEdit()
		self.topToolBar.addWidget(self.txtHost)
		self.txtHost.setText("127.0.0.1")
		
		## Server Port
		self.topToolBar.addWidget(QtGui.QLabel("fgms port:"))
		self.txtPort = QtGui.QLineEdit()
		self.txtPort.setText("9999")
		self.topToolBar.addWidget(self.txtPort)
		
		self.buttRefresh = QtGui.QToolButton()
		self.topToolBar.addWidget(self.buttRefresh)
		self.buttRefresh.setText("Load Server")
		self.connect( self.buttRefresh, QtCore.SIGNAL("clicked()"), self.send_request)
		
	def get_url(self):
		
		return self.txtHost.text().append(":").append( self.txtPort.text() ).append("/json/")

	
	def send_request(self):
		
		print self.get_url()
		request = QtNetwork.QNetworkRequest()
		request.setUrl( QtCore.QUrl( self.get_url()) )
		
		self.reply = self.netMan.get( self.request )
		self.connect( self.reply, QtCore.SIGNAL( 'error(QNetworkReply::NetworkError)' ), self.on_http_error )
		self.connect( self.reply, QtCore.SIGNAL( 'readyRead()' ), self.on_http_read )
		self.connect( self.reply, QtCore.SIGNAL( 'finished()' ), self.on_http_finished )
		
		
	def on_http_error(self):
		pass
	
	def on_http_read(self):
		print "read"
		
	def on_http_finished(self):
		print "done"
		
		
	