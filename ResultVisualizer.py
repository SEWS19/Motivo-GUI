from Delegate import ImageDelegate
from Model import CsvTableModel
import csv
from motivo_utils import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
import math
from ImageProvider import ImageProvider

class ResultVisualizer:
    def __init__(self,svgCache,data,headers,motifWidget,barWidget):
        super().__init__()
        '''
        input : csvFileName eg "/home/output.csv"
                motifWidget : QWidget
                barWidget   : QWidget 
        '''
        #Class Variables
        self._data = data;
        self._headers = headers; 
        self.motifWidget = motifWidget;
        self.barWidget = barWidget;
        #Initialize cache 
        self.svgCache = svgCache; 

        #Model 
        self._model = CsvTableModel(self._data,self._headers)
        #Delegate

        self._delegate =  ImageDelegate(self.svgCache,self.motifWidget)

    def visualizeMotif(self):
        self.motifWidget.setItemDelegateForColumn(1,self._delegate)
        self.motifWidget.setModel(self._model)
        header=self.motifWidget.horizontalHeader()
        header.setStretchLastSection(True)
        self.motifWidget.resizeColumnsToContents()
        self.motifWidget.setColumnWidth(0,200)
        self.motifWidget.setColumnWidth(1,500)
        self.motifWidget.resizeRowsToContents()
        self.motifWidget.hideColumn(5)
        self.motifWidget.hideColumn(7)
        self.motifWidget.hideColumn(8)
        self.motifWidget.setShowGrid(False)
        #self.motifWidget.resizeColumnsToContents()

    def visualizeChart(self):
        motifName= list()
        motifFrequency = list()

        for i, motifs in enumerate(self._data):
            if i >= 25:
                break
            motifName.append(motifs[0])
            proportion = format(float(motifs[2]),'.5f')
            motifFrequency.append(proportion)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)        
        self.barWidget.addWidget(self.canvas)
        

        plt.barh(motifName, motifFrequency)

        plt.xlabel('Frequencies (Log)')
        plt.ylabel('Motif')
        plt.title('Frequency Plot (First 25)')

        plt.savefig('./report/plot.svg')

        self.canvas.draw_idle()
