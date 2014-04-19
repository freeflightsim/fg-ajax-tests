# -*- coding: utf-8 -*-

import json

from PyQt4 import QtCore, QtGui, QtNetwork
from PyQt4.QtCore import Qt

class CP:
	node = 0
	val = 1
	type = 2
	kids = 3
	path = 4

class MainWindow( QtGui.QMainWindow ):
	

	def __init__( self, parent=None):
		QtGui.QMainWindow.__init__( self )

		
		self.setWindowTitle("FG Ajax Tests")
		
		
		self.netMan = QtNetwork.QNetworkAccessManager(self)
		self.connect(self.netMan , QtCore.SIGNAL("finished(QNetworkReply*)"), self.on_http_finished)
		
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
		self.txtPort.setText("8888")
		self.topToolBar.addWidget(self.txtPort)
		
		self.buttRefresh = QtGui.QToolButton()
		self.topToolBar.addWidget(self.buttRefresh)
		self.buttRefresh.setText("Load Server")
		self.connect( self.buttRefresh, QtCore.SIGNAL("clicked()"), self.send_request)


		## ========================================================
		## Tree
		self.treeProps = QtGui.QTreeWidget()
		self.setCentralWidget(self.treeProps)
		
		self.treeProps.setRootIsDecorated(True)
		hi = self.treeProps.headerItem()
		hi.setText(CP.node, "Path")
		hi.setText(CP.val, "Value")
		hi.setText(CP.type, "Type")
		hi.setText(CP.kids, "Child Count")
		
		
	def get_url(self):
		
		u = QtCore.QUrl()
		u.setScheme("http")
		u.setHost(self.txtHost.text())
		port, ok =self.txtPort.text().toInt() 
		u.setPort(port)
		u.setPath("/json/")
		return u
	
	def send_request(self):
		
		request = QtNetwork.QNetworkRequest()
		request.setUrl( self.get_url() )
		
		self.reply = self.netMan.get( request )
		
		self.connect( self.reply, QtCore.SIGNAL( 'error(QNetworkReply::NetworkError)' ), self.on_http_error )
		"""
		self.connect( self.reply, QtCore.SIGNAL( 'readyRead()' ), self.on_http_read )
		self.connect( self.reply, QtCore.SIGNAL( 'finished()' ), self.on_http_finished )
		"""
		
	def on_http_error(self, err):
		print "error", err
	
	def on_http_read(self):
		print "read"
		
	def on_http_finished(self, reply):
		
		bytes = reply.readAll()
		json_str = str(QtCore.QString.fromUtf8(bytes.data(), bytes.size()))
		data = json.loads(json_str)
		
		self.load_data(data)
		
	def load_data(self, data):
		
		self.treeProps.setUpdatesEnabled(False)
		for n in data:
			print n
			items = self.treeProps.findItems(n['path'], Qt.MatchExactly, CP.path)
			if len(items) == 0:
				# create a new node, and set everything here once, only value is updated later
				item = QtGui.QTreeWidgetItem()
				item.setText(CP.node, n['name'])
				item.setText(CP.path, n['path'])
				item.setText(CP.type, n['type'])
			else:
				# otherwise it exits fo first one
				item = items[0]
			#item.setText(CP.val, n[''])
		self.treeProps.setUpdatesEnabled(True)
		#print "done", reply
		
		
		
	