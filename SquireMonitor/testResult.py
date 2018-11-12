from testDirectory import TestDirectory
from datetime import datetime
import os.path


class TestResult:
	def __init__(self, testSystem, testName):
		self.testDirectory = TestDirectory(testSystem)
		self.resultPath = self.testDirectory.get_latest_test_result_path(testName)
		self.testName = testName
		self.dateTimeFormat = '%Y-%m-%d'

	def get_latest_result(self):
		pass

	def is_overdue(self):
		latestResultDate = self.get_latest_result_date()
		now = datetime.now().strftime(self.dateTimeFormat)
		return datetime.strptime(latestResultDate, self.dateTimeFormat) < datetime.strptime(now, self.dateTimeFormat)
	
	def get_latest_result_date(self):
		return datetime.fromtimestamp(os.path.getctime(self.resultPath)).strftime(self.dateTimeFormat)
