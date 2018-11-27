# Copyright (c) 2018 Koninklijke Philips N.V.
from testResult import TestResult
import os.path
import re


class IpislibTestResult(TestResult):
    def __init__(self, testSystem, testName):
        super().__init__(testSystem, testName)
        self.resultFile = os.path.join(self.resultPath, 'test_summary.txt')

    def get_latest_result(self):
        if os.path.isfile(self.resultFile):
            config = self.get_config()
            if "MONOPLANE" in config:
                return self.get_result("FRONTAL")
            elif "BIPLANE" in config:
                frontalPassed = self.get_result("FRONTAL") == "PASSED"
                lateralPassed = self.get_result("LATERAL") == "PASSED"
                biplanePassed = self.get_result("BIPLANE") == "PASSED"
                if frontalPassed and lateralPassed and biplanePassed:
                    return "PASSED"
                else:
                    return "FAILED"
            else:
                return "Not found"
        else:
            return "Not found"

    def get_config(self):
        return self.get_summary_element("CONFIG")

    def get_result(self, systemMode):
        summaryElement = self.get_summary_element(systemMode)
        if summaryElement != "Not found":
            testResultStr = "Overal TestResult ===>"
            subStringContainingResult = summaryElement[testResultStr.__len__():]
            return self.get_alpha_numeric_characters(subStringContainingResult)
        return "Not found"

    def get_summary_element(self, summaryElement):
        returnValue = "Not found"
        summaryElementStr = summaryElement + ":"
        resultFile = open(self.resultFile, 'r')
        for line in resultFile:
            if summaryElementStr in line:
                returnValue = line[summaryElementStr.__len__():]
        resultFile.close()
        return returnValue

    def get_alpha_numeric_characters(self, line):
        pattern = re.compile('\W')
        return re.sub(pattern, '', line)