import glob
import unittest

from PySide2.QtWidgets import QApplication

import sys

app = QApplication(sys.argv)

testSuite = unittest.TestSuite()
test_file_strings = glob.glob('test_*.py')
module_strings = [str[0:len(str)-3] for str in test_file_strings]
[__import__(str) for str in module_strings]
suites = [unittest.TestLoader().loadTestsFromName(str) for str in module_strings]
[testSuite.addTest(suite) for suite in suites]
print(testSuite)

result = unittest.TestResult()
testSuite.run(result)
print(result)

if __name__ == "__main__":
    unittest.main()
