from PySide2 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import networkx as nx

import sys
import csv

from graphviz import Graph

from motivo_utils import *

"""
Create a Model and  Loaded about 100 svg graph in memory 
Dynammically create and load it

"""

class CsvTableModel(QtCore.QAbstractTableModel):
    """The model for a CSV table."""

    def __init__(self, data,headers):
        super().__init__()
        self._data=data
        self._headers=headers;


    # Minimum necessary methods:
    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return len(self._headers)
    
    def data(self, index, role):
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            if(index.row() <= self.rowCount(self) and index.column()< self.columnCount(self)):
                if(index.column() < 2):
                        return self._data[index.row()][0]
                return self._data[index.row()][index.column()-1]
 
        # Additional features methods:
    def headerData(self, section, orientation, role):
        if orientation==QtCore.Qt.Vertical:
            if role==QtCore.Qt.DecorationRole:
                return ""
            if role==QtCore.Qt.DisplayRole:
                 return ""
        if role==QtCore.Qt.DisplayRole and orientation==QtCore.Qt.Horizontal:
            return self._headers[section]
           #return self.header_labels[section]
        return super().headerData(section, orientation, role)

