# This file pre parses the file and extract the important information
############################################
# file_type:    0     others               #
#               1     txt                  #
#               2     sxm                  #
#               3     dat                  #
#               4     3ds                  #
############################################
# file_format:  0     STM                  #
#               1     AFM                  #
#               2     dI/dV map            #
#               3     dI/dV                #
#               4     Force curve          #
############################################


import numpy as np
import os
import sys
import csv
import pandas as pd
#from nanonisdatfile import NanonisDat
#from nanonisfile import NanonisFile
sys.path.insert(1,'../nbrowser/')
from Data2D import Data2D

class Controller():
    # manage all the files

    def __init__(self,list_path):
       self.parser = Data2D()
       self.columns = self.parser.columns
       print self.columns
       self.count = 0
       self.list_path = list_path

    def init_table(self,dir_pre=None):
        # initialize with
        self.table = pd.DataFrame(columns=self.columns)
        with open(self.list_path,'r') as f:
            lines = f.readlines()
        for line in lines:
            if line[-1] == '\n':
                line = line[:-2]
            #print line
            if line[-3:] == 'sxm':
                self.parser.load(dir_pre+line)
                #print dir_pre+line
                #print self.parser.get_param()
                #print dir_pre+line
                #self.parser.parsing()
                #self.parser.output_to_csv()
                #print self.parser.param['filename'],self.parser.param['filetype']
                if self.parser.LOADED == 0:
                    if (self.parser.get_param())['ftype'] == 2:
                        #print dir_pre+line
                        self.table.loc[self.count] = self.parser.output_to_csv()
                        print self.parser.output_to_csv()
                        print "saved to entry %d", self.count
                        self.count = self.count + 1

    def load_table(self):
        pass

    def update_entry(self,row,column):
        pass

    def update_row(self,row):
        pass

    def write_table(self):
        pass



if __name__ == "__main__":
    fdir = '/home/jorghyq/Data/201501/'
    files = os.listdir(fdir)
    #parser = FileParser()
    #for item in files:
        #print item
        #parser.load_file(fdir+item)
        #parser.parsing()
        #parser.print_results()
        #parser.output_to_csv()
    cl = Controller('../scripts/file_names.txt')
    cl.init_table('/home/jorghyq/Data/')
    #print cl.table
    cl.table.to_csv('test.csv')
