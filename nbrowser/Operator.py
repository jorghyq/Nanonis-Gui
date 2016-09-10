# This Class displays the 2D image and provide some functionslities to process
# it
import sys
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

class Operator(QtGui.QWidget):
    # class to display image
    def __init__(self, parent=None):
        super(Operator, self).__init__(parent)
        self.showLayout = QtGui.QGridLayout()
        self.
        self.hLayout = QtGui.QHBoxLayout()
        self.channelComboBox = QtGui.QComboBox()
        #self.directQScrollBar = QtGui.QScrollBar(1)
        self.processComboBox = QtGui.QComboBox()
        self.hLayout.addWidget(self.channelComboBox)
        #self.hLayout.addWidget(self.directQScrollBar)
        self.hLayout.addWidget(self.processComboBox)
        self.vLayout.addLayout(self.hLayout)
        self.imv = pg.ImageView()
        self.vLayout.addWidget(self.imv)
        #self.setCentralWidget(self.vLayout)
        self.setLayout(self.vLayout)
        self.show()



def main():
    app = QtGui.QApplication(sys.argv)
    #win = QtGui.QMainWindow()
    #win.resize(400,400)
    imv = ImageViewer()
    #win.setCentralWidget(imv)
    imv.show()
    #win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
