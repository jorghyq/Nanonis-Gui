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
        row1 = ['x[nm]','0','y[nm]','0','compl','YES','square','YES']
        self.r1_Layout = init_row(row1)
        self.x_preLabel = QtGui.QLabel('x[nm]')
        self.xLabel = QtGui.QLabel('0')
        self.y_preLabel = QtGui.QLabel('y[nm]')
        self.yLabel = QtGui.QLabel('0')
        self.complete_preLabel = QtGui.QLabel('compl')
        self.completeLabel = QtGui.QLabel('YES')
        self.square_preLabel = QtGui.QLabel('square')
        self.squareLabel = QtGui.QLabel('YES')
        # second row
        row2 = ['s1[nm]','0','s2[nm]','0','p1','0','p2','0']
        self.r2_Layout = init_row(row2)
        self.size1_preLabel = QtGui.QLabel('s1[nm]')
        self.size1Lable = QtGui.QLabel('0')
        self.size2_preLabel = QtGui.QLabel('s2[nm]')
        self.size2Label = QtGui.QLabel('0')
        self.pixel1_preLabel = QtGui.QLabel('p1')
        self.pixel1Label = QtGui.QLabel('0')
        self.pixel2_preLabel = QtGui.QLabel('p2')
        self.pixel2Label = QtGui.QLabel('0')
        # third row
        row3 = ['U[V]','0','I[A]','0','ftype','0','fformat','0']
        self.r3_Layout = init_row(row3)
        self.bias_preLabel = QtGui.QLabel('U[V]')
        self.biasLabel = QtGui.QLabel('0')
        self.current_preLabel = QtGui.QLabel('I(A)')
        self.currentLabel = QtGui.QLabel('0')
        self.filetype_preLabel = QtGui.QLabel('ftype')
        self.filetypeLabel = QtGui.QLabel('0')
        self.fileformat_preLabel = QtGui.QLabel('fformat')
        self.fileformatLabel = QtGui.QLabel('0')
        #
        self.vLayout = QtGui.QVBoxLayout()
        self.vLayout.addLayout(self.r1_Layout)
        self.vLayout.addLayout(self.r2_Layout)
        self.vLayout.addLayout(self.r3_Layout)
        # forth row
        if DEV == 1:
            row4 = ['type','0','set',list('01234'),'predict','0']
            self.r4_Layout = init_row(row4)
            #print "row4 is done"
            row5 = ['quality','0','set',list('012345'),'predict','0']
            self.r5_Layout = init_row(row5)
            #print "row5 is done"
            row6 = ['flat','0','set',list('01234'),'predict','0']
            self.r6_Layout = init_row(row6)
            #print "row6 is done"
            row7 = ['clean','0','set',list('0123'),'predict','0']
            self.r7_Layout = init_row(row7)
            #print "row7 is done"
            self.vLayout.addLayout(self.r4_Layout)
            self.vLayout.addLayout(self.r5_Layout)
            self.vLayout.addLayout(self.r6_Layout)
            self.vLayout.addLayout(self.r7_Layout)
        self.setLayout(self.vLayout)
        self.show()

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
            hLayout.addWidget(QtGui.QLabel(name))
    return hLayout

def main():
    app = QtGui.QApplication(sys.argv)
    #win = QtGui.QMainWindow()
    #win.resize(400,400)
    infov = InfoViewer(1)
    #win.setCentralWidget(imv)
    infov.show()
    #win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
