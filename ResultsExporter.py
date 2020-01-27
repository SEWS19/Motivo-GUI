import csv
from motivo_utils import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
import math
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas 
from reportlab.graphics import renderPDF 
from svglib.svglib import svg2rlg 
from graphviz import Graph
from motivo_utils import *
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from PySide2.QtCore import QObject, QThread, Signal, Slot
from time import sleep

class ResultsExporter(QObject):

    progress = Signal(float)
    finished = Signal(int)

    def __init__(self,svgCache):
        super().__init__()

        #Class Variables

        self._data = list()
        self.pdfFile = None

        self.svgCache = svgCache


    @Slot(str, str)
    def setData(self, csvFilePath, pdfOutputName):
        try:
            with open(csvFilePath) as fh:
                csvreader = csv.reader(fh)
                headers = next(csvreader)
                data = list(csvreader)
        except FileNotFoundError:
            print("Results file not found")
            #Item Delegate

        self._data = data

        self.pdfOutputName = pdfOutputName
        self.saveAsPDF()

    def saveAsPDF(self):
        self.pdfFile = SimpleDocTemplate(self.pdfOutputName, rightMargin=0, leftMargin=6.5 , topMargin=0.3 , bottomMargin=0)

        self.exportMotifs()

    def exportMotifs(self):
        # Iterate through each motif 
        num_cols = 2 
        row_iterator =0;

        styles = getSampleStyleSheet()
        titleStyle = styles['Title']
        titleStyle.alignment = 2
        titleStyle.fontSize = 20
        title = Paragraph("Graphlets", titleStyle)
        tableData = [[title]]
   
        listStyle = TableStyle([('BACKGROUND',(1,1),(-2,-2),colors.green),('TEXTCOLOR',(0,0),(1,-1),colors.black)])
        numberOfRows = len(self._data) 
        # iterate over results in multiples of two 
        for index in range(0,numberOfRows-1,2):
            # Two motifs per row
            # Input first motif
            firstMotifFilename = self.svgCache[str(self._data[index][0])]
            factor=.2
            sx = sy = factor
            drawing1 = svg2rlg(firstMotifFilename)
            drawing1.width, drawing1.height = drawing1.minWidth() * sx, drawing1.height * sy
            drawing1.scale(sx, sy)

            
            # Input Last motif
            secondMotifFilename = self.svgCache[str(self._data[index+1][0])]
            drawing2 = svg2rlg(secondMotifFilename)
            drawing2.width, drawing2.height = drawing2.minWidth() * sx, drawing2.height * sy
            drawing2.scale(sx, sy)
            
            # Append the data
            tableData.append(["",""])
            tableData.append([self._data[index][0],self._data[index+1][0]])
            
            tableData.append([drawing1,drawing2])
            tableData.append([self._data[index][1],self._data[index+1][1]])
            tableData.append(["",""])

            self.progress.emit(index / numberOfRows * 100)

            if QThread.currentThread().isInterruptionRequested():
                return
        
        # For the last row if add the last row
        if(numberOfRows % 2 != 0 ):
            lastElementIndex = numberOfRows -1;
            lastmotifRow = self.svgCache[str(self._data[lastElementIndex][0])]
            drawing1 = svg2rlg(lastmotifRow)
            factor=.2
            sx = sy = factor
            drawing1.width, drawing1.height = drawing1.minWidth() * sx, drawing1.height * sy
            drawing1.scale(sx, sy)
            tableData.append(["",""])
            tableData.append([self._data[lastElementIndex][0],""])
            tableData.append([drawing1,""])
            tableData.append([self._data[lastElementIndex][1],""])
            tableData.append(["",""])

        elements=[]
        t=Table(tableData)
        listStyle.add("ALIGN",(0,0),(-1,-1),"CENTER")
        listStyle.add("VALIGN",(0,0),(-1,-1),"MIDDLE")
        listStyle.add("",(0,0),(-1,-1),"MIDDLE")
        #listStyle.add("BACKGROUND",(0,0),(-1,-1),colors.red)
        t.setStyle(listStyle.getCommands())
        elements.append(t)
        elements.append(svg2rlg("./report/plot.svg"))
            # write the to disk
        self.pdfFile.build(elements)

        self.finished.emit(True)
