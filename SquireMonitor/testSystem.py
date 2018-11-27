# Copyright (c) 2018 Koninklijke Philips N.V.
from squireTestResult import SquireTestResult
from continuousIntegrationTestResult import ContinuousIntegrationTestResult
from reviewingTestResult import ReviewingTestResult
from ipislibTestResult import IpislibTestResult
from tests import Tests
from testSystems import TestSystems


class TestSystem:
    def __init__(self, systemName, testSet):
        self.name = systemName
        self.testResults = []
        self.testSet = testSet

    def update_results(self):
        self.testResults.clear()
        for testName in self.testSet:
            if self.is_squire_system(self.name):
                if testName == Tests.Names.Reviewing:
                    self.testResults.append(ReviewingTestResult(self.name, testName))
                elif testName == Tests.Names.IPISLIB:
                    self.testResults.append(IpislibTestResult(self.name, testName))
                else:
                    self.testResults.append(SquireTestResult(self.name, testName))
            else:
                self.testResults.append(ContinuousIntegrationTestResult(self.name, testName))

    @staticmethod
    def is_squire_system(systemName):
        return systemName in TestSystems.squireSystems


if __name__ == '__main__':
    testSystem = TestSystem(TestSystems.Names.Squire1)
    testSystem.update_results()

    for result in testSystem.testResults:
        print(result.testName, result.get_latest_result(), result.get_latest_result_date())
