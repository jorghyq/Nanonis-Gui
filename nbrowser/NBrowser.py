# This Class provide the browser for nanonis files
import sys
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
from Data2D import Data2D
from FileSelector import FileSelector
from InfoViewer import InfoViewer
from ImageViewer import ImageViewer

class NBrowser(QtGui.QWidget):
        def __init__(self, parent=None):
            super(NBrowser, self).__init__(parent)
            self.vmainLayout = QtGui.QVBoxLayout()
            self.hmainLayout = QtGui.QHBoxLayout()
            self.fs = FileSelector()
            self.imv = ImageViewer()
            self.info = InfoViewer(1)
            self.vmainLayout.addWidget(self.fs)
            self.vsecondLayout = QtGui.QVBoxLayout()
            self.hmainLayout.addWidget(self.imv)
            self.vsecondLayout.addWidget(self.info)
            self.vsecondLayout.addItem(QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding))
            self.hmainLayout.addLayout(self.vsecondLayout)
            self.vmainLayout.addLayout(self.hmainLayout)
            self.setLayout(self.vmainLayout)
            self.show()

            self.connect(self.fs.selectComboBox, QtCore.SIGNAL("currentIndexChanged(int)"),self.update_all)

        def update_all(self):
            #print 'update all'
            self.imv.update_all(self.fs.param,self.fs.data)
            self.info.update_info(self.fs.param)

def main():
    app = QtGui.QApplication(sys.argv)
    nb = NBrowser()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
