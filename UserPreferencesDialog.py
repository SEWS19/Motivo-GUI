# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QDialog
from getUiFromFile import getUiFromFile
from definitions import UI_DIR
from PySide2.QtWidgets import QFileDialog
from PySide2.QtCore import QSettings
from definitions import MOTIVO_DIR
from MotivoAccess import MotivoAccess
import os

class UserPreferencesDialog(QDialog):

    motivoDirectory = MOTIVO_DIR

    def __init__(self, parent = None):
        super(UserPreferencesDialog, self).__init__(parent)

        self.userPreferencesDialog = getUiFromFile(os.path.join(UI_DIR,"userpreferencesdialog.ui"))


        self.fileDialog = QFileDialog()
        self.userPreferencesSettingsFile = QSettings("Motivo GUI", "project20")

        self.getMotivoDirectory()

        self.userPreferencesDialog.setDirectoryButton.clicked.connect(self.setMotivoDirectory)
        self.userPreferencesDialog.selectMotivoDirectoryButton.clicked.connect(self.openDirectoryBrowser)


    def show(self):
        self.userPreferencesDialog.show()

    def openDirectoryBrowser(self):

        motivoDir = self.fileDialog.getExistingDirectory()

        self.userPreferencesDialog.motivoDirectoryLineEdit.setText(motivoDir)

    def getMotivoDirectory(self):
        if self.userPreferencesSettingsFile.value("motivoDirectory") is not '' and self.userPreferencesSettingsFile.value("motivoDirectory") is not None:
            self.motivoDirectory = self.userPreferencesSettingsFile.value("motivoDirectory")
            self.userPreferencesDialog.motivoDirectoryLineEdit.setText(self.motivoDirectory)

            UserPreferencesDialog.motivoDirectory = self.motivoDirectory
            MotivoAccess.motivoDirectory = self.motivoDirectory
        return self.motivoDirectory

    def setMotivoDirectory(self):
        self.motivoDirectory = self.userPreferencesDialog.motivoDirectoryLineEdit.text()
        self.userPreferencesSettingsFile.setValue("motivoDirectory", self.motivoDirectory)


        self.userPreferencesDialog.close()
