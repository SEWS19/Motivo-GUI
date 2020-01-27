import os
import csv
from PySide2.QtCore import QObject, Signal, Slot, QThread
from PySide2.QtWidgets import QTableView,QMainWindow, QMenuBar, QMessageBox
from PySide2.QtWidgets import QFileDialog
from BasicDialog import BasicDialog
from AdvancedDialog import AdvancedDialog
from getUiFromFile import getUiFromFile
from MotivoParameters import MotivoParameters
from MotivoAccess import MotivoAccess
from definitions import ROOT_DIR
from UserPreferencesDialog import UserPreferencesDialog
from ResultVisualizer import ResultVisualizer
from ResultsExporter import ResultsExporter
from ImageProvider import ImageProvider


class MotivoGUI():
    def __init__(self):
        self.mainWindow = MainWindow()

    def show(self):
        self.mainWindow.show()
        self.mainWindow.checkMotivoDirectory()

class MainWindow(QMainWindow):

    writeToPDFSignal = Signal(str, str)

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.mainWindow = getUiFromFile(os.path.join(ROOT_DIR,"UI/mainwindow.ui"))
        self.setCentralWidget(self.mainWindow)


        # Visualization Part
        # accessing Motivo

        self.fileDialog = QFileDialog()

        self.userPreferencesDialog = UserPreferencesDialog()
        self.svgCache = ImageProvider(100)

        self.errorMessage = QMessageBox()

        self.csvFilePath = None

        self.writeToPDFThread = QThread(self)
        self.writeToPDF = ResultsExporter(self.svgCache)
        self.writeToPDF.moveToThread(self.writeToPDFThread)
        # TO DO: Creating a queue for motivo sessions

        # hide Layout

        self.mainWindow.writeToPdfProgressBar.hide()
        self.mainWindow.cancelWritingToPDFButton.hide()
        self.mainWindow.writeToPdfLabel.hide()

        # Creating the dialogs for menu bar actions

        self.basicDialog = BasicDialog()
        self.advancedDialog = AdvancedDialog()

        # Creating connections between menu bar actions and dialogs

        # File

        self.mainWindow.actionExit.triggered.connect(self.exit)

        # Motivo

        self.mainWindow.actionBasic.triggered.connect(self.openBasicDialog)
        self.mainWindow.actionAdvanced.triggered.connect(self.openAdvancedDialog)
        self.mainWindow.actionSaveAsPDF.triggered.connect(self.startWriteToPDFThread)
        self.mainWindow.actionOpenCSV.triggered.connect(self.openSelectCsv)

        self.writeToPDFSignal.connect(self.writeToPDF.setData)

        # Options
        self.mainWindow.actionUserPreferences.triggered.connect(self.openUserPreferencesDialog)

        # visualization

        self.basicDialog.outputReady.connect(self.visualizeFromBasicDialog)
        self.advancedDialog.outputReady.connect(self.visualizeFromAdvancedDialog)

        self.writeToPDF.progress.connect(self.updateWriteToPDFProgress)
        self.writeToPDF.finished.connect(self.writeToPdfComplete)
        self.mainWindow.cancelWritingToPDFButton.clicked.connect(self.cancelWritingToPDF)


    # functions called through menuBar actions

    def exit(self):
        self.close()

    def openBasicDialog(self):
        self.basicDialog.show()

    def openAdvancedDialog(self):
        self.advancedDialog.show()

    def openUserPreferencesDialog(self):
        self.userPreferencesDialog.show()

    def checkMotivoDirectory(self):
        if MotivoAccess.motivoDirectory == '':
            motivoDirError = QMessageBox()
            motivoDirError.critical(self.mainWindow, "motivo", "Motivo directory not found, please set the directory in User Preferences")

    def openSelectCsv(self):
        filePathAndName = self.fileDialog.getOpenFileName()[0]

        if filePathAndName[filePathAndName.rfind('.'):] == '.csv':
            self.csvFilePath = filePathAndName
            self.visualizeFromOpenCSV()
        elif filePathAndName != '':
            self.errorMessage.critical(self.mainWindow, "Visualize from a csv file", "Incorrect file format")

    def visualizeFromOpenCSV(self):
        self.updateMainGraphletWidget(self.csvFilePath)

    def visualizeFromBasicDialog(self):
        self.csvFilePath = self.basicDialog.getOutputFile() + '.csv'
        self.updateMainGraphletWidget(self.csvFilePath)

    def visualizeFromAdvancedDialog(self):
        self.csvFilePath = self.advancedDialog.getOutputFile() + '.csv'
        self.updateMainGraphletWidget(self.csvFilePath)


    def updateMainGraphletWidget(self,outputCsvFilePath):
        # Reset the widgets
        self.mainWindow.resultsView.clearSpans() 
        for i in reversed(range(self.mainWindow.plotLayout.count())): 
            self.mainWindow.plotLayout.itemAt(i).widget().setParent(None)
        try:  
            with open(outputCsvFilePath) as fh:
                csvreader = csv.reader(fh)
                headers = next(csvreader)
                headers.insert(1,"Graph")
                data = list(csvreader)
        except FileNotFoundError:
            print("Results file not found")
        results = ResultVisualizer(self.svgCache,data,headers,self.mainWindow.resultsView,self.mainWindow.plotLayout)
        results.visualizeMotif()
        results.visualizeChart()

    def startWriteToPDFThread(self):

        if self.csvFilePath == None:
            self.errorMessage.about(self.mainWindow, 'Save As PDF', 'Nothing to save')
            return

        pdfFileName = self.fileDialog.getSaveFileName()[0]

        if pdfFileName == '':
            return

        #self.writeToPDFThread.setTerminationEnabled(True)

        self.writeToPDFThread.start()

        self.mainWindow.writeToPdfProgressBar.setValue(0)
        self.showWriteToPdfProgressBar()

        self.writeToPDFSignal.emit(self.csvFilePath, pdfFileName)

    def updateWriteToPDFProgress(self, progress):
        self.mainWindow.writeToPdfProgressBar.setValue(progress)

    def writeToPdfComplete(self):
        self.mainWindow.writeToPdfProgressBar.setValue(100)

        self.hideWriteToPdfProgressBar()

        self.writeToPDFThread.quit()

    def showWriteToPdfProgressBar(self):
        self.mainWindow.writeToPdfProgressBar.show()
        self.mainWindow.cancelWritingToPDFButton.show()
        self.mainWindow.writeToPdfLabel.show()

    def hideWriteToPdfProgressBar(self):
        self.mainWindow.writeToPdfProgressBar.hide()
        self.mainWindow.cancelWritingToPDFButton.hide()
        self.mainWindow.writeToPdfLabel.hide()

    def cancelWritingToPDF(self):
        self.hideWriteToPdfProgressBar()
        self.writeToPDFThread.requestInterruption()
        self.writeToPDFThread.quit()
