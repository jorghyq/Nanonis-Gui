# simple gui test for display nanonis file

import os
import platform
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from guiqwt.plot import ImageWidget
from guiqwt.plot import CurveWidget
from guiqwt.plot import ImagePlot
from guiqwt.plot import CurvePlot
from guiqwt.image import ImageItem
from guiqwt.styles import ImageParam
from guiqwt.shapes import RectangleShape
from guiqwt.styles import ShapeParam
from guiqwt.shapes import EllipseShape
from guiqwt.annotations import AnnotatedRectangle
from guiqwt.annotations import AnnotatedPoint
from guiqwt.styles import AnnotationParam
from guiqwt.builder import make
#import random as rd
import numpy as np
#import matplotlib.pyplot as plt
import nanonisfile as nf
import nanonisdatfile as nd
import cv2


class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		################# DATA ####################################
		self.currentdir = None
		self.currentfile = None
		self.currentsxm = None
		self.nanofile = None
		self.scale_factor = None
		self.sxmlist = []
		self.alllist = {}
		self.datfiles = []
		
		################### GUI ###################################
		self.mdi = QWorkspace()
		self.fileMenu = self.menuBar().addMenu("Flie")
		fileToolbar = self.addToolBar("File Browser")
		self.showFileButton = QPushButton("Show File Browser")
		fileToolbar.addWidget(self.showFileButton)
		#self.addActions(fileToolbar,(self.showFilebrowser))
		self.setCentralWidget(self.mdi)
		self.fileWindow = FileWindow()
		self.fileWindow.setMinimumSize(300,500)
		self.mdi.addWindow(self.fileWindow)
		self.imageWindow = ImageWindow()
		self.mdi.addWindow(self.imageWindow)
		self.imageWindow.show()
		
		################# SIGNAL ####################################
		self.connect(self.showFileButton,SIGNAL("clicked()"), self.showFilebrowser)
		self.connect(self.fileWindow.selectButton,SIGNAL("clicked()"), self.selectfolder)
		
		################################ SLOTS ##############################
		
	def showFilebrowser(self):
		self.fileWindow.setVisible(True)
	
	def selectfolder(self):
		filepath = self.fileWindow.treeWidget.selectedIndexes()[0]
		if filepath.model().isDir(filepath):
			self.currentdir = str(filepath.model().filePath(filepath))
		else:
			dname,fname = os.path.split(str(filepath.model().filePath(filepath)))
			self.currentdir = dname
			self.currentfile = fname
		files = {}
		self.sxmlist = []
		for line in os.listdir(self.currentdir):
			filepath = os.path.join(self.currentdir,line)
			if os.path.isfile(filepath):
				line = os.path.basename(line)
				name,ext = os.path.splitext(line)
				if ext[1:] == "sxm":
					self.sxmlist.append(line)
					files[line] = os.path.getmtime(filepath)
				elif ext[1:] == "dat":
					files[line] = os.path.getmtime(filepath)
		#print self.sxmlist
		if len(files) > 0:
			nfiles = sorted(files.items(), key=lambda files:files[1])
			sxmindex = []
			for i in range(len(nfiles)):
				if nfiles[i][0].split(".")[-1] == "sxm":
					sxmindex.append(i)
			self.currentsxm = nfiles[sxmindex[0]][0]
			sortedfiles = {}
			for i in range(len(sxmindex)-1):
				temp_ind = sxmindex[i]
				sortedfiles[nfiles[temp_ind][0]] = []
				for j in range(sxmindex[i]+1,sxmindex[i+1]):
					sortedfiles[nfiles[temp_ind][0]].append(nfiles[j][0])
			self.alllist = sortedfiles
			self.imageWindow.alllist = self.alllist
			self.imageWindow.sxmlist = self.sxmlist
			self.imageWindow.currentdir = self.currentdir
			self.imageWindow.openfile(os.path.join(self.currentdir,self.currentsxm))
			self.imageWindow.selectComboBox.clear()
			self.imageWindow.selectComboBox.addItems(self.sxmlist)
			
			#print self.alllist
		
		
		

class FileWindow(QWidget):
	def __init__(self, parent=None):
		super(FileWindow, self).__init__(parent)
		#self.openButton = QPushButton("&OpenFile")
		self.selectButton = QPushButton("&SelectFolder")
		self.treeWidget = QTreeView()
		model = QFileSystemModel(self)
		model.setRootPath(QDir.currentPath())
		self.treeWidget.setModel(model)
		self.treeWidget.setHeaderHidden(True)
		self.treeWidget.setColumnHidden(1,True)
		self.treeWidget.setColumnHidden(2,True)
		self.treeWidget.setColumnHidden(3,True)
		
		self.hlayout = QHBoxLayout()
		#self.hlayout.addWidget(self.openButton)
		self.hlayout.addWidget(self.selectButton)
		self.vlayout = QVBoxLayout()
		self.vlayout.addLayout(self.hlayout)
		self.vlayout.addWidget(self.treeWidget)
		self.setLayout(self.vlayout)
		
		def closeEvent(self, event):
			self.setVisible(False)
		
			

class ImageWindow(QMainWindow):
	def __init__(self, parent=None):
		super(ImageWindow, self).__init__(parent)
		###################### DATA #################################
		self.currentdir = None
		self.alllist = {} 
		self.sxmlist = []
		self.sxmlist_time = {}
		self.sxmtodatlist = {}
		self.datlist = []
		self.datfiles = []
		self.datlist_time = {}
		self.datcoor = {}
		self.datrects = []
		self.matchrects = []
		self.dathighlights = []
		self.datannos = []
		self.speclist = []
		self.datchannels = []
		self.select_rect = None
		self.nanofile = None
		self.scale_factor = None
		self.currentsxm = None
		self.currentdata = None
		self.select_region = None
		
		##################### GUI #####################################
		self.imagePara = ImageParam()
		self.image = ImageItem()
		self.image.set_selectable(True)
		
		self.selectComboBox = QComboBox()
		self.proTable = QTableWidget()
		self.proTable.setFixedWidth(100)
		
		self.listWidget = QListWidget()
		self.listWidget.setFixedWidth(250)
		self.listWidget.setSelectionMode(3)
		self.xLabel = QLabel("Xc:")
		self.xshowLabel = QLabel("0")
		self.yLabel = QLabel("Yc:")
		self.yshowLabel = QLabel("0")
		self.processComboBox = QComboBox()
		self.processComboBox.addItems(["Raw","Substrac average","Substract slope","Subtract linear fit"])
		
		self.imagePlot = ImageWidget(aspect_ratio=1.0, lock_aspect_ratio=True,show_contrast=True,yreverse=False,colormap='gray')#,show_itemlist=True
		self.imagePlot.plot.set_aspect_ratio(1.00, True)
		self.imagePlot.plot.setFixedHeight(600)
		self.imagePlot.plot.setFixedWidth(600)
		self.imagePlot.register_all_image_tools()
		self.imagePlot.plot.add_item(self.image)
		
		self.curvePlot = CurveWidget()
		self.curvePlot.plot.setFixedHeight(400)
		self.curvePlot.plot.setFixedWidth(800)
		self.curvePlot.register_all_curve_tools()
		self.datchannelComboBox = QComboBox()
		self.datchannelComboBox.addItems(['Bias calc (V)', 'Current (A)', 'LIX 1 omega (A)', 'LIY 1 omega (A)'])
				
		self.forbackComboBox = QComboBox()
		self.forbackComboBox.addItems(['Forward','Backward'])
		self.channelComboBox = QComboBox()
		self.addButton = QPushButton("&Add")
		self.applyButton = QPushButton("Apply")
		self.openButton = QPushButton("&Open")
		self.closeButton = QPushButton("Close")
		
		paraLayout1 = QVBoxLayout()
		paraLayout1.addWidget(self.selectComboBox)
		paraLayout1.addWidget(self.proTable)
		
		showLayout = QHBoxLayout()
		showLayout.addWidget(self.xLabel)
		showLayout.addWidget(self.xshowLabel)
		showLayout.addWidget(self.yLabel)
		showLayout.addWidget(self.yshowLabel)
		showLayout.addStretch()
		showLayout.addWidget(self.processComboBox)
		paraLayout2 = QVBoxLayout()
		paraLayout2.addLayout(showLayout)
		paraLayout2.addWidget(self.imagePlot)
		
		paraLayout3 = QVBoxLayout()
		paraLayout3.addWidget(self.curvePlot)
		paraLayout3.addWidget(self.datchannelComboBox)
		
		paraLayout4 = QVBoxLayout()
		paraLayout4.addWidget(self.forbackComboBox)
		paraLayout4.addWidget(self.channelComboBox)
		paraLayout4.addWidget(self.addButton)
		paraLayout4.addWidget(self.applyButton)
		paraLayout4.addStretch()
		paraLayout4.addWidget(self.openButton)
		paraLayout4.addWidget(self.closeButton)
		
		
		layout = QHBoxLayout()
		layout.addLayout(paraLayout1)
		layout.addWidget(self.listWidget)
		layout.addStretch()
		layout.addLayout(paraLayout2)
		#layout.addLayout(paraLayout3)
		layout.addLayout(paraLayout4)
		centralWidget = QWidget()
		centralWidget.setLayout(layout);
		self.setCentralWidget(centralWidget);
		
		############################### SIGNALS ###########################
		self.connect(self.addButton,SIGNAL("clicked()"), self.selectRegion)
		self.connect(self.selectComboBox, SIGNAL("currentIndexChanged(int)"),self.changefile)
		self.connect(self.forbackComboBox, SIGNAL("currentIndexChanged(int)"),self.updateImage)
		self.connect(self.channelComboBox, SIGNAL("currentIndexChanged(int)"),self.updateImage)
		self.connect(self.listWidget, SIGNAL("itemSelectionChanged()"), self.updateSpec)
		self.connect(self.datchannelComboBox, SIGNAL("currentIndexChanged(int)"), self.updateSpec)
		self.connect(self.processComboBox, SIGNAL("currentIndexChanged(int)"), self.updateImage)
		self.connect(self.applyButton,SIGNAL("clicked()"), self.getSelectRegion)		

		############################## SLOTS #############################
	def openfile(self,filename):
		if filename:
			self.nanofile = nf.NanonisFile(filename)
			self.currentsxm = os.path.basename(self.nanofile.header['filename'])
		self.scale_factor = self.nanofile.header['scan_pixels'][0]/(self.nanofile.header['scan_range'][0]*1000000000)
		self.updateTable()
		self.updateImage()
		self.updateImageInfo()
		self.updateList()
		self.updateDatPosition()
		
	def changefile(self):
		fname = unicode(self.selectComboBox.currentText())
		fname = os.path.join(self.currentdir,fname)
		if fname:
			self.nanofile = nf.NanonisFile(fname)
			self.currentsxm = os.path.basename(self.nanofile.header['filename'])
		self.scale_factor = self.nanofile.header['scan_pixels'][0]/(self.nanofile.header['scan_range'][0]*1000000000)
		#print self.scale_factor
		self.updateTable()
		self.updateImage()
		self.updateImageInfo()
		self.updateList()
		self.updateDatPosition()
			
	def closefile(self):
		self.nanofile = None
		self.proTable.clear()
		
	def updateTable(self):
		# update the info of the currently opened sxm file
		self.proTable.clear()
		self.proTable.setRowCount(len(self.nanofile.header))
		self.proTable.setColumnCount(2)
		self.proTable.setHorizontalHeaderLabels(["Parameter","Value"])
		self.proTable.setAlternatingRowColors(True)
		self.proTable.setEditTriggers(QTableWidget.NoEditTriggers)
		self.proTable.setSelectionBehavior(QTableWidget.SelectRows)
		self.proTable.setSelectionMode(QTableWidget.SingleSelection)
		count = 0
		for key, value in self.nanofile.header.iteritems():
			item = QTableWidgetItem(key)
			self.proTable.setItem(count, 0, item)
			item = QTableWidgetItem("%s" % value)
			self.proTable.setItem(count, 1, item)
			count = count + 1
		self.proTable.resizeColumnsToContents()
	
	def updateList(self):
		# update the dat files belonging to the currently opened sxm
		self.listWidget.clear()
		self.datfiles = self.alllist[self.currentsxm]
		#print self.datfiles
		self.listWidget.addItems(self.datfiles)

	def selectRegion(self):
		if self.select_rect != None:
			self.imagePlot.plot.del_item(self.select_rect)
		self.select_rect = None
		if self.matchrects != None:
			self.imagePlot.plot.del_items(self.matchrects)
		self.matchrects = []
		#if self.
		param = ShapeParam()
		param.title = "region selected"
		x1 = self.nanofile.header['scan_pixels'][0]/2
		y1 = self.nanofile.header['scan_pixels'][1]/2
		x2 = x1 - 20
		y2 = y1 - 20
		self.select_rect = RectangleShape(x1,y1,x2,y2,param)
		self.select_rect.set_movable(True)
		self.select_rect.set_resizable(True)
		self.select_rect.set_selectable(True)
		self.select_rect.set_rotatable(True)
		self.imagePlot.plot.add_item(self.select_rect)
		self.imagePlot.plot.replot()
		self.imagePlot.plot.select_item(self.select_rect)
	
	def getSelectRegion(self):
		#if self.matchrects != None:
			#for rect in self.datrects:
		#	self.imagePlot.plot.del_items(self.matchrects)
		#self.matchrects = []
		#coor = self.select_rect.get_bounding_rect_coords()
		#coor2 = self.select_rect.get_center()
		coor3 = self.select_rect.get_points()
		co1 = coor3[0]  # top right, maximal x and y
		co2 = coor3[2]  # bottom left, minimal x and y
		print co1
		print co2
		self.select_region = self.currentdata[co2[1]:co1[1],co2[0]:co1[0]]
		self.currentdata = self.currentdata.astype(np.float32,copy=False)
		self.select_region = self.select_region.astype(np.float32,copy=False)
		print self.currentdata.dtype
		print self.select_region.dtype
		w,h = self.select_region.shape
		print w
		print h
		res = cv2.matchTemplate(self.currentdata,self.select_region,cv2.TM_CCOEFF_NORMED)
		cv2.imshow("test",res)
		threshold = 0.9
		loc = np.where( res >= threshold)
		if self.matchrects != None:
			self.imagePlot.plot.del_items(self.matchrects)
		self.matchrects = []
		num = 0
		loc_find = []
		for pt in zip(*loc[::-1]):
			#print pt
			if num == 0:
				x1 = pt[0]
				y1 = pt[1]
				print pt
				x2 = x1 + h
				y2 = y1 + w
				loc_find.append([x1,y1])
				rect = RectangleShape(x1,y1,x2,y2)
				self.matchrects.append(rect)
			else:
				x1 = pt[0]
				y1 = pt[1]
				if abs(x1 - loc_find[-1][0])+abs(y1 - loc_find[-1][1]) > (w+h)/3:
					print pt
					loc_find.append([x1,y1])
					x2 = x1 + h
					y2 = y1 + w
					rect = RectangleShape(x1,y1,x2,y2)
					self.matchrects.append(rect)
				#x2 = x1 + h
				#y2 = y1 + w
			num = num + 1
			#rect = RectangleShape(x1,y1,x2,y2)
			#self.matchrects.append(rect)
		print num
		for rect in self.matchrects:
			self.imagePlot.plot.add_item(rect)	
		self.imagePlot.plot.replot()
		
	
	
	def updateDatPosition(self):
		if self.datrects != None:
			#for rect in self.datrects:
			self.imagePlot.plot.del_items(self.datrects)
		self.datrects = []
		#temp_dat = None
		# read the coordinates from the dat files belonging to the currently opened sxm
		for line in self.datfiles:
			filepath = os.path.join(self.currentdir,line)
			temp_dat = nd.NanonisDat(filepath)
			temp_x = float(temp_dat.header['X (m)'])*1000000000
			temp_y = float(temp_dat.header['Y (m)'])*1000000000
			self.datcoor[line] = [temp_x,temp_y]
		# read the coordinates into the self.datcoor	
		# calculate the left-bottom coordinate of the current sxm
		x_abso = self.nanofile.header['scan_offset'][0]*1000000000 - self.nanofile.header['scan_range'][0]*1000000000/2
		y_abso = self.nanofile.header['scan_offset'][1]*1000000000 - self.nanofile.header['scan_range'][0]*1000000000/2
		#print str(x_abso) + " " + str(y_abso)
		for line in self.datfiles:
			temp_x = self.datcoor[line][0]
			temp_y = self.datcoor[line][1]
			x = -(x_abso - temp_x) * self.scale_factor
			y = -(y_abso - temp_y) * self.scale_factor
			#print str(x) + " " + str(y)
			x1 = x - 2
			y1 = y + 2
			x2 = x + 2
			y2 = y - 2
			rect = RectangleShape(x1,y1,x2,y2)
			#num = line.strip().split(".")
			#print num
			#num = num[-2][-3:]
			 
			#print num
			#param = AnnotationParam()
			#param.title = num
			#anno = AnnotatedPoint(x,y, param)
			#anno.set_label_visible(False)
			self.datrects.append(rect)
			#self.datannos.append(anno)
			#self.datchannelComboBox.clear()
			#self.datchannelComboBox.addItem(temp_dat)
			
		for rect in self.datrects:
			self.imagePlot.plot.add_item(rect)
		#for item in self.datannos:
		#	self.imagePlot.plot.add_item(item)
			
		self.imagePlot.plot.replot()
			#self.addRect(int(x),int(y))	

		# draw the position of these dat files
		
	
	def updateImage(self):
		self.clearImage()
		# update the image and also its properties
		temp1 = self.forbackComboBox.currentIndex()
		temp2 = self.channelComboBox.currentIndex()
		data = self.nanofile.data[temp2*2+temp1].data*100000000
		data = self.updateImageProcess(data)
		self.currentdata = data
		self.image.set_data(data)
		#self.imagePlot.plot.set_aspect_ratio(1.00, True)
		self.imagePlot.plot.replot()
		self.imagePlot.plot.set_axis_limits('left',0,self.nanofile.header['scan_pixels'][0])
		self.imagePlot.plot.set_axis_limits('bottom',0,self.nanofile.header['scan_pixels'][1])
		#self.imagePlot.plot.set_axis_scale('left',0,self.nanofile.header['scan_range'][0])
		#self.imagePlot.plot.set_axis_scale('bottom',0,self.nanofile.header['scan_range'][1])
		self.imagePlot.plot.select_item(self.image)
		
	def clearImage(self):
		if self.select_rect != None:
			self.imagePlot.plot.del_item(self.select_rect)
		self.select_rect = None
		if self.matchrects != None:
			self.imagePlot.plot.del_items(self.matchrects)
		self.matchrects = []
		
	def updateImageProcess(self, data):
		temp_index = self.processComboBox.currentIndex()
		# row data, no processing
		if temp_index == 0:
			pass
		# substract mean
		elif temp_index == 1:
			#print data
			# first calculate the mean of each row
			row_mean = np.mean(data,axis=1)
			#print row_mean
			data = (data.T - row_mean).T
			#print data
		# substract slope	
		elif temp_index == 2:
			data_temp = data.T
			n = self.nanofile.header['scan_pixels'][0]
			#print n
			xi = np.arange(n)
			#print xi
			x= np.array([xi,np.ones(n)])
			w = np.linalg.lstsq(x.T,data_temp)[0]
			data_sub = np.zeros([n,n])
			X = np.array([xi,]*int(n)).T
			Y = (X*w[0]).T
			data = data - Y
		# substract linear fit
		elif temp_index == 3:
			data_temp = data.T
			n = self.nanofile.header['scan_pixels'][0]
			xi = np.arange(n)
			x= np.array([xi,np.ones(n)])
			w = np.linalg.lstsq(x.T,data_temp)[0]
			data_sub = np.zeros([n,n])
			X = np.array([xi,]*int(n)).T
			Y = (X*w[0] + w[1]).T
			data = data - Y
		else:
			pass
		return data
		
	def updateImageInfo(self):
		self.channelComboBox.clear()
		channels = []
		for item in self.nanofile.header['data_info']:
			channels.append(item['Name'])
		self.channelComboBox.addItems(channels)
		x = self.nanofile.header['scan_offset'][0]*1000000000
		y = self.nanofile.header['scan_offset'][1]*1000000000
		self.xshowLabel.setText("%0.2f nm" % x)
		self.yshowLabel.setText("%0.2f nm" % y)
			
		
	def updateSpec(self):
		if self.speclist != None:
			self.curvePlot.plot.del_items(self.speclist)
		if self.dathighlights != None:
			self.imagePlot.plot.del_items(self.dathighlights)
		self.dathighlights = []
		self.speclist = []
		temp_list = self.listWidget.selectedItems()
		temp_index = self.datchannelComboBox.currentIndex()
		#for item in temp_list:
		#	print str(item.text())
		#print temp_list
		num_curves = len(temp_list)
		r = 0
		g = 0
		b = 0
		num = 0
		for line in temp_list:
			#print str(line.text())
			temp_str = str(line.text())
			filepath = os.path.join(self.currentdir,temp_str)
			#print filepath
			datfile = nd.NanonisDat(filepath)
			datfile.loadDate()
			curve = make.curve(datfile.data[:,0],datfile.data[:,temp_index],color = QColor(r,g,b,255))
			if num%3 == 0:
				r = r + int(255/num_curves)*2
			elif num%3 == 1:
				g = g + int(255/num_curves)*2
			else:
				b = b + int(255/num_curves)*2
			self.speclist.append(curve)
			# highlights the coordinates of these selected dat files
			[x,y] = self.datcoor[temp_str]
			x_abso = self.nanofile.header['scan_offset'][0]*1000000000 - self.nanofile.header['scan_range'][0]*1000000000/2
			y_abso = self.nanofile.header['scan_offset'][1]*1000000000 - self.nanofile.header['scan_range'][0]*1000000000/2
			x = -(x_abso - x) * self.scale_factor
			y = -(y_abso - y) * self.scale_factor
			#print x
			#print y
			x1 = x - 4
			y1 = y + 4
			x2 = x + 4
			y2 = y - 4
			param = ShapeParam()
			#param.fill()
			hrect = RectangleShape(x1,y1,x2,y2)
			self.dathighlights.append(hrect)
			num = num + 1
			
		for item in self.speclist:
			self.curvePlot.plot.add_item(item)
		for item in self.dathighlights:
			self.imagePlot.plot.add_item(item)
		self.curvePlot.plot.replot()
		self.imagePlot.plot.replot()
			
	def addRect(self,x,y):
		x1 = x - 2
		y1 = y + 2
		x2 = x + 2
		y2 = y - 2
		#print str(x1) + " " + str(y1)
		rect = RectangleShape(x1,y1,x2,y2)
		self.imagePlot.plot.add_item(rect)
		self.imagePlot.plot.replot()
			


def main():
    app = QApplication(sys.argv)
    #app.setOrganizationName("Qtrac Ltd.")
    #app.setOrganizationDomain("qtrac.eu")
    #app.setApplicationName("Image Changer")
    #app.setWindowIcon(QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    app.exec_()


main()
