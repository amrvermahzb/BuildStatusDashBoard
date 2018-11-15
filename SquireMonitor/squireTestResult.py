# Copyright (c) 2018 Koninklijke Philips N.V.
from testResult import TestResult
import os.path
import xml.etree.ElementTree as ET


class SquireTestResult(TestResult):
	def __init__(self, testSystem, testName):
		super().__init__(testSystem, testName)
		self.resultFile = os.path.join(self.resultPath, 'ip_subsystem_test_result.xml')
		
	def get_latest_result(self):
		if os.path.isfile(self.resultFile):
			root = ET.parse(self.resultFile).getroot()
			for child in root:
				if child.tag == "test-suite":
					return child.attrib['result']
			return "Not found"
		else:
			return "Not found"
