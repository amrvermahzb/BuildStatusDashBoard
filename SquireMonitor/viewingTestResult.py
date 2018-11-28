# Copyright (c) 2018 Koninklijke Philips N.V.
from testResult import TestResult
import os.path
import re


class ViewingTestResult(TestResult):
    def __init__(self, testSystem, testName):
        super().__init__(testSystem, testName)
        self.resultFile = os.path.join(self.resultPath, 'test_summary.txt')

    def get_config(self):
        return self._get_summary_element("CONFIG")

    def get_result(self, systemMode):
        summaryElement = self._get_summary_element(systemMode)
        if summaryElement != "Not found":
            if "Overal TestResult" in summaryElement and "PASSED" in summaryElement:
                return "PASSED"
            else:
                return "FAILED"
        return "Not found"

    def _get_summary_element(self, summaryElement):
        returnValue = "Not found"
        summaryElementStr = summaryElement + ":"
        resultFile = open(self.resultFile, 'r')
        for line in resultFile:
            if summaryElementStr in line:
                returnValue = line[summaryElementStr.__len__():]
        resultFile.close()
        return returnValue

    def _get_alpha_numeric_characters(self, line):
        pattern = re.compile('\W')
        return re.sub(pattern, '', line)