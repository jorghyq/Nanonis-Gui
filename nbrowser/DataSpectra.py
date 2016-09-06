# Class to handle the data needed for the GUI program
# Author:jorghyq
import pandas as pd


class DataSpectra:
    # Holding the generalized data for every data type

    def __init__(self):
        self.full_path = None
        self.__param = {}
        self.__data = None # Will be pandas Panel

    def load(self,path):
        self.full_path = path


    def get_param(self):
        return self.__param

    def get_data(self):
        return self.__data
