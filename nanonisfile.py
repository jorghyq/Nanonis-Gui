# -*- coding: utf-8 -*-

"""
    Copyright © 2011 François Bianco, University of Geneva - francois.bianco@unige.ch

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    \section Updates

    2013-05 fbianco:
        first version, from nanonis documentation and some example files
        only tested on Nanonis V2 files, but implements V1 file form
        the documentation.
"""


from __future__ import division
from struct import unpack
import datetime
#from pylab import *
import numpy as np
import os.path
import re

DEBUG = False


class Error(Exception):
    """Base class for exceptions in this module. """
    pass

class UnhandledFileError(Error):
    """Occurs if the file has an unknown structure."""
    pass

class ParameterTypeError(Error):
    """Occurs if a parameter has an unknown type."""
    pass

class UnhandledDataType(Error):
    """Occurs if the file has an unknown data structure."""
    pass

class DataArray():
    """A simple class holding the minimal structure for storing STM data.
       The data is a numpy array with the right shape according to the type of
       data (i.e a vector for curve, a matrix for images, a 3d matrix for maps.)
       Info is a python dictionary to store physical information on the data.
    """
    def __init__(self, data, info):
        self.data = data # is a nupmy matrix
        self.info = info.copy() # a simple dictionary

class NanonisFile(object):
    """Parser for Nanonis SXM file to a Python object"""

    def __init__(self, filename):
        """ \arg filename should be a valid path to a nanonis SXM file."""

        self.measurements = []
        self.data = []
        self.header = {}
        self.header['filename'] = filename

        self.open()

    def open(self):
        """ Parse a Nanonis file and create the data array with physical meaning
            based on the file structure stored in the file header.
        """

        # Open file in binary format. The header is stored in ascii format,
        # and data in 4 bytes big endian floats all in the same file.
        self.file = open(os.path.normpath(self.header['filename']), 'rb')

        # Check if file is a nanonis file
        s1 = self.file.readline()
        if not re.match(':NANONIS_VERSION:', s1):
            raise UnhandledFileError, \
                "The file %s does not have the Nanonis SXM" % \
                    self.header['filename']
            return

        self.header['version'] = int(self.file.readline())

        # Read header lines until the tag 'SCANIT_END' is found
        while True:
            line = self.file.readline().strip()

            if re.match('^:.*:$', line): # Tag are words between colons
                tagname = line[1:-1] # remove colons
                if DEBUG:
                    print 'New tag %s' % tagname
            else: # it's not a tag, we are reading a value for the previous tag
                if 'Z-CONTROLLER' == tagname:
                    # This is a tab separated table on two line
                    # first line is the tag and second value
                    keys = line.split('\t')
                    values = self.file.readline().strip().split('\t')
                    self.header['z-controller'] = dict(zip(keys, values))
                elif tagname in ('BIAS', 'REC_TEMP', 'ACQ_TIME', 'SCAN_ANGLE'):
                    self.header[tagname.lower()] = float(line)
                elif tagname in ('SCAN_PIXELS', 'SCAN_TIME', 'SCAN_RANGE', 'SCAN_OFFSET'):
                    self.header[tagname.lower()] = [ float(i) for i in re.split('\s+', line) ] # two numerical value separated by any amount of spaces
                elif 'DATA_INFO' == tagname:
                    # This is a tab separated table on two line
                    # first line is the tag and next store the values
                    # an empty line separate the values from the next tag.
                    if 1 == self.header['version']:
                        keys = re.split('\s\s+',line)
                        # FIXME I have no V1 file to test that, I expect
                        # from the rest of the files that there are min 2
                        # spaces to separate values.
                    else: # from V2 tab separated
                        keys = line.split('\t')
                    self.header['data_info'] = []

                    while True:
                        line = self.file.readline().strip()
                         # one empty line separate data from the next tag
                        if not line:
                            break
                        values = line.strip().split('\t')
                        self.header['data_info'].append(dict(zip(keys, values)))
                elif tagname in ('SCANIT_TYPE','REC_DATE', 'REC_TIME', 'SCAN_FILE', 'SCAN_DIR'):
                    self.header[tagname.lower()] = line
                elif 'SCANIT_END' == tagname:
                    break # end of header
                else:  # treat unknown tag content as string
                       # they could be multiline, like comments
                    if not self.header.has_key(tagname.lower()): # 1st create
                        self.header[tagname.lower()] = line
                    else: # then appends all the next lines
                        self.header[tagname.lower()] += '\n' + line

        # Fix a bug of V1 format
        if 1 == self.header['version']:
            # In version 1 line and pixel were inverted
            self.header['scan_pixels'].reverse()

        # read until 1A 04 (hex) is found, = beginning of binary data
        s = '\x00\x00'
        while '\x1A\x04' != s:
            s = s[1] + self.file.read(1)

        size = int( self.header['scan_pixels'][0] * \
                    self.header['scan_pixels'][1] * 4) # 4 Bytes/px

        nchannels = len(self.header['data_info'])
        supp = 0
        for n in range(nchannels): # add 1 per "both"/mirrored directions
            supp += ('both' == self.header['data_info'][n]['Direction'])
        nchannels+=supp

        for i in range(nchannels):
			data_buffer = self.file.read(size)
			self.header['channel'] = i
			self.data.append( DataArray(np.ndarray(shape=self.header['scan_pixels'],dtype='>f',buffer=data_buffer),self.header))
        for i in range(len(self.data)):
			if i%2 == 1:
				self.data[i].data = np.fliplr(self.data[i].data)
		
        if self.header['scan_dir'] == "down":
			for i in range(len(self.data)):
				self.data[i].data = np.flipud(self.data[i].data)

			
		
		
		
    def getData(self):
        """Return the read data"""

        return self.data
        
def load(filename):
    """Loader function for further data processing
    Return a list of DataArray object"""

    nf = NanonisFile(filename)
    return nf.getData()

if __name__ == "__main__":
    pass
