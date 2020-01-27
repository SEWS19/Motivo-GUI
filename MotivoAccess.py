# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QProcess, QThread, Signal, Slot
#from PySide2.QtWidgets import QMessageBox
from MotivoParameters import MotivoParameters
#from UserPreferencesDialog import UserPreferencesDialog
from definitions import MOTIVO_DIR

class MotivoAccess:

    motivoDirectory =  MOTIVO_DIR

    def __init__(self):

        self.motivoProcess = QProcess()

        self.buildProcess = QProcess()
        self.mergeProcess = QProcess()
        self.sampleProcess = QProcess()

        self.graphProcess = QProcess()

        # TODO check motivo directory and produce an error message if needed
        self.motivoProcess.setWorkingDirectory(MotivoAccess.motivoDirectory + '/scripts/')
        self.motivoProcess.setProgram('motivo.sh')
        # Qproces emit readReady signal when data is ready to be read
        # Connect the handler for read the data  

        self.buildProcess.setWorkingDirectory(MotivoAccess.motivoDirectory + '/build/bin/')
        self.buildProcess.setProgram('motivo-build')

        self.mergeProcess.setWorkingDirectory(MotivoAccess.motivoDirectory + '/build/bin/')
        self.mergeProcess.setProgram('motivo-merge')

        self.sampleProcess.setWorkingDirectory(MotivoAccess.motivoDirectory + '/build/bin/')
        self.sampleProcess.setProgram('motivo-sample')

        self.graphProcess.setWorkingDirectory(MotivoAccess.motivoDirectory + '/build/bin/')
        self.graphProcess.setProgram('motivo-graph')


    def runMotivo(self, motivoArguments):
        self.motivoProcess.setArguments(motivoArguments)
        self.motivoProcess.start()

    def runBuild(self, buildArguments):
        self.buildProcess.setArguments(buildArguments)
        self.buildProcess.start()

    def runMerge(self, mergeArguments):
        self.mergeProcess.setArguments(mergeArguments)
        self.mergeProcess.start()

    def runSample(self, sampleArguments):
        self.sampleProcess.setArguments(sampleArguments)
        self.sampleProcess.start()

    def runConvertTxtToBinary(self, convertTxtToBinaryArguments):
        self.graphProcess.setArguments(convertTxtToBinaryArguments)
        self.graphProcess.start()
