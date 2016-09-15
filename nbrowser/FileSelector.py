# This Class displays the 2D image and provide some functionslities to process
# it
import sys
import os
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
from Data2D import Data2D

class FileSelector(QtGui.QWidget):
    # class to display image
    def __init__(self, parent=None):
        self.data2d = Data2D()
        self.data = None
        self.param = None
        super(FileSelector, self).__init__(parent)
        self.vmainLayout = QtGui.QVBoxLayout()
        self.hopenLayout = QtGui.QHBoxLayout()
        self.hsaveLayout = QtGui.QHBoxLayout()
        self.vmainLayout.addLayout(self.hopenLayout)
        self.vmainLayout.addLayout(self.hsaveLayout)
        # hopenLayout
        self.pathLabel = QtGui.QLabel('path')
        self.selectComboBox = QtGui.QComboBox()
        self.selectComboBox.setFixedWidth(250)
        self.firstButton = QtGui.QPushButton(" <&f| ")
        self.firstButton.setFixedWidth(30)
        self.forwardButton = QtGui.QPushButton(" &n> ")
        self.forwardButton.setFixedWidth(30)
        self.backwardButton = QtGui.QPushButton(" <&b ")
        self.backwardButton.setFixedWidth(30)
        self.lastButton = QtGui.QPushButton(" |&l> ")
        self.lastButton.setFixedWidth(30)
        self.loadButton = QtGui.QPushButton("&Load")
        self.loadButton.setFixedWidth(100)
        self.hopenLayout.addWidget(self.pathLabel,4)
        self.hopenLayout.addWidget(self.selectComboBox,4)
        #self.hopenLayout.addStretch(1)
        self.hopenLayout.addWidget(self.firstButton)
        self.hopenLayout.addWidget(self.backwardButton)
        self.hopenLayout.addWidget(self.forwardButton)
        self.hopenLayout.addWidget(self.lastButton)
        self.hopenLayout.addWidget(self.loadButton)
        # hsaveLayout
        self.save_preLabel = QtGui.QLabel('SaveTo:')
        self.save_preLabel.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Plain)
        self.save_preLabel.setLineWidth(2)
        self.saveLabel = QtGui.QLabel('  ')
        self.saveLabel.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)
        self.resetButton = QtGui.QPushButton('&Reset')
        self.resetButton.setFixedWidth(100)
        self.setButton = QtGui.QPushButton('&Set')
        self.setButton.setFixedWidth(100)
        self.hsaveLayout.addWidget(self.save_preLabel)
        self.hsaveLayout.addWidget(self.saveLabel,5)
        self.hsaveLayout.addWidget(self.resetButton)
        self.hsaveLayout.addWidget(self.setButton)
        self.setLayout(self.vmainLayout)
        self.show()

        # Signal handling
        self.connect(self.loadButton, QtCore.SIGNAL("clicked()"), self.choose_dir)
        self.connect(self.firstButton, QtCore.SIGNAL("clicked()"), self.go_first)
        self.connect(self.forwardButton, QtCore.SIGNAL("clicked()"), self.go_forward)
        self.connect(self.backwardButton, QtCore.SIGNAL("clicked()"), self.go_backward)
        self.connect(self.lastButton, QtCore.SIGNAL("clicked()"), self.go_last)
        self.connect(self.resetButton, QtCore.SIGNAL("clicked()"), self.savedir_reset)
        self.connect(self.setButton, QtCore.SIGNAL("clicked()"), self.savedir_set)
        self.connect(self.selectComboBox, QtCore.SIGNAL("currentIndexChanged(int)"),self.open_file)

    def choose_dir(self):
        dname = unicode(QtGui.QFileDialog.getExistingDirectory(self, "Open Directory"))
        print dname
        nfirst = None
        files = {}
        if os.path.isdir(dname):
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
            self.nanofile = None
            self.currentsxm = None
            self.currentdata = None
            # set the path label
            self.currentdir = dname
            self.pathLabel.setText(dname)
            self.saveLabel.setText(dname)
            for line in os.listdir(dname):
                filepath = os.path.join(self.currentdir,line)
                #print line
                if os.path.isfile(filepath):
                    line = os.path.basename(line)
                    name,ext = os.path.splitext(line)
                    if ext[1:] == "sxm":
                        self.sxmlist.append(line)
                        self.sxmlist_time[line] = os.path.getctime(filepath)
                        files[line] = os.path.getmtime(filepath)
                        #print line +" "+ str(self.sxmlist_time[line])
                    elif ext[1:] == "dat":
                        self.datlist_time[line] = os.path.getctime(filepath)
                        self.datlist.append(line)
                        files[line] = os.path.getmtime(filepath)
                        #print line +" "+ str(self.datlist_time[line])
            nfiles = sorted(files.items(), key=lambda files:files[1])
            #print nfiles
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
            temp_ind = sxmindex[-1]
            sortedfiles[nfiles[temp_ind][0]] = []
            for j in range(temp_ind+1,len(nfiles)):
                sortedfiles[nfiles[temp_ind][0]].append(nfiles[j][0])
            self.alllist = sortedfiles
            self.selectComboBox.clear()
            self.selectComboBox.addItems(self.sxmlist)

    def open_file(self):
        fname = unicode(self.selectComboBox.currentText())
        fname = os.path.join(self.currentdir,fname)
        if fname:
            self.data2d.load(fname)
            self.data = self.data2d.get_data()
            self.param = self.data2d.get_param()
            #self.FILELOADED = True
        #else:
            #self.FILELOADED = False

    def go_first(self):
        active = self.selectComboBox.currentIndex()
        if active < 0:
            pass
        else:
            self.selectComboBox.setCurrentIndex(0)

    def go_backward(self):
        active = self.selectComboBox.currentIndex()
        if active < 0:
            pass
        elif active == 0:
            pass
        else:
            self.selectComboBox.setCurrentIndex(active-1)

    def go_forward(self):
        active = self.selectComboBox.currentIndex()
        if active < 0:
            pass
        elif active == (self.selectComboBox.count()-1):
            pass
        else:
            self.selectComboBox.setCurrentIndex(active+1)

    def go_last(self):
        active = self.selectComboBox.currentIndex()
        if active < 0:
            pass
        else:
            self.selectComboBox.setCurrentIndex(self.selectComboBox.count()-1)

    def savedir_reset(self):
        self.savedir = self.currentdir
        self.saveLabel.setText(self.savedir)

    def savedir_set(self):
        self.savedir = unicode(QtGui.QFileDialog.getExistingDirectory(self, "Open Directory"))
        self.saveLabel.setText(self.savedir)

def f2s(input):
    if isinstance(input, str):
        return input
    else:
        return "{0:.1f}".format(input)

def main():
    app = QtGui.QApplication(sys.argv)
    #win = QtGui.QMainWindow()
    #win.resize(400,400)
    fs = FileSelector()
    #win.setCentralWidget(imv)
    fs.show()
    #win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
