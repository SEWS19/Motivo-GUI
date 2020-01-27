# This Python file uses the following encoding: utf-8

import unittest
from PySide2.QtCore import Qt, QObject
from PySide2.QtWidgets import QApplication
from PySide2.QtTest import QTest

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from MotivoGUI import MainWindow


class TestBasicDialog(unittest.TestCase):


    def testWindow(self):
        mainWindow = MainWindow()
        file_button = mainWindow.basicDialog.fileDialog
        self.assert_(file_button.isEnabled())
        mainWindow.basicDialog.basicDialog.show()
        self.assert_(mainWindow.basicDialog.basicDialog.isVisible())


    def testButtonRunMotivo(self):
        mainWindow = MainWindow()
        motivo_button = mainWindow.basicDialog.basicDialog.runMotivoButton
        self.assertFalse(motivo_button.isEnabled())

    def testButtonInputGraph(self):
        mainWindow = MainWindow()
        input_graph = mainWindow.basicDialog.basicDialog.selectInputFileButton
        self.assert_(input_graph.isEnabled())
        QTest.mouseClick(input_graph, Qt.LeftButton)
        self.assert_(mainWindow.basicDialog.fileDialog.isEnabled())
        output_graph = mainWindow.basicDialog.basicDialog.selectOutputFileButton
        self.assert_(output_graph.isEnabled())
        QTest.mouseClick(output_graph, Qt.LeftButton)
        file_dialog1 = mainWindow.basicDialog.fileDialog
        self.assert_(file_dialog1.isEnabled())



    def testLineEmpty(self):
        mainWindow = MainWindow()
        inputText = mainWindow.basicDialog.basicDialog.inputFileLineEdit
        self.assertFalse(inputText.isModified())
        outputText = mainWindow.basicDialog.basicDialog.outputFileLineEdit
        self.assertFalse(outputText.isModified())

    def testSpinBox(self):
        mainWindow = MainWindow()
        graphletSize = mainWindow.basicDialog.basicDialog.graphletSizeSpinBox
        self.assert_(graphletSize.value(),1)
        numSample = mainWindow.basicDialog.basicDialog.numberOfSamplesSpinBox
        self.assert_(numSample.value(), 1000000)
        threads = mainWindow.basicDialog.basicDialog.threadsSpinBox
        self.assert_(threads.value(), 1)

    def testCheckBox(self):
        mainWindow = MainWindow()
        adaptiveCheckBox = mainWindow.basicDialog.basicDialog.adaptiveCheckBox
        self.assertFalse(adaptiveCheckBox.isChecked())
        QTest.mouseClick(adaptiveCheckBox, Qt.LeftButton)
        self.assert_(adaptiveCheckBox.isChecked())
        starsCheckBox = mainWindow.basicDialog.basicDialog.computeStarsCheckBox
        self.assert_(starsCheckBox.isChecked())
        QTest.mouseClick(starsCheckBox, Qt.LeftButton)
        self.assertFalse(starsCheckBox.isChecked())
        compressThreshold = mainWindow.basicDialog.basicDialog.compressThresholdCheckBox
        self.assertFalse(compressThreshold.isChecked())
        QTest.mouseClick(compressThreshold, Qt.LeftButton)
        self.assert_(compressThreshold.isChecked())



if __name__ == '__main__':
    unittest.main()
