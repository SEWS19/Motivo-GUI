# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QDialog, QMessageBox
from getUiFromFile import getUiFromFile
from definitions import UI_DIR
from PySide2.QtWidgets import QFileDialog
from MotivoParameters import MotivoParameters
from MotivoAccess import MotivoAccess
import os

class ConvertTxtToBinaryDialog(QDialog):
    def __init__(self, parent = None):
        super(ConvertTxtToBinaryDialog, self).__init__(parent)

        self.convertTxtToBinaryDialog = getUiFromFile(os.path.join(UI_DIR,"converttxttobinarydialog.ui"))

        self.fileDialog = QFileDialog()
        self.convertTxtToBinaryParameters = MotivoParameters()
        self.motivoAccess = MotivoAccess()
        self.errorMessage = QMessageBox()

        self.convertTxtToBinaryDialog.convertButton.clicked.connect(self.runConvert)
        self.convertTxtToBinaryDialog.inputFileLineEdit.textChanged.connect(self.updateConvertButton)
        self.convertTxtToBinaryDialog.selectInputFileButton.clicked.connect(self.selectInputFile)

        self.convertTxtToBinaryDialog.arcRadioButton.toggled.connect(self.updateFormatDescription)
        self.convertTxtToBinaryDialog.nodeRadioButton.toggled.connect(self.updateFormatDescription)
        self.convertTxtToBinaryDialog.nodeDegreeRadioButton.toggled.connect(self.updateFormatDescription)

        self.motivoAccess.graphProcess.finished.connect(self.updateConvertButton)
        self.motivoAccess.graphProcess.finished.connect(self.checkForError)
        self.motivoAccess.graphProcess.errorOccurred.connect(self.checkForError)



    def show(self):
        self.convertTxtToBinaryDialog.show()

    def setGraphFile(self, filePathAndName):
        self.convertTxtToBinaryDialog.inputFileLineEdit.setText(filePathAndName)

    def readConvertParameters(self):
        self.convertTxtToBinaryParameters.clear()

        paramValue = self.convertTxtToBinaryDialog.inputFileLineEdit.text()
        self.convertTxtToBinaryParameters.setValueParameter('--input', paramValue)

        paramValue = paramValue[:paramValue.rfind('.')]
        self.convertTxtToBinaryParameters.setValueParameter('--output', paramValue)

        if self.convertTxtToBinaryDialog.arcRadioButton.isChecked():
            self.convertTxtToBinaryParameters.setValueParameter('--format', 'ARC')
        elif self.convertTxtToBinaryDialog.nodeRadioButton.isChecked():
            self.convertTxtToBinaryParameters.setValueParameter('--format', 'NODE')
        elif self.convertTxtToBinaryDialog.nodeDegreeRadioButton.isChecked():
            self.convertTxtToBinaryParameters.setValueParameter('--format', 'NODE_DEGREE')

    def runConvert(self):

        self.readConvertParameters()
        self.convertTxtToBinaryDialog.convertButton.setEnabled(False)
        self.motivoAccess.runConvertTxtToBinary(self.convertTxtToBinaryParameters.getAsArguments())

    def selectInputFile(self):
        filePathAndName = self.fileDialog.getOpenFileName()[0]

        if filePathAndName[filePathAndName.rfind('.'):] == '.txt':
            self.convertTxtToBinaryDialog.inputFileLineEdit.setText(filePathAndName)
        else:
            self.errorMessage.critical(self.convertTxtToBinaryDialog, "motivo-graph", "File extension should be .txt")

    def checkRequiredParameters(self):
        completeInput = True

        if self.convertTxtToBinaryDialog.inputFileLineEdit.text().strip() == '':
            self.convertTxtToBinaryDialog.inputFileLineEdit.setStyleSheet("border: 1px ridge red;")
            completeInput = False
        else:
            self.convertTxtToBinaryDialog.inputFileLineEdit.setStyleSheet("")

        return completeInput

    def updateConvertButton(self):
        self.convertTxtToBinaryDialog.convertButton.setEnabled(self.checkRequiredParameters())

    def updateFormatDescription(self):
        if self.convertTxtToBinaryDialog.arcRadioButton.isChecked():
            self.convertTxtToBinaryDialog.graphFormatDescriptionLabel.setText('One arc per line')
        elif self.convertTxtToBinaryDialog.nodeRadioButton.isChecked():
            self.convertTxtToBinaryDialog.graphFormatDescriptionLabel.setText('One node and its neighbors per line)')
        elif self.convertTxtToBinaryDialog.nodeDegreeRadioButton.isChecked():
            self.convertTxtToBinaryDialog.graphFormatDescriptionLabel.setText('The i-th line contains the degree of node i by its neighbors')

    def displayError(self, errorText):
        print(errorText)
        self.errorMessage.critical(self.convertTxtToBinaryDialog, "motivo-graph", errorText)


    def checkForError(self):
        errorText = str(self.motivoAccess.graphProcess.readAllStandardError())
        errorText = errorText[2:]
        errorText = errorText[:-3]

        if errorText != "b''" and errorText != '':
            self.displayError(errorText)
        else:
            self.convertTxtToBinaryDialog.close()
