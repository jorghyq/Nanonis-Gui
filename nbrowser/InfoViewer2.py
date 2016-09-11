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
        if DEV == 0:
            self.count = 6
        else:
            self.count = 11
        self.showLayout = QtGui.QGridLayout()
        # first row
        self.labels = [['x[nm]','0','y[nm]','0'],
                       ['compl','YES','square','YES'],
                       ['size1[nm]','0','size2[nm]','0'],
                       ['pixel1','0','pixel2','0'],
                       ['U[V]','0','I[A]','0'],
                       ['ratio','0'],
                       ['ftype','0','fformat','0'],
                       ['type','0',list('01234'),'None'],
                       ['quality','0',list('012345'),'None'],
                       ['flat','0',list('01234'),'None'],
                       ['clean','0',list('0123'),'None']]
                     #  ['name', 'now', 'set to','predict'],
        for i, label in enumerate(self.labels):
            if i > self.count:
                break
            self.init_row(i, label)
        self.setLayout(self.showLayout)
        self.show()

    def update(self, param):
        for i, label in enumerate(self.labels):
            for j, item in enumerate(label):
                if not isinstance(item, list):
                    if item in param:
                        self.showLayout.itemAtPosition(i,j+1).widget().setText(f2s(param[item]))

    def init_row(self, row, items):
        for i,item in enumerate(items):
            if isinstance(item, list):
                combo = QtGui.QComboBox()
                combo.addItems(item)
                self.showLayout.addWidget(combo,row,i)
            else:
                label = QtGui.QLabel(item)
                self.showLayout.addWidget(label,row,i)
                if (i+1)%2 == 0:
                    label.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)
                else:
                    label.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Plain)
                    label.setLineWidth(2)

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
    infov.update({'x[nm]':2})
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
