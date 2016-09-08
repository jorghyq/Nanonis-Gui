# Class to handle the data needed for the GUI program
# Author:jorghyq


# This file pre parses the file and extract the important information
############################################
# filetype:     0     others               #
#               1     txt                  #
#               2     sxm                  #
#               3     dat                  #
#               4     3ds                  #
############################################
# fileformat:   0     STM                  #
#               1     AFM                  #
#               2     dI/dV map            #
#               3     dI/dV                #
#               4     Force curve          #
#               5     others               #
############################################

import pandas as pd
import os
from nanonisfile import NanonisFile

class Data2D:
    # Holding the generalized data for every data type

    def __init__(self):
        self.full_path = None
        self.__param = {}
        self.__data = None # Will be pandas Panel

    def load(self,path):
        self.full_path = path
        self.__param, self.__data = load_sxm(self.full_path)

    def get_param(self):
        return self.__param

    def get_data(self):
        return self.__data

    def print_param(self):
        for k, v in self.__param.iteritems():
            print k, v


m2nm = 1e9
columns = ['filename','filetype','fileformat','pixel1','pixel2',\
           'size1','size2','ratio','complete','quality','type','flat',\
           'fullpath']
type_dict = {'txt': 1, 'sxm': 2, 'dat': 3, '3ds': 4}

def load_sxm(path):
    dirname, filename= os.path.split(path)
    ending= filename.split('.')[-1]
    try:
        nfile = NanonisFile(path)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    ######## Prepare the parameter of the file
    param = {}
    param['filename'] = filename
    param['fullpath'] = path
    param['filetype'] = 0
    param['fileformat'] = 0
    param['complete'] = True
    param['square'] = True
    param['quality'] = 0
    param['type'] = 0
    param['flat'] = 0
    param['clean'] = 0
    param['ending']= ending
    if nfile.header['z-controller>controller status'] == 'ON':
        if nfile.header['z-controller>controller name'] == 'log Current':
            param['fileformat'] = 0 # constant current
    else:
        param['fileformat'] = 1 # constant height
    param['pixel1'] = nfile.header['scan_pixels'][0]
    param['pixel2'] = nfile.header['scan_pixels'][1]
    param['size1'] = round(nfile.header['scan_range'][0]*m2nm,1)
    param['size2'] = round(nfile.header['scan_range'][1]*m2nm,1)
    if param['size1'] == param['size2']:
        param['square'] = True
    else:
        param['square'] = False
    param['ratio'] = round((param['pixel1']*param['pixel2']/\
                                 (param['size1']*param['size2'])),1)
    param['acq_time'] = nfile.header['acq_time']
    scan_time = nfile.header['scan_time']
    full_time = param['pixel1']*scan_time[0] + param['pixel2']*scan_time[1]
    if abs(param['acq_time']-full_time) < 1:
        param['complete'] = True
    else:
        param['complete'] = False
    param['bias'] = nfile.header['bias']
    param['current'] = nfile.header['z-controller>setpoint']
    param['bias_unit'] = 'V'
    param['current_unit'] = nfile.header['z-controller>setpoint unit']
    param['channels'] = nfile.header['scan>channels'].split(';')
    param['fullchannels'] = []
    for i, item in enumerate(param['channels']):
        param['fullchannels'].append(item+'_F')
        param['fullchannels'].append(item+'_B')
    ############# Prepare the data of the file
    data = pd.Panel(major_axis=range(int(param['pixel1']))\
                                     ,minor_axis=range(int(param['pixel2'])))
    for i, item in enumerate(param['fullchannels']):
        data[str(i)] = nfile.data[i].data
    return param, data


if __name__ == "__main__":
    d2d = Data2D()
    d2d.load('../test/A151125.005114-01292.sxm')
    d2d.print_param()
