# functions that are useful
from nanonisfile import NanonisFile
import numpy as np


def extract_data(full_path,channel):
    """ extract specified channel from the raw data """
    data = NanonisFile(full_path)
    return data.data[channel].data

def process_img(data, process_id):
    if process_id == 0:
        pass
    # subtract mean
    elif process_id == 1:
        row_mean = np.mean(data,axis=0)
        data = (data - row_mean)
    # subtract slope
    elif process_id == 2:
        #print data.shape
        data_temp = data
        n = data_temp.shape[0]
        m = data_temp.shape[1]
        #print n, m
        xi = np.arange(n)
        x= np.array([xi,np.ones(n)]).T
        w = np.linalg.lstsq(x,data_temp)[0]
        X = np.array([xi,]*int(m)).T
        Y = (X*w[0])
        data = data - Y
        #print data.shape
    # subtract linear fit
    elif process_id == 3:
        data_temp = data
        n = data_temp.shape[0]
        m = data_temp.shape[1]
        xi = np.arange(n)
        x= np.array([xi,np.ones(n)]).T
        w = np.linalg.lstsq(x,data_temp)[0]
        X = np.array([xi,]*int(m)).T
        Y = (X*w[0] + w[1])
        data = data - Y
    elif process_id == 4:
        pass
    else:
        pass
    return data


if __name__ == "__main__":
    data = np.zeros((100,100))
    data_out = process_img(data,1)
