import unittest
from PySide2.QtCore import Qt, QObject
from PySide2.QtWidgets import QApplication
from PySide2.QtTest import QTest

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from MotivoGUI import MainWindow


class TestAdvancedDialog(unittest.TestCase):

    def testSampleButtonProgressBar(self):
            mainWindow = MainWindow()
            file_button = mainWindow.advancedDialog.fileDialog
            self.assert_(file_button.isEnabled())
            mainWindow.advancedDialog.advancedDialog.show()
            self.assert_(mainWindow.advancedDialog.advancedDialog.isVisible())
            QTest.mouseClick(mainWindow.advancedDialog.advancedDialog.sampleTab, Qt.LeftButton)
            sample_button = mainWindow.advancedDialog.advancedDialog.sampleButton
            self.assertFalse(sample_button.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleProgressBar.isEnabled())


#Check the default settings for input graph and output directory at the sample tab
    def testInputOutput(self):
            mainWindow = MainWindow()
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleSelectInputFileButton.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleSelectOutputFileButton.isEnabled())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleSelectTreeletsToBuildFileButton.isEnabled())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleSelectTreeletsToSampleFileButton.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleInputFileLineEdit.text() == '')
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleOutputFileLineEdit.text() == '')

    def testSpinBox(self):
            mainWindow = MainWindow()
            #size of treelets
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleSizeOfTreeletsSpinBox.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleSizeOfTreeletsSpinBox.value(), 1)
            #Number of samples
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleNumberOfSamplesSpinBox.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleNumberOfSamplesSpinBox.value(), 1000000)
            #Threads
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleThreadsSpinBox.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleThreadsSpinBox.value(), 1)
            #Sample time budget
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleTimeBudgetSpinBox.isEnabled())
            #treelet buffer size
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleTreeletBufferSizeSpinBox.isEnabled())
            #treelet buffer degree
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleTreeletBufferDegreeSpinBox.isEnabled())
            #proportional number of starts
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleNumberOfStarsSpinBox.isEnabled())

    def testTextBox(self):
            mainWindow = MainWindow()
            #Tables basename
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleTablesBasenameLineEdit.text() == '')
            #seed
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleSeedLineEdit.text() == '')
            #selective sampling
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleSelectTreeletsToBuildFileLineEdit.text() == '')
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleSelectTreeletsToSampleFileLineEdit.text() == '')



#Check the default in checkboxes in the sample tab
    def testCheckboxNumberofSamples(self):
            mainWindow = MainWindow()
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleNumberOfSamplesCheckBox.isChecked())
            QTest.mouseClick(mainWindow.advancedDialog.advancedDialog.sampleNumberOfSamplesCheckBox, Qt.LeftButton)
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleNumberOfSamplesCheckBox.isChecked())

    def testTimeBudget(self):
            mainWindow = MainWindow()
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleTimeBudgetCheckBox.isChecked())
            QTest.mouseClick(mainWindow.advancedDialog.advancedDialog.sampleTimeBudgetCheckBox, Qt.LeftButton)
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleTimeBudgetCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleTimeBudgetSpinBox.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleTimeBudgetSpinBox.value(), 1)

    def testTreeletBuffering(self):
            mainWindow = MainWindow()
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleEnableTreeletBufferingCheckBox.isChecked())
            QTest.mouseClick(mainWindow.advancedDialog.advancedDialog.sampleEnableTreeletBufferingCheckBox, Qt.LeftButton)
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleEnableTreeletBufferingCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleTreeletBufferSizeSpinBox.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleTreeletBufferSizeSpinBox.value(), 10000)
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleTreeletBufferDegreeSpinBox.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleTreeletBufferDegreeSpinBox.value(), 1)

    def testSelectiveBuildingSampling(self):
            mainWindow = MainWindow()
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleEnableSelectiveBuildAndSamplingCheckBox.isChecked())
            QTest.mouseClick(mainWindow.advancedDialog.advancedDialog.sampleEnableSelectiveBuildAndSamplingCheckBox, Qt.LeftButton)
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleEnableSelectiveBuildAndSamplingCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleSelectTreeletsToBuildFileButton.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleSelectTreeletsToSampleFileButton.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleSelectTreeletsToBuildFileLineEdit.text() == '')
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleSelectTreeletsToSampleFileLineEdit.text() == '')

    def testSmartStars(self):
            mainWindow = MainWindow()
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleSmartStarsCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleNumberOfStarsCheckBox.isChecked())
            QTest.mouseClick(mainWindow.advancedDialog.advancedDialog.sampleNumberOfStarsCheckBox, Qt.LeftButton)
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleNumberOfStarsCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleNumberOfStarsSpinBox.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleNumberOfStarsSpinBox.value(), 1)
            QTest.mouseClick(mainWindow.advancedDialog.advancedDialog.sampleSmartStarsCheckBox, Qt.LeftButton)
            #self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleSmartStarsCheckBox.isChecked())
            #self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleNumberOfStarsCheckBox.isEnabled())
            #self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleNumberOfStarsSpinBox.isEnabled())

    def testDefaultcheckboxes(self):
            mainWindow = MainWindow()
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleGraphletsCheckBox.isChecked())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleEstimateOccurencesCheckBox.isChecked())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleEstimateOccurencesAdaptiveCheckBox.isChecked())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleCanonicizeCheckBox.isChecked())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleNoSpanningTreesCheckBox.isChecked())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleGroupCheckBox.isChecked())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleVerticesCheckBox.isChecked())



    def testCombination(self):
            mainWindow = MainWindow()
            QTest.mouseClick(mainWindow.advancedDialog.advancedDialog.sampleEstimateOccurencesCheckBox, Qt.LeftButton)
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleEstimateOccurencesCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleGraphletsCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleNoSpanningTreesCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleGroupCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleVerticesCheckBox.isChecked())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleEstimateOccurencesAdaptiveCheckBox.isChecked())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleCanonicizeCheckBox.isChecked())

            QTest.mouseClick(mainWindow.advancedDialog.advancedDialog.sampleEstimateOccurencesAdaptiveCheckBox, Qt.LeftButton)
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleEstimateOccurencesCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleGraphletsCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleNoSpanningTreesCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleGroupCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleVerticesCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleEstimateOccurencesAdaptiveCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleCanonicizeCheckBox.isChecked())


            QTest.mouseClick(mainWindow.advancedDialog.advancedDialog.sampleEstimateOccurencesCheckBox, Qt.LeftButton)
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleEstimateOccurencesCheckBox.isChecked())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleGraphletsCheckBox.isChecked())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleNoSpanningTreesCheckBox.isChecked())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleGroupCheckBox.isChecked())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.sampleVerticesCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleEstimateOccurencesAdaptiveCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.sampleCanonicizeCheckBox.isChecked())



    def testBuildMergeButtonProgressbar(self):
            mainWindow = MainWindow()
            QTest.mouseClick(mainWindow.advancedDialog.advancedDialog.buildTab, Qt.LeftButton)
            merge_button = mainWindow.advancedDialog.advancedDialog.mergeButton
            self.assertFalse(merge_button.isEnabled())
            build_button = mainWindow.advancedDialog.advancedDialog.buildButton
            self.assertFalse(build_button.isEnabled())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.buildSelectTreeletsFileButton.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildProgressBar.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.mergeProgressBar.isEnabled())


    def testBuildMergeInputOutput(self):
            mainWindow = MainWindow()
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildSelectInputFileButton.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildSelectOutputFileButton.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.mergeSelectOutputFileButton.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildInputFileLineEdit.text() == '')
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildOutputFileLineEdit.text() == '')
            self.assert_(mainWindow.advancedDialog.advancedDialog.mergeOutputFileLineEdit.text() == '')

    def testBuilTableSize(self):
            mainWindow = MainWindow()
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildTableSizeSpinBox.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildTableSizeSpinBox.value(), 1)

    def testBuildColoringBias(self):
            mainWindow = MainWindow()
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildColoringBiasSpinBox.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildNumberOfColorsSpinBox.value(), 1)

    def testBuildFromVertex(self):
            mainWindow = MainWindow()
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildFromVertexSpinBox.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildFromVertexSpinBox.text() == '0')

    def testBuildToVertex(self):
            mainWindow =MainWindow()
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.buildToVertexSpinBox.isEnabled())

    def testBuildThreads(self):
            mainWindow = MainWindow()
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.buildThreadsSpinBox.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildColoringBiasSpinBox.value(), 1)

    def testBuildTextBoxes(self):
            mainWindow = MainWindow()
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.buildTablesBasenameLineEdit.isEnabled())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.buildTreeletsFileLineEdit.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildSeedLineEdit.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildSeedLineEdit.text() == '')

    def testMergeCompressThreshold(self):
            mainWindow = MainWindow()
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.mergeCompressThresholdSpinBox.isEnabled())

    def testBuildToVertexCheckBox(self):
            mainWindow = MainWindow()
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildToVertexCheckBox.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildToVertexCheckBox.isChecked())
            QTest.mouseClick(mainWindow.advancedDialog.advancedDialog.buildToVertexCheckBox, Qt.LeftButton)
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildToVertexSpinBox.isEnabled())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.buildToVertexCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildToVertexSpinBox.text() == '0')

    def testBuildTreeletCount(self):
            mainWindow = MainWindow()
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.buildSelectTreeletsFileButton.isEnabled())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.buildSelectiveCountCheckBox.isChecked())
            QTest.mouseClick(mainWindow.advancedDialog.advancedDialog.buildSelectiveCountCheckBox, Qt.LeftButton)
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildSelectTreeletsFileButton.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.buildTreeletsFileLineEdit.text() == '')

    def testMergeCompressThresholdCheckBox(self):
            mainWindow = MainWindow()
            self.assert_(mainWindow.advancedDialog.advancedDialog.mergeCompressThresholdCheckBox.isEnabled())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.mergeCompressThresholdCheckBox.isChecked())
            self.assertFalse(mainWindow.advancedDialog.advancedDialog.mergeCompressThresholdSpinBox.isEnabled())
            QTest.mouseClick(mainWindow.advancedDialog.advancedDialog.mergeCompressThresholdCheckBox, Qt.LeftButton)
            self.assert_(mainWindow.advancedDialog.advancedDialog.mergeCompressThresholdCheckBox.isChecked())
            self.assert_(mainWindow.advancedDialog.advancedDialog.mergeCompressThresholdSpinBox.isEnabled())
            self.assert_(mainWindow.advancedDialog.advancedDialog.mergeCompressThresholdSpinBox.value(), 1)



if __name__ == '__main__':
    unittest.main()
