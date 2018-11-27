# Copyright (c) 2018 Koninklijke Philips N.V.
from testResult import TestResult
import os.path
import re
import zipfile


class ReviewingTestResult(TestResult):
    def __init__(self, testSystem, testName):
        super().__init__(testSystem, testName)
        self.resultFile = os.path.join(self.resultPath, 'RevTestHarness_ur.TestReport')

        self.zipFile = os.path.join(self.resultPath, 'TestReports.zip')
        if not os.path.isfile(self.resultFile) and os.path.isfile(self.zipFile):
            self.unzip_testresults()

    def get_latest_result(self):
        if os.path.isfile(self.resultFile):
            resultFile = open(self.resultFile, 'r')
            testResultStr = "Overal TestResult ===>"
            for line in resultFile:
                if testResultStr in line:
                    subStringContainingResult = line[testResultStr.__len__():]
                    return self.get_alpha_numeric_characters(subStringContainingResult)
            return "Not found"
        else:
            return "Not found"

    def unzip_testresults(self):
        zip_ref = zipfile.ZipFile(self.zipFile, 'r')
        zip_ref.extractall(self.resultPath)
        zip_ref.close()

    def get_alpha_numeric_characters(self, line):
        pattern = re.compile('\W')
        return re.sub(pattern, '', line)