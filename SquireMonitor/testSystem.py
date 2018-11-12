from squireTestResult import SquireTestResult
from nonSquireTestResult import NonSquireTestResult
from testNames import TestNames
from testSystemNames import TestSystemNames


class TestSystem:
    def __init__(self, systemName, testSet):
        self.name = systemName
        self.testResults = []
        self.testSet = testSet

    def update_results(self):
        self.testResults.clear()
        for testName in self.testSet:
            if self.is_squire_system(self.name):
                self.testResults.append(SquireTestResult(self.name, testName))
            else:
                self.testResults.append(NonSquireTestResult(self.name, testName))

    @staticmethod
    def is_squire_system(systemName):
        return (systemName == TestSystemNames.Squire1 or
                systemName == TestSystemNames.Squire2 or
                systemName == TestSystemNames.Squire3 or
                systemName == TestSystemNames.Squire4 or
                systemName == TestSystemNames.Squire5 or
                systemName == TestSystemNames.Squire6 or
                systemName == TestSystemNames.Squire7 or
                systemName == TestSystemNames.Squire8 or
                systemName == TestSystemNames.Squire9)


if __name__ == '__main__':
    testSystem = TestSystem(TestSystemNames.Squire1)
    testSystem.update_results()

    for result in testSystem.testResults:
        print(result.testName, result.get_latest_result(), result.get_latest_result_date())
