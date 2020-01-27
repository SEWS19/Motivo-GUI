# This Python file uses the following encoding: utf-8

class MotivoParameters:
    def __init__(self):
        self.valueParameters = dict()
        self.flagParameters = dict()


    def setValueParameter(self, parameterName, parameterValue):
        self.valueParameters[parameterName] = parameterValue

    def setFlagParameter(self, parameterName):
        self.flagParameters[parameterName] = True

    def getAsArguments(self):
        motivoArguments = ""

        for parameterName in self.valueParameters:
            if self.valueParameters[parameterName] is not None and self.valueParameters[parameterName] is not '':
                motivoArguments += parameterName + ' ' + self.valueParameters[parameterName] + ' '

        #motivoArguments = list("-g /home/wrabbit/motivo/build/test-graph -o /home/wrabbit/motivo/build/RVL/output -k 5 -s 100000".split())

        for parameterName in self.flagParameters:
            if self.flagParameters[parameterName]:
                motivoArguments += parameterName + ' '

        motivoArguments = list(motivoArguments.split())
        #print(motivoArguments)

        return motivoArguments

    def getInputFile(self):
        try:
            return self.valueParameters['--graph']
        except:
            return ''

    def getOutputFile(self):
        try:
            return self.valueParameters['--output']
        except:
            return ''

    def ioFilesSelected(self):
        return self.getInputFile() != '' and self.getOutputFile() != ''

    def clear(self):
        self.valueParameters.clear()
        self.flagParameters.clear()
