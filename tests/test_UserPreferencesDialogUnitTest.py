import unittest
from PySide2.QtCore import Qt, QObject
from PySide2.QtWidgets import QApplication
from PySide2.QtTest import QTest

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from MotivoGUI import MainWindow


class TestUserPrefDialog(unittest.TestCase):

    def testWindow(self):
            mainWindow = MainWindow()
            file_button = mainWindow.userPreferencesDialog.fileDialog
            self.assert_(file_button.isEnabled())
            userpref_button = mainWindow.userPreferencesDialog.userPreferencesDialog
            self.assert_(userpref_button.isEnabled())
            self.assert_(mainWindow.userPreferencesDialog.userPreferencesSettingsFile.fallbacksEnabled())

    def testButton(self):
            mainWindow = MainWindow()
            self.assert_(mainWindow.userPreferencesDialog.userPreferencesDialog.setDirectoryButton.isEnabled())
            self.assert_(mainWindow.userPreferencesDialog.userPreferencesDialog.selectMotivoDirectoryButton.isEnabled())

            self.assert_(mainWindow.userPreferencesDialog.userPreferencesDialog.motivoDirectoryLineEdit.text() != "" )


if __name__ == '__main__':

    unittest.main()
