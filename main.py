# This Python file uses the following encoding: utf-8
# vim:set ts=2 sts=2 sw=2 et:
import sys
from MotivoGUI import MotivoGUI
from PySide2.QtWidgets import QApplication
from definitions import ROOT_DIR

if __name__ == "__main__":
    app = QApplication(sys.argv)

    motivoGUI = MotivoGUI()
    motivoGUI.show()

    sys.exit(app.exec_())
