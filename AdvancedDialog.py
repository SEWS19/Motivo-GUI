# This Python file uses the following encoding: utf-8

from PySide2.QtWidgets import QDialog, QMessageBox
from PySide2.QtCore import Signal
from getUiFromFile import getUiFromFile
from MotivoParameters import MotivoParameters
from MotivoAccess import MotivoAccess
from definitions import UI_DIR
from PySide2.QtWidgets import QFileDialog
from ConvertTxtToBinaryDialog import ConvertTxtToBinaryDialog
import os

class AdvancedDialog(QDialog):
    outputReady = Signal(int)

    def __init__(self, parent = None):
        super(AdvancedDialog, self).__init__(parent)

        self.advancedDialog = getUiFromFile(os.path.join(UI_DIR,"advanceddialog.ui"))

        self.fileDialog = QFileDialog()
        self.errorMessage = QMessageBox()

        self.motivoAccess = MotivoAccess()

        self.convertTxtToBinaryDialog = ConvertTxtToBinaryDialog()
        # parameters

        self.buildParameters = MotivoParameters()
        self.mergeParameters = MotivoParameters()
        self.sampleParameters = MotivoParameters()

        # init run buttons and required input

        self.updateBuildButton()
        self.updateMergeButton()
        self.updateSampleButton()

        self.sampleCancelled = False
        self.outputFile = ''

        self.showSampleButton()

        # connects

         # build tab

        self.advancedDialog.buildToVertexCheckBox.toggled.connect(self.advancedDialog.buildToVertexSpinBox.setDisabled)

        self.advancedDialog.buildTableSizeSpinBox.valueChanged.connect(self.buildTableSizeImplications)

        self.advancedDialog.buildSelectiveCountCheckBox.toggled.connect(self.advancedDialog.buildTreeletsFileLineEdit.setEnabled)
        self.advancedDialog.buildSelectiveCountCheckBox.toggled.connect(self.advancedDialog.buildSelectTreeletsFileButton.setEnabled)

         # merge tab

        self.advancedDialog.mergeCompressThresholdCheckBox.toggled.connect(self.advancedDialog.mergeCompressThresholdSpinBox.setEnabled)

         # sample tab

        self.advancedDialog.sampleNumberOfSamplesCheckBox.toggled.connect(self.advancedDialog.sampleNumberOfSamplesSpinBox.setEnabled)
        self.advancedDialog.sampleTimeBudgetCheckBox.toggled.connect(self.advancedDialog.sampleTimeBudgetSpinBox.setEnabled)

        self.advancedDialog.sampleEnableTreeletBufferingCheckBox.toggled.connect(self.advancedDialog.sampleTreeletBufferSizeSpinBox.setEnabled)
        self.advancedDialog.sampleEnableTreeletBufferingCheckBox.toggled.connect(self.advancedDialog.sampleTreeletBufferDegreeSpinBox.setEnabled)

        self.advancedDialog.sampleEnableSelectiveBuildAndSamplingCheckBox.toggled.connect(self.advancedDialog.sampleSelectTreeletsToBuildFileButton.setEnabled)
        self.advancedDialog.sampleEnableSelectiveBuildAndSamplingCheckBox.toggled.connect(self.advancedDialog.sampleSelectTreeletsToBuildFileLineEdit.setEnabled)
        self.advancedDialog.sampleEnableSelectiveBuildAndSamplingCheckBox.toggled.connect(self.advancedDialog.sampleSelectTreeletsToSampleFileButton.setEnabled)
        self.advancedDialog.sampleEnableSelectiveBuildAndSamplingCheckBox.toggled.connect(self.advancedDialog.sampleSelectTreeletsToSampleFileLineEdit.setEnabled)

        self.advancedDialog.sampleSmartStarsCheckBox.toggled.connect(self.sampleSmartStarImplications)
        self.advancedDialog.sampleNumberOfStarsCheckBox.toggled.connect(self.sampleSmartStarImplications)

        self.advancedDialog.sampleGraphletsCheckBox.toggled.connect(self.advancedDialog.sampleVerticesCheckBox.setChecked)

        self.advancedDialog.sampleEstimateOccurencesCheckBox.toggled.connect(self.advancedDialog.sampleGraphletsCheckBox.setChecked)
        self.advancedDialog.sampleEstimateOccurencesCheckBox.toggled.connect(self.advancedDialog.sampleNoSpanningTreesCheckBox.setChecked)
        self.advancedDialog.sampleEstimateOccurencesCheckBox.toggled.connect(self.advancedDialog.sampleGroupCheckBox.setChecked)

        self.advancedDialog.sampleEstimateOccurencesAdaptiveCheckBox.toggled.connect(self.advancedDialog.sampleEstimateOccurencesCheckBox.setChecked)
        self.advancedDialog.sampleEstimateOccurencesAdaptiveCheckBox.toggled.connect(self.advancedDialog.sampleCanonicizeCheckBox.setChecked)

        # file browsing
         # build

        self.advancedDialog.buildSelectInputFileButton.clicked.connect(self.buildSelectInputFile)
        self.advancedDialog.buildSelectOutputFileButton.clicked.connect(self.buildSelectOutputFile)

        self.advancedDialog.buildSelectTreeletsFileButton.clicked.connect(self.buildSelectTreeletsFile)

         # merge

        self.advancedDialog.mergeSelectOutputFileButton.clicked.connect(self.mergeSelectOutputFile)

         # Sample

        self.advancedDialog.sampleSelectInputFileButton.clicked.connect(self.sampleSelectInputFile)
        self.advancedDialog.sampleSelectOutputFileButton.clicked.connect(self.sampleSelectOutputFile)

        self.advancedDialog.sampleSelectTreeletsToBuildFileButton.clicked.connect(self.sampleSelectTreeletsToBuildFile)
        self.advancedDialog.sampleSelectTreeletsToSampleFileButton.clicked.connect(self.sampleSelectTreeletsToSampleFile)

         # run buttons

        self.advancedDialog.buildButton.clicked.connect(self.runBuild)
        self.advancedDialog.mergeButton.clicked.connect(self.runMerge)
        self.advancedDialog.sampleButton.clicked.connect(self.runSample)

         # user input suggestions

        self.motivoAccess.buildProcess.finished.connect(self.suggestAfterBuildInputs)

         # run buttons availability
        self.motivoAccess.buildProcess.finished.connect(self.advancedDialog.buildButton.setEnabled)

         # error display
        self.motivoAccess.buildProcess.finished.connect(self.displayBuildError)

        self.motivoAccess.mergeProcess.finished.connect(self.displayMergeError)

        self.motivoAccess.sampleProcess.finished.connect(self.displaySampleError)

         # build Progress bar

        self.motivoAccess.buildProcess.readyReadStandardOutput.connect(self.updateBuildProgressBar)
        self.motivoAccess.buildProcess.finished.connect(self.completeBuildProcess)

         # merge Progress Bar
        self.motivoAccess.mergeProcess.readyReadStandardOutput.connect(self.updateMergeProgressBar)
        self.motivoAccess.mergeProcess.finished.connect(self.completeMergeProcess)

         # sample Progress Bar
        self.motivoAccess.sampleProcess.readyReadStandardOutput.connect(self.updateSampleProgressBar)
        self.motivoAccess.sampleProcess.finished.connect(self.completeSampleProcess)

        # checking required build parameters

        self.advancedDialog.buildInputFileLineEdit.textChanged.connect(self.updateBuildButton)
        self.advancedDialog.buildOutputFileLineEdit.textChanged.connect(self.updateBuildButton)

        self.advancedDialog.buildTablesBasenameLineEdit.textChanged.connect(self.updateBuildButton)
        self.advancedDialog.buildTableSizeSpinBox.valueChanged.connect(self.updateBuildButton)

        self.advancedDialog.buildTreeletsFileLineEdit.textChanged.connect(self.updateBuildButton)
        self.advancedDialog.buildSelectiveCountCheckBox.toggled.connect(self.updateBuildButton)


        # checking required merge parameters

        self.advancedDialog.mergeOutputFileLineEdit.textChanged.connect(self.updateMergeButton)

        # checking required sample parameters

        self.advancedDialog.sampleInputFileLineEdit.textChanged.connect(self.updateSampleButton)
        self.advancedDialog.sampleOutputFileLineEdit.textChanged.connect(self.updateSampleButton)
        self.advancedDialog.sampleTablesBasenameLineEdit.textChanged.connect(self.updateSampleButton)

        self.advancedDialog.sampleSelectTreeletsToBuildFileLineEdit.textChanged.connect(self.updateSampleButton)
        self.advancedDialog.sampleSelectTreeletsToSampleFileLineEdit.textChanged.connect(self.updateSampleButton)

        self.advancedDialog.sampleEnableSelectiveBuildAndSamplingCheckBox.toggled.connect(self.updateSampleButton)

        # cancelButton

        self.advancedDialog.cancelButton.clicked.connect(self.cancelSampleProcess)


    def show(self):
        self.advancedDialog.show()


    # Read parameters

    def readBuildParameters(self):
        self.buildParameters.clear()

        # input graph
        paramValue = self.advancedDialog.buildInputFileLineEdit.text()
        self.buildParameters.setValueParameter('--graph', paramValue)

        # output

        paramValue = self.advancedDialog.buildOutputFileLineEdit.text()
        self.buildParameters.setValueParameter('--output', paramValue)

        # table size

        paramValue = self.advancedDialog.buildTableSizeSpinBox.text()
        self.buildParameters.setValueParameter('--size', paramValue)

        # number of colors

        paramValue = self.advancedDialog.buildNumberOfColorsSpinBox.text()
        self.buildParameters.setValueParameter('--colors', paramValue)


        # from vertex

        paramValue = self.advancedDialog.buildFromVertexSpinBox.text()
        self.buildParameters.setValueParameter('--from-vertex', paramValue)

        # to vertex

        if self.advancedDialog.buildToVertexSpinBox.isEnabled():
            paramValue = self.advancedDialog.buildToVertexSpinBox.text()
            self.buildParameters.setValueParameter('--to-vertex', paramValue)



        # threads

        paramValue = self.advancedDialog.buildThreadsSpinBox.text()
        self.buildParameters.setValueParameter('--threads', paramValue)



        # coloring bias

        paramValue = self.advancedDialog.buildColoringBiasSpinBox.text()
        self.buildParameters.setValueParameter('--coloring-bias', paramValue)

        # tables basename

        if self.advancedDialog.buildTablesBasenameLineEdit.isEnabled():
            paramValue = self.advancedDialog.buildTablesBasenameLineEdit.text()
            self.buildParameters.setValueParameter('--tables-basename', paramValue)

        # seed

        paramValue = self.advancedDialog.buildSeedLineEdit.text().strip()
        self.buildParameters.setValueParameter('--seed', paramValue)


        # count only treelets in file

        if self.advancedDialog.buildTreeletsFileLineEdit.isEnabled():
            paramValue = self.advancedDialog.buildTreeletsFileLineEdit.text()
            self.buildParameters.setValueParameter('--selective', paramValue)

        # set store-on-0-colored-vertices-only flag

        if self.advancedDialog.buildStore0ColoredOnlyCheckBox.isChecked():
            self.buildParameters.setFlagParameter('--store-on-0-colored-vertices-only')




    def readMergeParameters(self):
        self.mergeParameters.clear()

        paramValue = self.advancedDialog.mergeOutputFileLineEdit.text()
        paramValue = paramValue[:paramValue.rfind('.')]
        paramValue += ' ' + self.advancedDialog.mergeOutputFileLineEdit.text()
        self.mergeParameters.setValueParameter('--output', paramValue)

        if self.advancedDialog.mergeCompressThresholdSpinBox.isEnabled():
            paramValue = self.advancedDialog.mergeCompressThresholdSpinBox.text()
            self.mergeParameters.setValueParameter('--compress-threshold', paramValue)

    def readSampleParameters(self):
        self.sampleParameters.clear()

        # input
        paramValue = self.advancedDialog.sampleInputFileLineEdit.text()
        self.sampleParameters.setValueParameter('--graph', paramValue)

        # output

        paramValue = self.advancedDialog.sampleOutputFileLineEdit.text()
        self.sampleParameters.setValueParameter('--output', paramValue)
        self.outputFile = paramValue

        # size of the treelets

        paramValue = self.advancedDialog.sampleSizeOfTreeletsSpinBox.text()
        self.sampleParameters.setValueParameter('--size', paramValue)

        # number of samples

        if self.advancedDialog.sampleNumberOfSamplesCheckBox.isChecked():
            paramValue = self.advancedDialog.sampleNumberOfSamplesSpinBox.text()
            self.sampleParameters.setValueParameter('--num-samples', paramValue)

        # threads

        paramValue = self.advancedDialog.sampleThreadsSpinBox.text()
        self.sampleParameters.setValueParameter('--threads', paramValue)

        # time budget

        if self.advancedDialog.sampleTimeBudgetSpinBox.isEnabled():
            paramValue = self.advancedDialog.sampleTimeBudgetSpinBox.text()
            self.sampleParameters.setValueParameter('--time-budget', paramValue)

        # tables basename

        paramValue = self.advancedDialog.sampleTablesBasenameLineEdit.text()
        self.sampleParameters.setValueParameter('--tables-basename', paramValue)

        # seed

        paramValue = self.advancedDialog.sampleSeedLineEdit.text()
        self.sampleParameters.setValueParameter('--seed', paramValue)

        # Treelet buffering

        if self.advancedDialog.sampleEnableTreeletBufferingCheckBox.isChecked():
            paramValue = self.advancedDialog.sampleTreeletBufferSizeSpinBox.text()
            self.sampleParameters.setValueParameter('--treelet-buffer-size', paramValue)

            paramValue = self.advancedDialog.sampleTreeletBufferDegreeSpinBox.text()
            self.sampleParameters.setValueParameter('--treelet-buffer-degree', paramValue)

        # selective build and sampling

        if self.advancedDialog.sampleEnableSelectiveBuildAndSamplingCheckBox.isChecked():
            paramValue = self.advancedDialog.sampleSelectTreeletsToBuildFileLineEdit.text()
            self.sampleParameters.setValueParameter('--selective-build', paramValue)

            paramValue = self.advancedDialog.sampleSelectTreeletsToSampleFileLineEdit.text()
            self.sampleParameters.setValueParameter('--selective', paramValue)

        # smart-stars

        if self.advancedDialog.sampleSmartStarsCheckBox.isChecked():
            self.sampleParameters.setFlagParameter('--smart-stars')

            if self.advancedDialog.sampleNumberOfStarsCheckBox.isChecked() == False:
                paramValue = self.advancedDialog.sampleNumberOfStarsSpinBox.text()
                self.sampleParameters.setValueParameter('--num-stars', paramValue)

        # flags

        if self.advancedDialog.sampleCanonicizeCheckBox.isChecked():
            self.sampleParameters.setFlagParameter('--canonicize')

        if self.advancedDialog.sampleNoSpanningTreesCheckBox.isChecked():
            self.sampleParameters.setFlagParameter('--spanning-trees-no')

        if self.advancedDialog.sampleGroupCheckBox.isChecked():
            self.sampleParameters.setFlagParameter('--group')

        if self.advancedDialog.sampleVerticesCheckBox.isChecked():
            self.sampleParameters.setFlagParameter('--vertices')

        if self.advancedDialog.sampleGraphletsCheckBox.isChecked():
            self.sampleParameters.setFlagParameter('--graphlets')

        if self.advancedDialog.sampleEstimateOccurencesCheckBox.isChecked():
            self.sampleParameters.setFlagParameter('--estimate-occurrences')

        if self.advancedDialog.sampleEstimateOccurencesCheckBox.isChecked():
            self.sampleParameters.setFlagParameter('--estimate-occurrences-adaptive')

    # Run buttons

    def runBuild(self):
        self.readBuildParameters()

        self.advancedDialog.buildProgressBar.setValue(0)
        self.advancedDialog.buildButton.setEnabled(False)

        #print(self.buildParameters.getAsArguments())

        self.motivoAccess.runBuild(self.buildParameters.getAsArguments())


    def runMerge(self):
        self.readMergeParameters()

        self.advancedDialog.mergeProgressBar.setValue(0)
        self.advancedDialog.mergeButton.setEnabled(False)

        #print(self.mergeParameters.getAsArguments())

        self.motivoAccess.runMerge(self.mergeParameters.getAsArguments())

    def runSample(self):
        self.readSampleParameters()

        self.advancedDialog.sampleProgressBar.setValue(0)
        self.advancedDialog.sampleButton.setEnabled(False)

        self.showCancelButton()

        #print(self.sampleParameters.getAsArguments())

        self.motivoAccess.runSample(self.sampleParameters.getAsArguments())


    # file browsing

    def buildSelectInputFile(self):

        filePathAndName = self.fileDialog.getOpenFileName()[0]

        if filePathAndName[filePathAndName.rfind('.'):] == '.txt':
            self.openConvertTxtToBinaryDialog(filePathAndName)
            filePathAndName = ''
        elif filePathAndName[filePathAndName.rfind('.'):] == '.ged' or filePathAndName[filePathAndName.rfind('.'):] == '.gof':
            filePathAndName = filePathAndName[:filePathAndName.rfind('.')]
        else:
            self.errorMessage.critical(self.advancedDialog, 'Incorrect file format', 'Incorrect input graph file format')
            filePathAndName = ''


        self.advancedDialog.buildInputFileLineEdit.setText(filePathAndName)

    def buildSelectOutputFile(self):

        filePathAndName = self.fileDialog.getExistingDirectory()

        if filePathAndName != '':
            filePathAndName += '/' + 'tables'

        self.advancedDialog.buildOutputFileLineEdit.setText(filePathAndName)
        self.advancedDialog.buildTablesBasenameLineEdit.setText(filePathAndName)


    def buildSelectTreeletsFile(self):
        filePathAndName = self.fileDialog.getOpenFileName()[0]

        self.advancedDialog.buildTreeletsFileLineEdit.setText(filePathAndName)



    def mergeSelectOutputFile(self):
        #filesPath = ''.join([str(str(elem) + ' ')  for elem in self.fileDialog.getOpenFileNames()[0]])
        filePathAndName = self.fileDialog.getOpenFileName()[0]

        if filePathAndName[filePathAndName.rfind('.'):] == '.cnt':
            self.advancedDialog.mergeOutputFileLineEdit.setText(filePathAndName)
        else:
            self.errorMessage.critical(self.advancedDialog, 'Incorrect file format', 'Incorrect file format')


    def sampleSelectInputFile(self):

        filePathAndName = self.fileDialog.getOpenFileName()[0]

        if filePathAndName[filePathAndName.rfind('.'):] == '.txt':
            self.openConvertTxtToBinaryDialog(filePathAndName)
            filePathAndName = ''
        elif filePathAndName[filePathAndName.rfind('.'):] == '.ged' or filePathAndName[filePathAndName.rfind('.'):] == '.gof':
            filePathAndName = filePathAndName[:filePathAndName.rfind('.')]
        else:
            self.errorMessage.critical(self.advancedDialog, 'Incorrect file format', 'Incorrect input graph file format')
            filePathAndName = ''

        self.advancedDialog.sampleInputFileLineEdit.setText(filePathAndName)

    def sampleSelectOutputFile(self):

        filePathAndName = self.fileDialog.getExistingDirectory()

        if filePathAndName != '':
            filePathAndName += '/' + 'output'

        self.advancedDialog.sampleOutputFileLineEdit.setText(filePathAndName)


    def sampleSelectTreeletsToBuildFile(self):
        filePathAndName = self.fileDialog.getOpenFileName()[0]

        self.advancedDialog.sampleSelectTreeletsToBuildFileLineEdit.setText(filePathAndName)

    def sampleSelectTreeletsToSampleFile(self):
        filePathAndName = self.fileDialog.getOpenFileName()[0]

        self.advancedDialog.sampleSelectTreeletsToSampleFileLineEdit.setText(filePathAndName)



    # Parameter implications

    def buildTableSizeImplications(self):

        sizeOverOne = self.advancedDialog.buildTableSizeSpinBox.value() > 1

        # to do: add/delete to/from REQUIRED list

        self.advancedDialog.buildNumberOfColorsSpinBox.setDisabled(sizeOverOne)

        self.advancedDialog.buildTablesBasenameLineEdit.setEnabled(sizeOverOne)

        # To Do: 0 = using the number of logical processors
        self.advancedDialog.buildThreadsSpinBox.setEnabled(sizeOverOne)

        self.advancedDialog.buildStore0ColoredOnlyCheckBox.setEnabled(sizeOverOne)

    def sampleSmartStarImplications(self):
        if self.advancedDialog.sampleSmartStarsCheckBox.isChecked():
            self.advancedDialog.sampleNumberOfStarsCheckBox.setEnabled(True)

            if self.advancedDialog.sampleNumberOfStarsCheckBox.isChecked():
                self.advancedDialog.sampleNumberOfStarsSpinBox.setDisabled(True)
            else:
                self.advancedDialog.sampleNumberOfStarsSpinBox.setEnabled(True)

        else:
            self.advancedDialog.sampleNumberOfStarsCheckBox.setDisabled(True)
            self.advancedDialog.sampleNumberOfStarsSpinBox.setDisabled(True)


    def suggestAfterBuildInputs(self):
        if self.advancedDialog.mergeOutputFileLineEdit.text() == '':
            self.advancedDialog.mergeOutputFileLineEdit.setText(self.buildParameters.valueParameters['--output'] + '.' + self.buildParameters.valueParameters['--size'] + '.cnt')

        if self.advancedDialog.sampleInputFileLineEdit.text() == '':
            self.advancedDialog.sampleInputFileLineEdit.setText(self.buildParameters.valueParameters['--graph'])

        if self.advancedDialog.sampleTablesBasenameLineEdit.text() == '' and '--tables-basename' in self.buildParameters.valueParameters:
            self.advancedDialog.sampleTablesBasenameLineEdit.setText(self.buildParameters.valueParameters['--tables-basename'])



    def displayBuildError(self):
        print(self.motivoAccess.buildProcess.readAllStandardError())
        if self.motivoAccess.buildProcess.exitStatus() != 0:
            self.errorMessage.critical(self.advancedDialog, "motivo-build", str(self.motivoAccess.buildProcess.readAllStandardError()))

    def displayMergeError(self):
        print(self.motivoAccess.mergeProcess.readAllStandardError())
        if self.motivoAccess.mergeProcess.exitStatus() != 0:
            self.errorMessage.critical(self.advancedDialog, "motivo-merge", str(self.motivoAccess.mergeProcess.readAllStandardError()))


    def displaySampleError(self):
        errorText = str(self.motivoAccess.sampleProcess.readAllStandardError())
        print(errorText)

        #if self.motivoAccess.sampleProcess.exitStatus() != 0 and errorText != "b''":
        #    self.errorMessage.critical(self.advancedDialog, "motivo-sample", errorText)


    def updateBuildProgressBar(self):

        progress = min(self.advancedDialog.buildProgressBar.value() + 20, 90)

        self.advancedDialog.buildProgressBar.setValue(progress)

    def completeBuildProcess(self):

        self.advancedDialog.buildProgressBar.setValue(100)
        self.advancedDialog.buildButton.setEnabled(True)


    def updateMergeProgressBar(self):

        progress = min(self.advancedDialog.mergeProgressBar.value() + 20, 90)

        self.advancedDialog.mergeProgressBar.setValue(progress)

    def completeMergeProcess(self):

        self.advancedDialog.mergeProgressBar.setValue(100)
        self.advancedDialog.mergeButton.setEnabled(True)


    def updateSampleProgressBar(self):

        progress = min(self.advancedDialog.sampleProgressBar.value() + 20, 90)

        self.advancedDialog.sampleProgressBar.setValue(progress)

    def completeSampleProcess(self):

        self.advancedDialog.sampleButton.setEnabled(True)

        self.showSampleButton()

        if self.sampleCancelled:
            self.advancedDialog.sampleProgressBar.setValue(0)
            self.sampleCancelled = False
        else:
            self.advancedDialog.sampleProgressBar.setValue(100)
            self.outputReady.emit(1)


    def getOutputFile(self):
        return self.outputFile


    def updateBuildButton(self):
        completeInput = True

        if self.advancedDialog.buildInputFileLineEdit.text().strip() == '':
            self.advancedDialog.buildInputFileLineEdit.setStyleSheet("border: 1px ridge red;")
            completeInput = False
        else:
            self.advancedDialog.buildInputFileLineEdit.setStyleSheet("")

        if self.advancedDialog.buildOutputFileLineEdit.text().strip() == '':
            self.advancedDialog.buildOutputFileLineEdit.setStyleSheet("border: 1px ridge red;")
            completeInput = False
        else:
            self.advancedDialog.buildOutputFileLineEdit.setStyleSheet("")


        if self.advancedDialog.buildTablesBasenameLineEdit.text().strip() == '' and self.advancedDialog.buildTablesBasenameLineEdit.isEnabled():
            self.advancedDialog.buildTablesBasenameLineEdit.setStyleSheet("border: 1px ridge red;")
            completeInput = False
        else:
            self.advancedDialog.buildTablesBasenameLineEdit.setStyleSheet("")



        if self.advancedDialog.buildTreeletsFileLineEdit.text().strip() == '' and self.advancedDialog.buildTreeletsFileLineEdit.isEnabled():
            self.advancedDialog.buildTreeletsFileLineEdit.setStyleSheet("border: 1px ridge red;")
            completeInput = False
        else:
            self.advancedDialog.buildTreeletsFileLineEdit.setStyleSheet("")


        self.advancedDialog.buildButton.setEnabled(completeInput)

    def updateMergeButton(self):
        completeInput = True

        if self.advancedDialog.mergeOutputFileLineEdit.text().strip() == '':
            self.advancedDialog.mergeOutputFileLineEdit.setStyleSheet("border: 1px ridge red;")
            completeInput = False
        else:
            self.advancedDialog.mergeOutputFileLineEdit.setStyleSheet("")

        self.advancedDialog.mergeButton.setEnabled(completeInput)

    def updateSampleButton(self):
        completeInput = True

        if self.advancedDialog.sampleInputFileLineEdit.text().strip() == '':
            self.advancedDialog.sampleInputFileLineEdit.setStyleSheet("border: 1px ridge red;")
            completeInput = False
        else:
            self.advancedDialog.sampleInputFileLineEdit.setStyleSheet("")


        if self.advancedDialog.sampleOutputFileLineEdit.text().strip() == '':
            self.advancedDialog.sampleOutputFileLineEdit.setStyleSheet("border: 1px ridge red;")
            completeInput = False
        else:
            self.advancedDialog.sampleOutputFileLineEdit.setStyleSheet("")


        if self.advancedDialog.sampleTablesBasenameLineEdit.text().strip() == '':
            self.advancedDialog.sampleTablesBasenameLineEdit.setStyleSheet("border: 1px ridge red;")
            completeInput = False
        else:
            self.advancedDialog.sampleTablesBasenameLineEdit.setStyleSheet("")


        if self.advancedDialog.sampleSelectTreeletsToSampleFileLineEdit.text().strip() == '' and self.advancedDialog.sampleSelectTreeletsToSampleFileLineEdit.isEnabled():
            self.advancedDialog.sampleSelectTreeletsToSampleFileLineEdit.setStyleSheet("border: 1px ridge red;")
            completeInput = False
        else:
            self.advancedDialog.sampleSelectTreeletsToSampleFileLineEdit.setStyleSheet("")


        if self.advancedDialog.sampleSelectTreeletsToBuildFileLineEdit.text().strip() == '' and self.advancedDialog.sampleSelectTreeletsToBuildFileLineEdit.isEnabled():
            self.advancedDialog.sampleSelectTreeletsToBuildFileLineEdit.setStyleSheet("border: 1px ridge red;")
            completeInput = False
        else:
            self.advancedDialog.sampleSelectTreeletsToBuildFileLineEdit.setStyleSheet("")

        self.advancedDialog.sampleButton.setEnabled(completeInput)

    def openConvertTxtToBinaryDialog(self, filePathAndName):
        self.convertTxtToBinaryDialog.setGraphFile(filePathAndName)
        self.convertTxtToBinaryDialog.show()





    # Cancelling the sampling process


    def showCancelButton(self):
        self.advancedDialog.cancelButton.show()

        self.advancedDialog.sampleButton.hide()


    def showSampleButton(self):
        self.advancedDialog.cancelButton.hide()

        self.advancedDialog.sampleButton.show()

    def cancelSampleProcess(self):
        self.sampleCancelled = True
        self.motivoAccess.sampleProcess.kill()
        self.showSampleButton()
