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

m2nm = 1e9
A2nA = 1e9
columns = ['filename','ftype','fformat','pixel1','pixel2','size1[nm]','size2[nm]',\
           'acq_time','ratio','square','complete','quality','type','flat','clean',\
           'fullpath','good','process','read']
type_dict = {'txt': 1, 'sxm': 2, 'dat': 3, '3ds': 4}

class Data2D:
    # Holding the generalized data for every data type

    def __init__(self):
        self.full_path = None
        self.LOADED = -1
        self.__param = {}
        self.__data = None # Will be pandas Panel
        self.columns = columns
        self.type_dict = type_dict

    def load(self,path):
        self.full_path = path
        #fpath, fname = os.path.split(self.full_path)
        if self.full_path[-3:] == 'sxm':
            self.__param, self.__data, self.LOADED = load_sxm(self.full_path)
            #print self.__param

    def get_param(self):
        return self.__param

    def get_data(self):
        return self.__data

    def print_param(self):
        for k, v in self.__param.iteritems():
            print k, v

    def output_to_csv(self):
        output = []
        for item in self.columns:
            if item in self.__param:
                output.append(self.__param[item])
        #print output
        return output

def load_sxm(path):
    dirname, filename= os.path.split(path)
    ending= filename.split('.')[-1]
    nfile = NanonisFile(path)
    #except IOError as e:
    #    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    if not nfile.LOADED:
        return None, None, -1
    ######## Prepare the parameter of the file
    param = {}
    param['filename'] = filename
    param['fullpath'] = path
    param['ftype'] = 2
    param['fformat'] = 0
    param['complete'] = True
    param['square'] = True
    param['quality'] = 0
    param['type'] = 0
    param['flat'] = 0
    param['clean'] = 0
    #param['cmin'] = 0.0
    #param['cmax'] = 0.0
    param['process'] = []
    param['read'] = 0
    param['good'] = 0
    param['ending']= ending
    #if 'z-controller>controller status' in nfile.header:
    #    if nfile.header['z-controller>controller status'] == 'ON':
    #        if nfile.header['z-controller>controller name'] == 'log Current':
    #            param['fformat'] = 0 # constant current
    #    else:
    #        param['fformat'] = 1 # constant height
    #else:
    # determine the file format
    if nfile.header['z-controller']['on'] == '1':
        if nfile.header['z-controller']['Name'] == 'log Current':
            param['fformat'] = 0
    else:
        param['fformat'] = 1
    param['x[nm]'] = round(nfile.header['scan_offset'][0]*m2nm,1)
    param['y[nm]'] = round(nfile.header['scan_offset'][1]*m2nm,1)
    param['pixel1'] = nfile.header['scan_pixels'][0]
    param['pixel2'] = nfile.header['scan_pixels'][1]
    param['size1[nm]'] = round(nfile.header['scan_range'][0]*m2nm,1)
    param['size2[nm]'] = round(nfile.header['scan_range'][1]*m2nm,1)
    if param['size1[nm]'] == param['size2[nm]']:
        param['square'] = True
    else:
        param['square'] = False
    if param['size1[nm]'] == 0 or param['size2[nm]'] == 0:
        param['ratio'] = 'Inf'
    else:
        param['ratio'] = round((param['pixel1']*param['pixel2']/\
                                (param['size1[nm]']*param['size2[nm]'])),1)
    param['acq_time'] = nfile.header['acq_time']
    scan_time = nfile.header['scan_time']
    full_time = param['pixel1']*scan_time[0] + param['pixel2']*scan_time[1]
    if abs(param['acq_time']-full_time) < 1:
        param['complete'] = True
    else:
        param['complete'] = False
    param['U[V]'] = nfile.header['bias']
    #param['I[A]'] = nfile.header['z-controller>setpoint']
    param['I[A]'], param['current_unit'] = nfile.header['z-controller']['Setpoint'].split(' ')
    param['bias_unit'] = 'V'
    #param['current_unit'] = nfile.header['z-controller>setpoint unit']
    #param['channels'] = nfile.header['scan>channels'].split(';')
    param['fullchannels'] = []
    #for i, item in enumerate(param['channels']):
    #    param['fullchannels'].append(item+'_F')
    #    param['fullchannels'].append(item+'_B')
    for i, item in enumerate(nfile.header['data_info']):
        if item['Direction'] == 'both':
            param['fullchannels'].append(item['Name']+'_('+item['Unit']+')_F')
            param['fullchannels'].append(item['Name']+'_('+item['Unit']+')_B')
        else:
            param['fullchannels'].append(item['Name']+'_('+item['Unit']+')')
    ############# Prepare the data of the file
    data = pd.Panel(major_axis=range(int(param['pixel1']))\
                                     ,minor_axis=range(int(param['pixel2'])))
    for i, item in enumerate(param['fullchannels']):
        data_temp = pd.DataFrame(nfile.data[i].data)
        #data_temp = data_temp.fillna(0)
        data_temp = data_temp.astype('<f4')
        data[str(i)] = data_temp
    return param, data, 0


if __name__ == "__main__":
    d2d = Data2D()
    d2d.load('../test/A150114.101316-01257.sxm')
    d2d.print_param()
    panel = d2d.get_data()
    print panel.shape
    print panel.keys()
    print panel['1'].values
    d = panel['1'].values
    print d.shape
    d2 = panel['1'].dropna()
    print d2.shape

