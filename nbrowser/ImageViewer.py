# This Class displays the 2D image and provide some functionslities to process
# it
import sys
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
from Data2D import Data2D
from FileSelector import FileSelector

class ImageViewer(QtGui.QWidget):
    # class to display image
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.current_channel = None
        self.current_process = None
        self.param = None
        self.data = None
        self.vLayout = QtGui.QVBoxLayout()
        self.hLayout = QtGui.QHBoxLayout()
        self.channelComboBox = QtGui.QComboBox()
        #self.directQScrollBar = QtGui.QScrollBar(1)
        self.processComboBox = QtGui.QComboBox()
        self.processComboBox.addItem('None')
        self.hLayout.addWidget(self.channelComboBox)
        #self.hLayout.addWidget(self.directQScrollBar)
        self.hLayout.addWidget(self.processComboBox)
        self.vLayout.addLayout(self.hLayout)
        self.imv = pg.ImageView()
        self.imv.setFixedHeight(500)
        self.imv.setFixedWidth(500)
        self.vLayout.addWidget(self.imv)
        #self.setCentralWidget(self.vLayout)
        self.setLayout(self.vLayout)
        self.show()
        self.connect(self.channelComboBox, QtCore.SIGNAL("currentIndexChanged(int)"),self.update_img)
        self.connect(self.processComboBox, QtCore.SIGNAL("currentIndexChanged(int)"),self.update_img)

    def update_img(self):
        self.current_channel = self.channelComboBox.currentIndex()
        self.current_process = self.processComboBox.currentIndex()
        self.imv.setImage(self.data[str(self.current_channel)].values.astype('<f4'))

    def update_all(self,param,data):
        self.param = param
        self.data = data
        if 'fullchannels' in self.param:
            self.channelComboBox.addItems(self.param['fullchannels'])
            self.update_img()

def main():
    class Test(QtGui.QWidget):
        def __init__(self, parent=None):
            super(Test, self).__init__(parent)
            self.vmainLayout = QtGui.QVBoxLayout()
            self.fs = FileSelector()
            self.imv = ImageViewer()
            self.vmainLayout.addWidget(self.fs)
            self.vmainLayout.addWidget(self.imv)
            self.setLayout(self.vmainLayout)
            self.show()

            self.connect(self.fs.selectComboBox, QtCore.SIGNAL("currentIndexChanged(int)"),self.update_all)

        def update_all(self):
            print 'update all'
            self.imv.update_all(self.fs.param,self.fs.data)
    app = QtGui.QApplication(sys.argv)
    #win = QtGui.QMainWindow()
    #win.resize(400,400)
    test = Test()
    #win.setCentralWidget(imv)
    #imv.update_img(np.random.rand(10,10))
    #win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
