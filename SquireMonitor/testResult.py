from testDirectory import TestDirectory
from datetime import datetime
import os.path
import xml.etree.ElementTree as ET


class TestResult:
	def __init__(self, testSystem, testName):
		testDirectory = TestDirectory(testSystem)
		self.testName = testName
		self.resultPath = testDirectory.get_latest_test_result_path(testName)
		self.resultFile = os.path.join(self.resultPath, 'ip_subsystem_test_result.xml')
		self.dateTimeFormat = '%Y-%m-%d'
		
	def get_latest_result(self):
		if os.path.isfile(self.resultFile):
			root = ET.parse(self.resultFile).getroot()
			for child in root:
				if child.tag == "test-suite":
					return child.attrib['result']
		else:
			return "Not found"
				

	def is_overdue(self):
		latestResultDate = self.get_latest_result_date()
		now = datetime.now().strftime(self.dateTimeFormat)
		return datetime.strptime(latestResultDate, self.dateTimeFormat) < datetime.strptime(now, self.dateTimeFormat)
	
	
	def get_latest_result_date(self):
		return datetime.fromtimestamp(os.path.getctime(self.resultPath)).strftime(self.dateTimeFormat)
