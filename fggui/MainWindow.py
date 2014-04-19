# -*- coding: utf-8 -*-

import os
import json

from PyQt4 import QtCore, QtGui, QtNetwork
from PyQt4.QtCore import Qt


IMG_DIR = os.path.abspath( '../images/')

class ICO:
	refresh = "arrow-circle-double.png"
	prop = "blue-document-attribute-p.png"
	folder = "folder.png"


def make_icon(file_name):
	return QtGui.QIcon( IMG_DIR + "/" + file_name )


class CP:
	"""Enum(ish) for the column numbers"""
	node = 0
	val = 1
	type = 2
	child_count = 3
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
		self.buttRefresh.setIcon( make_icon(ICO.refresh) )
		self.buttRefresh.setText("Load Server")
		self.buttRefresh.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
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
		hi.setText(CP.child_count, "Child Count")
		hi.setText(CP.path, "path")
		
		self.treeProps.setColumnWidth(CP.node, 200)
		self.treeProps.setColumnWidth(CP.val, 100)
		self.treeProps.setColumnWidth(CP.type, 100)
		
		
		self.setGeometry( 10, 10, 1200, 800 )
		self.move( 1600, 20 )
				
	def get_url(self):
		
		u = QtCore.QUrl()
		u.setScheme("http")
		u.setHost(self.txtHost.text())
		port, ok =self.txtPort.text().toInt() 
		u.setPort(port)
		u.setPath("/json/")
		u.addQueryItem("d", "3")
		return u
	
	def send_request(self):
		
		request = QtNetwork.QNetworkRequest()
		request.setUrl( self.get_url() )
		
		print "request", request.url().toString()
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
		
		## decode json string to data
		bytes = reply.readAll()
		json_str = str(QtCore.QString.fromUtf8(bytes.data(), bytes.size()))
		data = json.loads(json_str)
		
		## Load the kids of first node
		self.treeProps.setUpdatesEnabled(False)
		self.load_prop_nodes(data['children'], self.treeProps.invisibleRootItem())
		self.treeProps.setUpdatesEnabled(True)
		
	def load_prop_nodes(self, nodes, parentNode):
		
		
		for n in nodes:
			items = self.treeProps.findItems(n['path'], Qt.MatchExactly|Qt.MatchRecursive, CP.path)
			
			## get child nodes, we use this to determin icon also
			
				
			if len(items) == 0:
				# create a new node, and set everything here once, only value is updated later
				item = QtGui.QTreeWidgetItem(parentNode)
				item.setText(CP.node, n['name'])
				item.setText(CP.path, n['path'])
				item.setText(CP.type, n['type'])
				
				item.setIcon(CP.node, make_icon( ICO.folder if n['type'] == "-" else ICO.prop) )
			else:
				# otherwise it exits so first one
				item = items[0]
			
			nChild = n['nChildren'] 
			if nChild > 0:
				item.setText(CP.child_count, str(nChild))
			else:
				item.setText(CP.child_count, "-")
			# set the values
			v = n.get("value")
			if v:
				item.setText(CP.val, str(v))
			
			if nChild > 0:
				kids = n.get("children")	
				if kids:
					self.load_prop_nodes(kids, item)
				else:
					## add a fake item so + sign shows 
					itemFake = QtGui.QTreeWidgetItem(item)
					itemFake.setText(CP.type, "##")




		
		
	