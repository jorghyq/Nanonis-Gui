# -*- coding: utf-8 -*-

# This file is to load the .dat data from the nanonis software into a python object

from __future__ import division
from struct import unpack
import datetime
import numpy as np
#from pylab import *
import os.path
import re

DEBUG = False


class NanonisDat(object):
	
	def __init__(self, filename):
		self.measurements = []
		self.data = []
		self.header = {}
		self.nameofdata = []
		self.header['filename'] = filename
		self.skip = 1
		self.open()
	
	def open(self):
		self.file = open(os.path.normpath(self.header['filename']), 'r')
		# determine the type of the spectroscopy
		s1 = self.file.readline().strip()
		if s1.split("\t")[0] == 'Experiment':
			self.header['type'] = s1.split("\t")[1]
		else:
			print 'Not a correct type!'
		# read the header
		skip = 1
		while True:
			self.skip = self.skip + 1
			line  = self.file.readline().strip()
			items = line.split("\t")
			# if this line is not a void line
			if len(items) == 2:
				self.header[items[0]] = items[1]
			elif items[0] == '[DATA]':
				break
			else:
				pass
			
		# read the data
		line = self.file.readline()
		self.skip = self.skip + 1
		# read the data name
		self.nameofdata = line.strip().split("\t")
		# read the data
		#self.data = np.loadtxt(self.header['filename'],skiprows=skip)
		
		
				
	def loadDate(self):
		self.data = np.loadtxt(self.header['filename'],skiprows=self.skip)
		

if __name__ == "__main__":
	b = NanonisDat("Follow Me_Bias Spectroscopy238.dat")
	b.loadDate()
	print b.header
	print b.data
	print b.data.shape
