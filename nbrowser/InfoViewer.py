# This Class displays the 2D image and provide some functionslities to process
# it
import sys
#import numpy as np
import pandas as pd
from ast import literal_eval
from pyqtgraph.Qt import QtCore, QtGui
#import pyqtgraph as pg

#def ProcessParser(data):


class InfoViewer(QtGui.QWidget):
    # class to display image
    def __init__(self, DEV = 0, parent=None):
        super(InfoViewer, self).__init__(parent)
        self.data = None
        self.data_name = None
        self.DATALOADED = False
        self.EXISTED = False
        self.DEV = DEV
        self.vmainLayout = QtGui.QVBoxLayout()
        self.showLayout = QtGui.QGridLayout()
        # first row
        self.labels = [['x[nm]','0','y[nm]','0'],
                       ['compl','YES','square','YES'],
                       ['size1[nm]','0','size2[nm]','0'],
                       ['pixel1','0','pixel2','0'],
                       ['U[V]','0','I[A]','0'],
                       ['ratio','0','compl','YES'],
                       ['ftype','0','fformat','0']]
                     #  ['name', 'now', 'set to','predict'],
        for i, label in enumerate(self.labels):
            self.init_row(i, label, self.showLayout)
        self.vmainLayout.addLayout(self.showLayout)
        if self.DEV == 1:
            self.predictLayout = QtGui.QGridLayout()
            self.openButton = QtGui.QPushButton('Open')
            self.saveButton = QtGui.QPushButton('Save')
            self.statusLabel = QtGui.QLabel('None')
            self.sepLabel = QtGui.QLabel('Predictor:')
            self.sepLabel.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Plain)
            self.sepLabel.setLineWidth(3)
            self.predictLayout.addWidget(self.sepLabel,0,0)
            self.predictLayout.addWidget(self.openButton,0,1)
            self.predictLayout.addWidget(self.saveButton,0,2)
            self.predictLayout.addWidget(self.statusLabel,0,3)
            self.fileLabel = QtGui.QLabel('  ')
            self.predictLayout.addWidget(self.fileLabel,1,0,1,4)
            self.vmainLayout.addLayout(self.predictLayout)
            self.labels_predict = [['# Loaded', '0', 'Exist','No'],
                                ['type','0',list('0123456'),'0'],
                                ['quality','0',list('0123456'),'0'],
                                ['flat','0',list('012345'),'0'],
                                ['clean','0',list('01234'),'0'],
                                ['good','0',list('012'),'0']]
            for i, label in enumerate(self.labels_predict):
                self.init_row(i+2, label, self.predictLayout)
            self.connect(self.openButton,QtCore.SIGNAL("clicked()"),self.open_file)
            self.connect(self.saveButton,QtCore.SIGNAL("clicked()"),self.save_file)
            for i in [3,4,5,6]:
                self.associate(i)
        self.setLayout(self.vmainLayout)
        self.show()

    def associate(self, row):
        #label = self.predictLayout.itemAtPosition(row,1).widget()
        combo = self.predictLayout.itemAtPosition(row,2).widget()
        self.connect(combo,QtCore.SIGNAL("currentIndexChanged(int)"),self.update_row)

    def update_row(self):
        #print "update row"
        for row in [3,4,5,6]:
            label_pre = self.predictLayout.itemAtPosition(row,0).widget()
            text_pre = label_pre.text()
            label = self.predictLayout.itemAtPosition(row,1).widget()
            combo = self.predictLayout.itemAtPosition(row,2).widget()
            combo_current = combo.currentIndex()
            #print combo_current
            if combo_current != 0:
                #print text_pre
                #print self.columns.values
                if text_pre in self.columns.values.tolist():
                    #print "label exist in self.columns"
                    column_ind = self.columns.values.tolist().index(text_pre)
                    #print column_ind
                    if self.EXISTED:
                        self.data.ix[self.row_ind,column_ind] = combo_current
                        label.setText(f2s(combo_current))
                        #print self.data.iloc[self.row_ind]

    def open_file(self):
        fname = unicode(QtGui.QFileDialog.getOpenFileName())
        if fname[-3:] == 'csv':
            self.data_name = fname
            self.data = pd.read_csv(fname,converters={'process':literal_eval},index_col=0)
            self.fileLabel.setText(fname)
            self.statusLabel.setText('File Loaded')
            #print type(self.data)
            #print self.data.shape
            self.predictLayout.itemAtPosition(2,1).widget().setText(f2s(self.data.shape[0]))
            self.columns = self.data.columns
            self.DATALOADED = True
            self.update_predict()
        else:
            self.statusLabel.setText('File invalid')
            self.DATALOADED = False

    def save_file(self):
        self.data.to_csv(self.data_name)
        self.statusLabel.setText('Saved!')

    def update_info(self, param):
        self.param = param
        for i, label in enumerate(self.labels):
            for j, item in enumerate(label):
                if not isinstance(item, list):
                    if item in param:
                        self.showLayout.itemAtPosition(i,j+1).widget().setText(f2s(param[item]))
        if self.DEV == 1:
            self.update_predict()

    def update_predict(self):
        if self.DATALOADED:
            if 'filename' in self.param:
                filenames = self.data['filename']
                if (filenames == self.param['filename']).any():
                    self.predictLayout.itemAtPosition(2,3).widget().setText('YES')
                    self.EXISTED = True
                    temp = ['type','quality','clean','flat','good'] # for reseting the combobox
                    self.row_ind = filenames[filenames ==self.param['filename']].index[0]
                    row = self.data.iloc[self.row_ind]
                    for i, label in enumerate(self.labels_predict):
                        for j, item in enumerate(label):
                           if not isinstance(item, list):
                               if item in row:
                                   self.predictLayout.itemAtPosition(i+2,j+1).widget().setText(f2s(row[item]))
                                   if item in temp:
                                       self.predictLayout.itemAtPosition(i+2,j+2).widget().setCurrentIndex(0)

                else:
                    self.predictLayout.itemAtPosition(2,3).widget().setText('NO')
                    self.EXISTED = False
        else:
            pass

    def init_row(self, row, items, layout):
        for i,item in enumerate(items):
            if isinstance(item, list):
                combo = QtGui.QComboBox()
                combo.addItems(item)
                layout.addWidget(combo,row,i)
            else:
                label = QtGui.QLabel(item)
                layout.addWidget(label,row,i)
                if (i+1)%2 == 0:
                    label.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)
                else:
                    label.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Plain)
                    label.setLineWidth(2)

    def update_process(self, process_info):
        exist = 0
        channel = process_info.keys()[0]
        #print process_info, channel
        value = process_info[channel]
        #process_id = process_info[channel][0]
        #min_max = process_info[channel][1]
        if self.DATALOADED:
            # format of process_info should be {'channel':[process_id,[min,max]}
            if 'process' in self.columns.values.tolist():
                column_ind = self.columns.values.tolist().index('process')
                if self.EXISTED:
                    data = self.data.ix[self.row_ind,column_ind]
                    #print 'data: ', data
                    # if some channels already are saved
                    if len(data) != 0:
                        for i, item in enumerate(data):
                            #print 'item: ', i, item
                            if channel in item:
                                self.data.ix[self.row_ind,column_ind][i][channel] = value
                                exist = 1
                        if exist == 0:
                            self.data.ix[self.row_ind,column_ind].append(process_info)
                    else:
                        self.data.ix[self.row_ind,column_ind].append(process_info)
                #print self.data.ix[self.row_ind,column_ind]
            if 'read' in self.columns.values.tolist():
                column_ind = self.columns.values.tolist().index('read')
                self.data.ix[self.row_ind,column_ind] = 1

def f2s(input):
    if isinstance(input, str):
        return input
    else:
        return "{0:.1f}".format(input)

def main():
    app = QtGui.QApplication(sys.argv)
    #win = QtGui.QMainWindow()
    #win.resize(400,400)
    infov = InfoViewer(1)
    #win.setCentralWidget(imv)
    infov.show()
    #win.show()
    infov.update_info({'x[nm]':2})
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
