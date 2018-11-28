# Copyright (c) 2018 Koninklijke Philips N.V.
from viewingTestResult import ViewingTestResult
import os.path


class ReviewingTestResult(ViewingTestResult):
    def __init__(self, testSystem, testName):
        super().__init__(testSystem, testName)

    def get_latest_result(self):
        if os.path.isfile(self.resultFile):
            config = self.get_config()
            if "MONOPLANE" in config:
                return self.get_result("MONOPLANE")
            elif "BIPLANE" in config:
                return self.get_result("BIPLANE")
            else:
                return "Not found"
        else:
            return "Not found"
