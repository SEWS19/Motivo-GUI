# This Python file uses the following encoding: utf-8

from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile

# load GUI designed in Qt Designer from a .ui file
def getUiFromFile(uiFileName):
    uiFile = QFile(uiFileName)
    uiFile.open(QFile.ReadOnly)

    uiLoader = QUiLoader()

    ui = uiLoader.load(uiFile)

    uiFile.close()

    return ui
