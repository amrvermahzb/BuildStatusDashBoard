from testResult import TestResult
import os.path
import xml.etree.ElementTree as ET


class NonSquireTestResult(TestResult):
    def __init__(self, testSystem, testName):
        super().__init__(testSystem, testName)
        fileName = self.testDirectory.get_latest_test_result_filename(testName) + " - Test Results.xml"
        self.resultFile = os.path.join(self.resultPath, fileName)

    def get_latest_result(self):
        if os.path.isfile(self.resultFile):
            root = ET.parse(self.resultFile).getroot()
            for item in root.iter():
                if item.tag == "RunResult":
                    return item.text
            return "Not found"
        else:
            return "Not found"
