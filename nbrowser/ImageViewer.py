# This Class displays the 2D image and provide some functionslities to process
# it
import sys
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
from Data2D import Data2D
#from FileSelector import FileSelector

class ImageViewer(QtGui.QWidget):
    # class to display image
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.current_channel = None
        self.current_process = None
        self.last_channel_text = None
        self.last_process = None
        self.current_contrast = None
        self.last_contrast = None
        self.param = None
        self.data = None
        self.vLayout = QtGui.QVBoxLayout()
        self.hLayout = QtGui.QHBoxLayout()
        self.channelComboBox = QtGui.QComboBox()
        #self.directQScrollBar = QtGui.QScrollBar(1)
        self.processComboBox = QtGui.QComboBox()
        self.processComboBox.addItems(['None','Sub mean','Sub slope','Sub linear fit'])
        self.contrastComboBox = QtGui.QComboBox()
        self.contrastComboBox.addItems(['full range', 'setting1', 'setting2'])
        self.hLayout.addWidget(self.channelComboBox)
        #self.hLayout.addWidget(self.directQScrollBar)
        self.hLayout.addWidget(self.processComboBox)
        self.hLayout.addWidget(self.contrastComboBox)
        self.vLayout.addLayout(self.hLayout)
        self.imv = pg.ImageView()
        #self.imv.setFixedHeight(400)
        self.imv.setFixedWidth(600)
        self.vLayout.addWidget(self.imv)
        #self.setCentralWidget(self.vLayout)
        self.setLayout(self.vLayout)
        self.show()
        self.connect(self.channelComboBox, QtCore.SIGNAL("currentIndexChanged(int)"),self.update_img)
        self.connect(self.processComboBox, QtCore.SIGNAL("currentIndexChanged(int)"),self.update_img)
        self.connect(self.contrastComboBox, QtCore.SIGNAL("currentIndexChanged(int)"),self.update_img)

    def update_img(self):
        self.current_channel = self.channelComboBox.currentIndex()
        if self.current_channel >= 0:
            self.current_process= self.processComboBox.currentIndex()
            self.last_channel_text = self.channelComboBox.currentText()
            self.last_process = self.current_process
            self.current_contrast = self.contrastComboBox.currentIndex()
            self.last_contrast = self.current_contrast
            print "last channel text is set to", self.last_channel_text
            self.currentdata = self.data[str(self.current_channel)]
            self.currentdata = self.currentdata.dropna().values.T
            self.currentdata = np.fliplr(self.currentdata)
            self.currentdata = self.process_img(self.currentdata)
            self.contrast_img()
            #print self.currentdata.shape
            self.imv.setImage(self.currentdata)

    def update_all(self,param,data):
        self.param = param
        self.data = data
        if 'fullchannels' in self.param:
            # record the channel
            if self.last_channel_text:
                print "history channel exists:", self.last_channel_text
                if self.last_channel_text in self.param['fullchannels']:
                    self.current_channel = self.param['fullchannels'].index(self.last_channel_text)
                    print self.current_channel
                    print "initialize channel set to the history:", self.last_channel_text
                else:
                    self.current_channel = 0
                    #self.last_channel_text = self.channelComboBox.currentText()
            else:
                self.current_channel = 0
            self.channelComboBox.clear()
            self.channelComboBox.addItems(self.param['fullchannels'])
            self.channelComboBox.setCurrentIndex(self.current_channel)
            self.last_channel_text = self.channelComboBox.currentText()
            # record the process
            if self.last_process:
                self.current_process = self.last_process
                self.processComboBox.setCurrentIndex(self.current_process)
            else:
                self.last_process = 0
                self.processComboBox.setCurrentIndex(0)
            #self.update_img()

    def process_img(self,data):
        print data.shape,type(data)
        # nothing
        if self.current_process == 0:
            pass
        # subtract mean
        elif self.current_process == 1:
            row_mean = np.mean(data,axis=0)
            data = (data - row_mean)
        # subtract slope
        elif self.current_process == 2:
            data_temp = data.T
            n = data_temp.shape[0]
            m = data_temp.shape[1]
            print n, m
            xi = np.arange(n)
            x= np.array([xi,np.ones(n)]).T
            w = np.linalg.lstsq(x,data_temp)[0]
            X = np.array([xi,]*int(m)).T
            Y = (X*w[0]).T
            data = data - Y
        # subtract linear fit
        elif self.current_process == 3:
            data_temp = data.T
            n = data_temp.shape[0]
            m = data_temp.shape[1]
            xi = np.arange(n)
            x= np.array([xi,np.ones(n)]).T
            w = np.linalg.lstsq(x,data_temp)[0]
            X = np.array([xi,]*int(m)).T
            Y = (X*w[0] + w[1]).T
            data = data - Y
        #else:
            pass
        return data

    def contrast_img(self):
        if self.current_contrast == 0:
            pass
        elif self.current_contrast == 1:
            pass
        elif self.current_contrast == 2:
            pass
        else:
            pass

def main():
    app = QtGui.QApplication(sys.argv)
    imv = ImageViewer()
    d2d = Data2D()
    d2d.load('../test/A151125.005114-01292.sxm')
    imv.update_all(d2d.get_param(),d2d.get_data())
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
