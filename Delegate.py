
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
class ImageDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self,imageCache, parent):
        self.imageCache = imageCache
        QtWidgets.QStyledItemDelegate.__init__(self, parent)
    def paint(self, painter, option, index):        
        painter.save()
        if index.column()==1:
            motifPath = self.imageCache[index.data()]
            icon=QtGui.QIcon(motifPath)
            icon.paint(painter, option.rect)
        painter.restore()
    def sizeHint(self, option, index):
        super().sizeHint(option, index)
        return QtCore.QSize(300, 300)
  
  
