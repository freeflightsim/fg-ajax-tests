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

FAKE_NODE = "#FAKE#"

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
		
		self.buttGrooupLoadNode = QtGui.QButtonGroup(self)
		self.buttGrooupLoadNode.setExclusive(False)
		self.connect(self.buttGrooupLoadNode, QtCore.SIGNAL("buttonClicked(QAbstractButton *)"), self.on_reload_node_clicked)
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
		self.connect( self.buttRefresh, QtCore.SIGNAL("clicked()"), self.on_load_server)


		## ========================================================
		## Request Info Dock

		dock = QtGui.QDockWidget("Net Info")
		self.addDockWidget(Qt.LeftDockWidgetArea, dock)
		
		dnetWidget = QtGui.QWidget()
		dock.setWidget(dnetWidget)
		dnetLayout = QtGui.QVBoxLayout()
		dnetLayout.setContentsMargins(0,0,0,0)
		dnetLayout.setSpacing(0)
		dnetWidget.setLayout(dnetLayout)
		
		
		self.treeHttp = QtGui.QTreeWidget()
		dnetLayout.addWidget(self.treeHttp, 1)
		self.treeHttp.setRootIsDecorated(False)
		self.treeHttp.headerItem().setText(0, "Name")
		self.treeHttp.headerItem().setText(1, "Value")
		
		self.txtRawJson = QtGui.QTextEdit()
		dnetLayout.addWidget(self.txtRawJson, 2)
		
	
		## ========================================================
		## Request Info Dock

		dock = QtGui.QDockWidget("Watching Nodes")
		self.addDockWidget(Qt.RightDockWidgetArea, dock)
		
		dwWidget = QtGui.QWidget()
		dock.setWidget(dwWidget)
		dwLayout = QtGui.QVBoxLayout()
		dwLayout.setContentsMargins(0,0,0,0)
		dwLayout.setSpacing(0)
		dwWidget.setLayout(dwLayout)
		
		
		self.treeWatch = QtGui.QTreeWidget()
		dwLayout.addWidget(self.treeWatch, 1)
		self.treeWatch.setRootIsDecorated(False)
		self.treeWatch.headerItem().setText(0, "Node")
		self.treeWatch.headerItem().setText(1, "Value")		
		
		self.treeWatch.setMinimumWidth(400)


		## ========================================================
		## Central Widget
		cWidget = QtGui.QWidget()
		self.setCentralWidget(cWidget)
		cLayout = QtGui.QVBoxLayout()
		cLayout.setContentsMargins(0,0,0,0)
		cLayout.setSpacing(0)
		cWidget.setLayout(cLayout)
		
		cToolBar = QtGui.QToolBar()
		cLayout.addWidget(cToolBar)
		
		self.txtPropsFilter = QtGui.QLineEdit()
		cToolBar.addWidget(self.txtPropsFilter)
		self.connect(self.txtPropsFilter, QtCore.SIGNAL("textChanged(const QString &)"), self.on_props_filter)
		## ==========================
		## Properties Tree
		self.treeProps = QtGui.QTreeView()
		cLayout.addWidget(self.treeProps)
		
		self.treeProps.setModel(self.modelPropsFilter)
		self.treeProps.setSortingEnabled(True)
		self.treeProps.setRootIsDecorated(True)
		
		self.treeProps.setColumnWidth(CP.node, 200)
		self.treeProps.setColumnWidth(CP.val, 100)
		self.treeProps.setColumnWidth(CP.type, 100)
		
		self.treeProps.setColumnHidden(CP.path, True)
		
		self.connect(self.treeProps, QtCore.SIGNAL("expanded(const QModelIndex &)"), self.on_tree_props_expanded)
		self.connect(self.modelProps, QtCore.SIGNAL("itemChanged(QStandardItem *)"), self.on_prop_item_changed)
		
		## hack for oppetes dualcreen
		if os.path.exists("LOCAL"):
			self.setGeometry( 10, 10, 1200, 800 )
			self.move( 1600, 20 )
		

		
	def on_tree_props_expanded(self, proxy_idx):
		
		item = self.modelProps.itemFromIndex(self.modelPropsFilter.mapToSource(proxy_idx))
		
		if item.child(0,0).text() == FAKE_NODE:
			self.modelProps.removeRow(0, item.index())
			#item.child(0,0).setText("Loading")
			self.send_request(item.data(Qt.UserRole).toString())
	
	def on_prop_item_changed(self, item):
		print item
		if item.index().column() == CP.val:
			## check its checked
			if item.checkState() == Qt.Checked:
				path = self.modelProps.itemFromIndex( self.modelProps.index( item.index().row(), CP.path, item.parent().index()) ).text()
				items = self.treeWatch.findItems(path, Qt.MatchExactly, 0)
				if len(items) == 0:
					item = QtGui.QTreeWidgetItem()
					item.setText(0, path)
					self.treeWatch.addTopLevelItem(item)
	
	def on_props_filter(self, txt):
		self.modelPropsFilter.setFilterFixedString(txt)	
		self.modelPropsFilter.setFilterKeyColumn(CP.path)
	
	def on_reload_node_clicked(self, butt):
		path = butt.property("path").toString()
		self.send_request(path)
				
	def get_url(self, path):
		
		u = QtCore.QUrl()
		u.setScheme("http")
		u.setHost(self.txtHost.text())
		port = int(self.txtPort.text()) 
		u.setPort(port)
		u.setPath("/json" + path)
		u.addQueryItem("d", "1")
		return u

	def on_load_server(self):
		self.send_request("/")
		
	def send_request(self, path):
		
		self.txtRawJson.clear()
		self.treeHttp.clear()
		
		request = QtNetwork.QNetworkRequest()
		request.setUrl( self.get_url(path) )
		
		print "request", request.url().toString()
		self.reply = self.netMan.get( request )
		
		self.connect( self.reply, QtCore.SIGNAL( 'error(QNetworkReply::NetworkError)' ), self.on_http_error )
		"""
		self.connect( self.reply, QtCore.SIGNAL( 'readyRead()' ), self.on_http_read )
		self.connect( self.reply, QtCore.SIGNAL( 'finished()' ), self.on_http_finished )
		"""
		
	def on_http_error(self, err):
		self.treeHttp.clear()
		item = QtGui.QTreeWidgetItem()
		item.setText(0, "Error" )
		item.setText(1, "??" )
		self.treeHttp.addTopLevelItem(item)
		
		
	def on_http_finished(self, reply):
		
		if reply.error():
			## its an error so handled by on_http_error
			return
		
		self.treeHttp.setUpdatesEnabled(False)
		self.treeHttp.clear()
		for h in reply.rawHeaderPairs():
			item = QtGui.QTreeWidgetItem()
			item.setText(0, str(h[0]) )
			item.setText(1, str(h[1]) )
			self.treeHttp.addTopLevelItem(item)
		self.treeHttp.setUpdatesEnabled(True)

		
		## decode json string to data
		bytes = reply.readAll()
		json_str = str(bytes)		
		data = json.loads(json_str)
		
		self.txtRawJson.setText(json_str)
		
		## Load the kids of first node
		## dfind which node this is, and find its parent
		if data['path'] == "": ## should be "/"
			## its the root node
			parentItem = self.modelProps.invisibleRootItem()
			
		else:
			## find the parent
			idxs = self.modelProps.match(self.modelProps.index(0,0), Qt.UserRole, data['path'], -1, Qt.MatchExactly|Qt.MatchRecursive) 
			parentItem = self.modelProps.itemFromIndex( idxs[0] )
		#self.treeProps.setUpdatesEnabled(False)
		
		self.load_prop_nodes(data['children'], parentItem)
		#self.treeProps.expandAll()
		
		#self.treeProps.setUpdatesEnabled(True)
		
		
	def load_prop_nodes(self, nodes, parentItem):
		
		
		for n in nodes:
			idx = self.modelProps.index(0,0)
			#print CP.path, n['path'], idx
			#items = self.modelProps.findItems(  str(n['path']), Qt.MatchRecursive, CP.path)
			
			idxs = self.modelProps.match(idx, Qt.UserRole, n['path'], -1, Qt.MatchExactly|Qt.MatchRecursive) 
			#print n['path'], idxs
			## get child nodes, we use this to determin icon also
			
			nChild = n['nChildren'] 
			v = n.get("value")
			kids = n.get("children")
				
			if len(idxs) == 0:
				# create a new node, and set everything here once, only value is updated later
				iName = QtGui.QStandardItem()
				iName.setText(n['name'])
				
				iName.setIcon( make_icon( ICO.folder if nChild > 0 else ICO.prop) )
				iName.setData(n['path'], Qt.UserRole)
				
				iValue = QtGui.QStandardItem()
				iValue.setTextAlignment(Qt.AlignRight)
				if nChild == 0:
					iValue.setCheckable(True)
		
				if v:
					iValue.setText(str(v))
								
				iType = QtGui.QStandardItem()
				iType.setText(n['type'])

								
				iCount = QtGui.QStandardItem()
				iCount.setText(str(n['nChildren']) if nChild  > 0 else "-")
				iCount.setTextAlignment(Qt.AlignCenter)
				
				iPath = QtGui.QStandardItem()
				iPath.setText(n['path'])
				
				parentItem.appendRow([iName, iValue, iType, iCount, iPath])
				
				if nChild > 0:
					idx = self.modelProps.indexFromItem(iValue)
					butt = QtGui.QToolButton()
					butt.setText("Reload")
					butt.setProperty("path",n['path'])
					butt.setAutoRaise(True)
					self.treeProps.setIndexWidget(self.modelPropsFilter.mapFromSource(idx), butt)
					self.buttGrooupLoadNode.addButton(butt)
					
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
						itemFake.setText(FAKE_NODE)
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
	

			



		
		
	