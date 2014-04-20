# -*- coding: utf-8 -*-

import os
import json


from PyQt4 import  QtCore, QtGui, QtNetwork
from PyQt4.QtCore import Qt



IMG_DIR = os.path.abspath( '../images/')

class ICO:
	fg = "flightgear_icon.png"
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
		self.setWindowIcon( make_icon(ICO.fg))
		
		##========================================
		## Objects
		
		## network access - Note error is in reply !
		self.netMan = QtNetwork.QNetworkAccessManager(self)
		self.connect(self.netMan , QtCore.SIGNAL("finished(QNetworkReply*)"), self.on_http_finished)
		
		## Properties Modes
		self.modelProps = QtGui.QStandardItemModel(self)
		self.modelProps.setColumnCount(5)
		self.modelProps.setHorizontalHeaderLabels( ["Node", "Value", "Type", "Child Count", "Path"] )
		
		## Filter Model
		self.modelPropsFilter = QtGui.QSortFilterProxyModel(self)
		self.modelPropsFilter.setSourceModel(self.modelProps) 
		
		
		## ========================================================
		## Top Toolbar
		self.topToolBar = QtGui.QToolBar()
		self.addToolBar(Qt.TopToolBarArea, self.topToolBar)
		
		## Server Address
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
		self.treeProps = QtGui.QTreeView()
		self.setCentralWidget(self.treeProps)
		
		self.treeProps.setModel(self.modelPropsFilter)
		self.treeProps.setSortingEnabled(True)
		self.treeProps.setRootIsDecorated(True)
		
		"""
		hi = self.treeProps.headerItem()
		hi.setText(CP.node, "Path")
		hi.setText(CP.val, "Value")
		hi.setText(CP.type, "Type")
		hi.setText(CP.child_count, "Child Count")
		hi.setText(CP.path, "path")
		"""
		self.treeProps.setColumnWidth(CP.node, 200)
		self.treeProps.setColumnWidth(CP.val, 100)
		self.treeProps.setColumnWidth(CP.type, 100)
		
		## hack for oppetes dualcreen
		if os.path.exists("LOCAL"):
			self.setGeometry( 10, 10, 1200, 800 )
			self.move( 1600, 20 )
				
	def get_url(self):
		
		u = QtCore.QUrl()
		u.setScheme("http")
		u.setHost(self.txtHost.text())
		port = int(self.txtPort.text()) 
		u.setPort(port)
		u.setPath("/json/")
		u.addQueryItem("d", "2")
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
		json_str = str(bytes)
		data = json.loads(json_str)
		
		## Load the kids of first node
		#self.treeProps.setUpdatesEnabled(False)
		
		self.load_prop_nodes(data['children'], self.modelProps.invisibleRootItem())
		#self.treeProps.expandAll()
		
		#self.treeProps.setUpdatesEnabled(True)
		
		
	def load_prop_nodes(self, nodes, parentNode):
		
		
		for n in nodes:
			idx = self.modelProps.index(0,0)
			#print CP.path, n['path'], idx
			#items = self.modelProps.findItems(  str(n['path']), Qt.MatchRecursive, CP.path)
			
			idxs = self.modelProps.match(idx, Qt.UserRole, n['path'], -1, Qt.MatchExactly|Qt.MatchRecursive) 
			#print items
			## get child nodes, we use this to determin icon also
			
			nChild = n['nChildren'] 
			v = n.get("value")
			kids = n.get("children")
				
			if len(idxs) == 0:
				# create a new node, and set everything here once, only value is updated later
				iName = QtGui.QStandardItem()
				iName.setText(n['name'])
				iName.setIcon( make_icon( ICO.folder if n['type'] == "-" else ICO.prop) )
				iName.setData(n['path'], Qt.UserRole)
				
				iValue = QtGui.QStandardItem()
				iValue.setTextAlignment(Qt.AlignRight)
				if v:
					iValue.setText(str(v))
								
				iType = QtGui.QStandardItem()
				iType.setText(n['type'])

								
				iCount = QtGui.QStandardItem()
				iCount.setText(str(n['nChildren']) if nChild  > 0 else "-")
				iCount.setTextAlignment(Qt.AlignCenter)
				
				iPath = QtGui.QStandardItem()
				iPath.setText(n['path'])
				
				parentNode.appendRow([iName, iValue, iType, iCount, iPath])
				
				"""
				item.setText(CP.node, n['name'])
				item.setText(CP.path, n['path'])
				item.setText(CP.type, n['type'])
				"""
				if nChild > 0:
						
					if kids:
						self.load_prop_nodes(kids, iName)
					else:
						## add a fake item so + sign shows 
						itemFake = QtGui.QStandardItem()
						itemFake.setText("##")
						iName.appendRow([itemFake, QtGui.QStandardItem(), QtGui.QStandardItem(), QtGui.QStandardItem(), QtGui.QStandardItem()])
			else:
				# otherwise it exits so first one
				idx = idxs[0]
				#print "YES", idx
				#print self.modelProps.itemFromIndex(self.modelProps.index(idx.row(), CP.val) )
				if v:
					self.modelProps.itemFromIndex(self.modelProps.index(idx.row(), CP.val, idx.parent()) ).setText( str(v) )
				if kids:
					self.load_prop_nodes(kids, self.modelProps.itemFromIndex(idx))
				
			"""
			
			if nChild > 0:
				item.setText(CP.child_count, str(nChild))
			else:
				item.setText(CP.child_count, "-")
			"""
			
			# set the values
			"""
			v = n.get("value")
			if v:
				item.setText(CP.val, str(v))
			"""
	

			



		
		
	