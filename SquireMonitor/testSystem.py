from testResult import TestResult
from testNames import TestNames
from testSystemNames import TestSystemNames

class TestSystem:
	def __init__(self, systemName):
		self.name = systemName
		self.testResults = []

	def update_results(self):
		self.testResults.clear()
		for testName in TestNames:
			self.testResults.append(TestResult(self.name, testName))
		
	
if __name__ == '__main__':
	testSystem = TestSystem(TestSystemNames.Squire1)
	testSystem.update_results()
	
	for result in testSystem.testResults:
		print(result.testName, result.get_latest_result(), result.get_latest_result_date())