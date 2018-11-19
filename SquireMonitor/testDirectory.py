# Copyright (c) 2018 Koninklijke Philips N.V.
import os.path
from os import scandir
from tests import Tests
from testSystems import TestSystems

TESTRESULTS_PATH = r'\\192.168.116.106\TestResults'
RESULT_FOLDERS = {TestSystems.Names.Squire1: "\SQUIREIP-1\\", TestSystems.Names.Squire2: "\SQUIREIP-2\\",
                  TestSystems.Names.Squire3: "\SQUIREIP-3\\", TestSystems.Names.Squire4: "\SQUIREIP-4\\",
                  TestSystems.Names.Squire5: "\SQUIREIP-5\\", TestSystems.Names.Squire6: "\SQUIREIP-6\\",
                  TestSystems.Names.Squire7: "\SQUIREIP-7\\", TestSystems.Names.Squire8: "\SQUIREIP-8\\",
                  TestSystems.Names.Squire9: "\SQUIREIP-9\\",
                  TestSystems.Names.BV2: "\CI\\NLYBSTQVP4DT7K5\\",
                  }

TEST_APPENDIX = {Tests.Names.Drive: "_DRIVE", Tests.Names.Loop: "_LOOP", Tests.Names.IVVR: "_IVVR",
                 Tests.Names.Install: "AlluraCIBatch", Tests.Names.Nightbatch: "PBL8x Development Nightbatch",
                 Tests.Names.Regressioncheck: "precheck"}


class TestDirectory:
    def __init__(self, squireName):
        self.squireFolder = TESTRESULTS_PATH + RESULT_FOLDERS[squireName]

    def get_test_paths(self, testName):
        testPaths = []
        for entry in os.scandir(self.squireFolder):
            if entry.is_dir() and TEST_APPENDIX[testName] in entry.name:
                testPaths.append(entry.name)
        testPaths.sort()
        return testPaths

    def get_latest_test_result_path(self, testName):
        testPaths = self.get_test_paths(testName)
        if testPaths:
            return os.path.join(self.squireFolder, testPaths[-1]) + "\\"
        else:
            return "Not found"

    def get_latest_test_result_folder(self, testName):
        testPaths = self.get_test_paths(testName)
        if testPaths:
            return testPaths[-1]
        else:
            return "Not found"


if __name__ == '__main__':
    directory = TestDirectory(TestSystems.Names.Squire1)
    print(directory.get_latest_test_result_path(Tests.Names.Drive))
    print(directory.get_latest_test_result_path(Tests.Names.Loop))
    print(directory.get_latest_test_result_path(Tests.Names.IVVR))
