# Copyright (c) 2018 Koninklijke Philips N.V.
from viewingTestResult import ViewingTestResult
import os.path
import re


class IpislibTestResult(ViewingTestResult):
    def __init__(self, testSystem, testName):
        super().__init__(testSystem, testName)

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
