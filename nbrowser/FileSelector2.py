# This Class displays the 2D image and provide some functionslities to process
# it
import sys
import os
import numpy as np
import random
import pandas as pd
from ast import literal_eval
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
from Data2D import Data2D

class FileSelector2(QtGui.QWidget):
    # class to display image
    def __init__(self, parent=None):
        super(FileSelector2, self).__init__(parent)
        self.data2d = Data2D()
        self.data = None
        self.db = None
        self.db_selected = None
        self.param = None
        self.num_select = 4
        self.select_param = {}
        #for i in range(self.num_select):
        #    self.select_param['select'+str(i)] = None
        self.vmainLayout = QtGui.QVBoxLayout()
        self.hopenLayout = QtGui.QHBoxLayout()
        self.hfileLayout = QtGui.QHBoxLayout()
        self.hselectLayout1 = QtGui.QHBoxLayout()
        self.hselectLayout2 = QtGui.QHBoxLayout()
        # hopenLayout
        self.pathLabel = QtGui.QLabel('path')
        self.selectComboBox = QtGui.QComboBox()
        self.selectComboBox.setFixedWidth(250)
        self.randomComboBox = QtGui.QComboBox()
        self.randomComboBox.addItems(['in Order','random'])
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
        self.updateButton = QtGui.QPushButton("&Update")
        self.updateButton.setFixedWidth(100)
        self.hopenLayout.addWidget(self.pathLabel,4)
        self.hopenLayout.addWidget(self.loadButton)
        self.hopenLayout.addWidget(self.updateButton)
        # hfileLayout
        self.setButton = QtGui.QPushButton("&Set dir")
        self.dirLabel = QtGui.QLabel('pre_dir')
        self.hfileLayout.addWidget(self.dirLabel)
        self.hfileLayout.addWidget(self.selectComboBox,4)
        self.hfileLayout.addWidget(self.randomComboBox)
        #self.hopenLayout.addStretch(1)
        self.hfileLayout.addWidget(self.firstButton)
        self.hfileLayout.addWidget(self.backwardButton)
        self.hfileLayout.addWidget(self.forwardButton)
        self.hfileLayout.addWidget(self.lastButton)
        self.hfileLayout.addWidget(self.setButton)
        # hsaveLayout
        self.select = self.add_select_gui(self.num_select)
        self.vmainLayout.addLayout(self.hfileLayout)
        self.vmainLayout.addLayout(self.hopenLayout)
        #self.vmainLayout.addLayout(self.hselectLayout1)
        #self.vmainLayout.addLayout(self.hselectLayout2)
        for item in self.select:
            self.vmainLayout.addLayout(item)

        self.setLayout(self.vmainLayout)
        self.show()

        # Signal handling
        self.connect(self.loadButton, QtCore.SIGNAL("clicked()"), self.choose_file)
        self.connect(self.firstButton, QtCore.SIGNAL("clicked()"), self.go_first)
        self.connect(self.forwardButton, QtCore.SIGNAL("clicked()"), self.go_forward)
        self.connect(self.backwardButton, QtCore.SIGNAL("clicked()"), self.go_backward)
        self.connect(self.lastButton, QtCore.SIGNAL("clicked()"), self.go_last)
        self.connect(self.updateButton, QtCore.SIGNAL("clicked()"), self.update_select)
        self.connect(self.setButton, QtCore.SIGNAL("clicked()"), self.choose_dir)
        self.connect(self.selectComboBox, QtCore.SIGNAL("currentIndexChanged(int)"),self.open_file)

    def add_select_gui(selfi,n):
        """ add gui for selecting wanted files """
        selectLayout = []
        for i in range(n):
            hlayout = QtGui.QHBoxLayout()
            fieldComboBox = QtGui.QComboBox()
            fieldComboBox.addItem("None")
            operationComboBox1 = QtGui.QComboBox()
            operationComboBox1.addItems(['None','>','=','<','!='])
            valueLine1 = QtGui.QLineEdit()
            valueLine1.setText("0")
            valueLine1.setFixedWidth(40)
            operationComboBox2 = QtGui.QComboBox()
            operationComboBox2.addItems(['None','>','=','<','!='])
            operationComboBox2.setCurrentIndex(4)
            valueLine2 = QtGui.QLineEdit()
            valueLine2.setText("0")
            valueLine2.setFixedWidth(40)
            hlayout.addWidget(fieldComboBox,4)
            hlayout.addWidget(operationComboBox1)
            hlayout.addWidget(valueLine1)
            hlayout.addWidget(operationComboBox2)
            hlayout.addWidget(valueLine2)
            selectLayout.append(hlayout)
            #self.connect(fieldComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.update_select)
            #self.connect(valueLine1, QtCore.SIGNAL("editingFinished()"),self.update_select)
        return selectLayout

    def update_select(self):
        select = {}
        self.db = pd.read_csv(self.fname,converters={'process':literal_eval},index_col=0)
        for i, item in enumerate(self.select):
            field = str(item.itemAt(0).widget().currentText())
            operation1 = str(item.itemAt(1).widget().currentText())
            value1 = int(item.itemAt(2).widget().text())
            operation2 = str(item.itemAt(3).widget().currentText())
            value2 = int(item.itemAt(4).widget().text())
            #print i, field, operation1,value1,operation2,value2
            if field != 'None':
                if operation1 != 'None':
                    select[field] = []
                    select[field].append([operation1, value1])
                if operation2 != 'None':
                    select[field].append([operation2, value2])
            #self.select_param['select'+str(i)] = {field:[operation1,value1,operation2,value2]}
        #self.db_selected = self.db.copy(deep=True)
        if len(select) > 0:
            for key in select:
                for item in select[key]:
                    if item[0] == '>':
                        self.db = self.db.loc[self.db[key] > item[1]]
                    elif item[0] == '=':
                        self.db = self.db.loc[self.db[key] == item[1]]
        self.fnames = self.db['filename']
        self.fpaths = self.db['fullpath']
        self.sxmlist = list(self.fnames)
        self.num_sxm =  len(self.sxmlist)
        self.selectComboBox.clear()
        self.selectComboBox.addItems(self.sxmlist)
        self.selectComboBox.setCurrentIndex(0)


    def choose_dir(self):
        self.dname = unicode(QtGui.QFileDialog.getExistingDirectory(self, "Open Directory"))
        self.dirLabel.setText(self.dname)

    def choose_file(self):
        self.fname = unicode(QtGui.QFileDialog.getOpenFileName())
        print self.fname
        if os.path.isfile(self.fname):
            self.sxmlist = []
            self.nanofile = None
            self.currentsxm = None
            self.currentdata = None
            # set the path label
            self.pathLabel.setText(self.fname)
            #self.saveLabel.setText(dname)
            if os.path.isfile(self.fname):
                self.db = pd.read_csv(self.fname,converters={'process':literal_eval},index_col=0)
                #self.fnames = self.db['filename']
                #self.fpaths = self.db['fullpath']
                #self.sxmlist = list(self.fnames)
                #print self.columns
                #self.selectComboBox.clear()
                #self.selectComboBox.addItems(self.sxmlist)
                #self.selectComboBox.setCurrentIndex(0)
                self.columns = self.db.columns
                for item in self.select:
                    item.itemAt(0).widget().addItems(self.columns)


    def get_field_from_db(self,db,in_value,in_field,out_field):
        if in_field in self.columns and out_field in self.columns:
            return (db.loc[db[in_field] == in_value])[out_field].iloc[0]

    def open_file(self):
        fname = unicode(self.selectComboBox.currentText())
        print fname
        if fname:
            fpath = self.get_field_from_db(self.db,fname,'filename','fullpath')
            print fpath
            self.data2d.load(os.path.join(self.dname,fpath))
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
        rand = self.randomComboBox.currentIndex()
        random_id = random.randint(0,self.num_sxm-1)
        if active < 0:
            pass
        elif active == 0:
            if rand == 0:
                pass
            else:
                self.selectComboBox.setCurrentIndex(random_id)
        else:
            if rand == 0:
                self.selectComboBox.setCurrentIndex(active-1)
            else:
                self.selectComboBox.setCurrentIndex(random_id)


    def go_forward(self):
        active = self.selectComboBox.currentIndex()
        rand = self.randomComboBox.currentIndex()
        random_id = random.randint(0,self.num_sxm-1)
        if active < 0:
            pass
        elif active == (self.selectComboBox.count()-1):
            if rand == 0:
                pass
            else:
                self.selectComboBox.setCurrentIndex(random_id)
        else:
            if rand == 0:
                self.selectComboBox.setCurrentIndex(active+1)
            else:
                self.selectComboBox.setCurrentIndex(random_id)

    def go_last(self):
        active = self.selectComboBox.currentIndex()
        if active < 0:
            pass
        else:
            self.selectComboBox.setCurrentIndex(self.selectComboBox.count()-1)

    def savedir_reset(self):
        self.savedir = self.currentdir
        selectLayout = []
        for i in range(n):
            hlayout = QtGui.QHBoxLayout()
            fieldComboBox = QtGui.QComboBox()
            fieldComboBox.addItem("None")
            operationComboBox1 = QtGui.QComboBox()
            operationComboBox1.addItems(['>','>=','=','<=','<'])
            valueLine1 = QtGui.QLineEdit()
            valueLine1.setText("0")
            valueLine1.setFixedWidth(40)
            operationComboBox2 = QtGui.QComboBox()
            operationComboBox2.addItems(['>','>=','=','<=','<'])
            operationComboBox2.setCurrentIndex(4)
            valueLine2 = QtGui.QLineEdit()
            valueLine2.setText("0")
            valueLine2.setFixedWidth(40)
            hlayout.addWidget(fieldComboBox,4)
            hlayout.addWidget(operationComboBox1)
            hlayout.addWidget(valueLine1)
            hlayout.addWidget(operationComboBox2)
            hlayout.addWidget(valueLine2)
            selectLayout.append(hlayout)
        return selectLayout

def main():
    app = QtGui.QApplication(sys.argv)
    #win = QtGui.QMainWindow()
    #win.resize(400,400)
    fs = FileSelector2()
    #win.setCentralWidget(imv)
    fs.show()
    #win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
