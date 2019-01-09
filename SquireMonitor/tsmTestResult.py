# Copyright (c) 2018 Koninklijke Philips N.V.
from testResult import TestResult
import os.path
import xml.etree.ElementTree as ET


class TsmTestResult(TestResult):
    def __init__(self, testSystem, testName):
        super().__init__(testSystem, testName)
        self.resultFile = os.path.join(self.resultPath, 'TsmTestResults.xml')

    def get_latest_result(self):
        if os.path.isfile(self.resultFile):
            root = ET.parse(self.resultFile).getroot()
            for item in root.iter('test-suite'):
                if item.get('name') == "TsmUI_Automation":
                    return item.get('result')
            return "Not found"
        else:
            return "Not found"
