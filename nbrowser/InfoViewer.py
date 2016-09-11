# This Class displays the 2D image and provide some functionslities to process
# it
import sys
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

class InfoViewer(QtGui.QWidget):
    # class to display image
    def __init__(self, DEV = 0, parent=None):
        super(InfoViewer, self).__init__(parent)
        #self.showLayout = QtGui.QGridLayout()
        self.h1Layout = QtGui.QHBoxLayout()
        self.h2Layout = QtGui.QHBoxLayout()
        self.h3Layout = QtGui.QHBoxLayout()
        # first row
        self.row1_pre = ['x[nm]: ','y[nm]: ','compl: ','square: ']
        self.r1_Layout = init_row(self.row1_pre)
        # second row
        self.row2_pre = ['s1[nm]: ','s2[nm]: ','p1: ','p2: ']
        self.r2_Layout = init_row(self.row2_pre)
        # third row
        self.row3_pre = ['U[V]: ','I[A]: ','ftype: ','fformat: ']
        self.r3_Layout = init_row(self.row3_pre)
        #
        self.vLayout = QtGui.QVBoxLayout()
        self.vLayout.addLayout(self.r1_Layout)
        self.vLayout.addLayout(self.r2_Layout)
        self.vLayout.addLayout(self.r3_Layout)
        # forth row
        if DEV == 1:
            self.row4_pre = ['type: ','set',list('01234'),'predict: ']
            self.r4_Layout = init_row(self.row4_pre)
            #print "row4 is done"
            self.row5_pre = ['quality: ,','set',list('012345'),'predict: ']
            self.r5_Layout = init_row(self.row5_pre)
            #print "row5 is done"
            self.row6_pre = ['flat: ','set',list('01234'),'predict: ']
            self.r6_Layout = init_row(self.row6_pre)
            #print "row6 is done"
            self.row7_pre = ['clean: ,','set',list('0123'),'predict: ']
            self.r7_Layout = init_row(self.row7_pre)
            #print "row7 is done"
            self.vLayout.addLayout(self.r4_Layout)
            self.vLayout.addLayout(self.r5_Layout)
            self.vLayout.addLayout(self.r6_Layout)
            self.vLayout.addLayout(self.r7_Layout)
        self.setLayout(self.vLayout)
        self.show()

    def update(self, param):
        self.row1 = ['x', 'y', 'complete', 'square']
        self.row2 = ['size1', 'size2', 'pixel1', 'pixel2']
        self.row3 = ['bias', 'current', 'filetype', 'fileformat']
        for i, item in enumerate(self.row1):
            if item in param:
                self.r1_Layout.itemAt(2*i+1).widget().setText(self.row1_pre[i]+f2s(param[item]))
        for i, item in enumerate(self.row2):
            if item in param:
                self.r2_Layout.itemAt(2*i+1).widget().setText(self.row2_pre[i]+f2s(param[item]))
        for i, item in enumerate(self.row3):
            if item in param:
                self.r3_Layout.itemAt(2*i+1).widget().setText(self.row3_pre[i]+f2s(param[item]))

#def update_row(self, layout,)

def f2s(input):
    if isinstance(input, str):
        return input
    else:
        return "{0:.1f}".format(input)


def init_row(names):
    hLayout = QtGui.QHBoxLayout()
    for name in names:
        if isinstance(name, list):
            combo = QtGui.QComboBox()
            combo.addItems(name)
            #for item in name:
            #    combo.addITem
            hLayout.addWidget(combo)
        else:
            label = QtGui.QLabel(name)
            label.setFrameStyle(QtGui.QFrame.Panel)
            label.setLineWidth(2)
            hLayout.addWidget(label)
    return hLayout

def main():
    app = QtGui.QApplication(sys.argv)
    #win = QtGui.QMainWindow()
    #win.resize(400,400)
    infov = InfoViewer(1)
    #win.setCentralWidget(imv)
    infov.show()
    #win.show()
    infov.update({'x':2})
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
