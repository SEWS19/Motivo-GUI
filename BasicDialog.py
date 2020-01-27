# This Python file uses the following encoding: utf-8

from PySide2.QtWidgets import QDialog, QMessageBox
from PySide2.QtCore import Signal, QProcess
from getUiFromFile import getUiFromFile
from definitions import UI_DIR
from PySide2.QtWidgets import QFileDialog
from MotivoParameters import MotivoParameters
from MotivoAccess import MotivoAccess
from ConvertTxtToBinaryDialog import ConvertTxtToBinaryDialog
import os, signal

class BasicDialog(QDialog):
    outputReady = Signal(int)

    def __init__(self, parent = None):
        super(BasicDialog, self).__init__(parent)

        self.basicDialog = getUiFromFile(os.path.join(UI_DIR,"basicdialog.ui"))

        self.fileDialog = QFileDialog()

        self.errorMessage = QMessageBox()

        self.motivoParameters = MotivoParameters()
        self.motivoAccess = MotivoAccess()
        self.outputFile = ''

        self.cancelled = False

        self.convertTxtToBinaryDialog = ConvertTxtToBinaryDialog()

        # init

        self.showRunMotivoButton()

        # connect

        self.basicDialog.runMotivoButton.clicked.connect(self.runMotivo)

        self.basicDialog.selectInputFileButton.clicked.connect(self.selectInputFileBrowser)
        self.basicDialog.selectOutputFileButton.clicked.connect(self.selectOutputFileBrowser)

        self.basicDialog.inputFileLineEdit.textChanged.connect(self.updateRunMotivoButton)
        self.basicDialog.outputFileLineEdit.textChanged.connect(self.updateRunMotivoButton)

        self.basicDialog.compressThresholdCheckBox.toggled.connect(self.basicDialog.compressThresholdSpinBox.setEnabled)

        self.motivoAccess.motivoProcess.readyReadStandardOutput.connect(self.updateProgressBar)
        self.motivoAccess.motivoProcess.finished.connect(self.completeProcess)

        self.basicDialog.cancelButton.clicked.connect(self.cancelProcess)

    def show(self):
        self.updateRunMotivoButton()
        self.basicDialog.show()

    def readParametersFromBasicDialog(self):
        # set VALUE parameters

        # TODO: replace ' ' with '\ ' in dirs and filenames
        # set input file
        paramValue = self.basicDialog.inputFileLineEdit.text()
        self.motivoParameters.setValueParameter('--graph', paramValue)

        # set output file

        paramValue = self.basicDialog.outputFileLineEdit.text()
        self.motivoParameters.setValueParameter('--output', paramValue)
        self.outputFile = paramValue

        # TODO: disable space character input
        # set Graphlet Size
        paramValue = self.basicDialog.graphletSizeSpinBox.text()
        self.motivoParameters.setValueParameter('-k', paramValue)

        # set Number of Samples
        paramValue = self.basicDialog.numberOfSamplesSpinBox.text()
        self.motivoParameters.setValueParameter('--samples', paramValue)

        # set compress threshold

        if self.basicDialog.compressThresholdCheckBox.isChecked():
            paramValue = self.basicDialog.compressThresholdSpinBox.text()
            self.motivoParameters.setValueParameter('--compress', paramValue)

        # set threads
        paramValue = self.basicDialog.threadsSpinBox.text()
        self.motivoParameters.setValueParameter('--threads', paramValue)

        # set FLAG parameters

        # set Adaptive
        if self.basicDialog.adaptiveCheckBox.checkState() == True:
            self.motivoParameters.setFlagParameter(paramName = '--adaptive')

        # set Smart Stars
        if self.basicDialog.computeStarsCheckBox.checkState() == True:
            self.motivoParameters.setFlagParameter(paramName = '--smart-stars')

        #print(self.motivoParameters.getAsArguments())
    

    def updateProgressBar(self,updateStep=2):
        progress = min(self.basicDialog.basicProgressBar.value() + updateStep, 90)
        self.basicDialog.basicProgressBar.setValue(progress)

    def completeProcess(self):

        self.basicDialog.runMotivoButton.setEnabled(True)

        self.showRunMotivoButton()

        if self.cancelled:
            self.basicDialog.basicProgressBar.setValue(0)
            self.cancelled = False
        else:
            self.basicDialog.basicProgressBar.setValue(100)
            self.outputReady.emit(1)

    def updateRunMotivoButton(self):
        self.basicDialog.runMotivoButton.setEnabled(self.checkRequiredInputs())

    def runMotivo(self):
        # Disble the run button  TODO

        self.basicDialog.runMotivoButton.setEnabled(False)
        self.readParametersFromBasicDialog()
        self.basicDialog.basicProgressBar.setValue(0)

        self.motivoAccess.runMotivo(self.motivoParameters.getAsArguments())

        self.showCancelButton()


    def getOutputFile(self):
        return self.outputFile

    def selectInputFileBrowser(self):

        filePathAndName = self.fileDialog.getOpenFileName()[0]

        if filePathAndName[filePathAndName.rfind('.'):] == '.txt':
            self.openConvertTxtToBinaryDialog(filePathAndName)
            filePathAndName = ''
        elif filePathAndName[filePathAndName.rfind('.'):] == '.ged' or filePathAndName[filePathAndName.rfind('.'):] == '.gof':
            filePathAndName = filePathAndName[:filePathAndName.rfind('.')]
        else:
            self.errorMessage.critical(self.basicDialog, 'Incorrect file format', 'Incorrect input graph file format')
            filePathAndName = ''


        self.basicDialog.inputFileLineEdit.setText(filePathAndName)

    def selectOutputFileBrowser(self):

        filePathAndName = self.fileDialog.getExistingDirectory()
        if filePathAndName != '':
            filePathAndName += '/' + 'output'

        self.basicDialog.outputFileLineEdit.setText(filePathAndName)


    def checkRequiredInputs(self):
        completeInput = True

        if self.basicDialog.inputFileLineEdit.text().strip() == '':
            self.basicDialog.inputFileLineEdit.setStyleSheet("border: 1px ridge red;")
            completeInput = False
        else:
            self.basicDialog.inputFileLineEdit.setStyleSheet("")

        if self.basicDialog.outputFileLineEdit.text().strip() == '':
            self.basicDialog.outputFileLineEdit.setStyleSheet("border: 1px ridge red;")
            completeInput = False
        else:
            self.basicDialog.outputFileLineEdit.setStyleSheet("")

        return completeInput

    def openConvertTxtToBinaryDialog(self, filePathAndName):
        self.convertTxtToBinaryDialog.setGraphFile(filePathAndName)
        self.convertTxtToBinaryDialog.show()


    def showCancelButton(self):
        self.basicDialog.runMotivoButton.hide()

        self.basicDialog.cancelButton.show()


    def showRunMotivoButton(self):
        self.basicDialog.cancelButton.hide()

        self.basicDialog.runMotivoButton.show()

    def cancelProcess(self):
        self.cancelled = True
        self.motivoAccess.motivoProcess.kill()
        self.showRunMotivoButton()
