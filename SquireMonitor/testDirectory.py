import os.path
from os import scandir
from testNames import TestNames
from testSystemNames import TestSystemNames

BUILD_BASE_PATH = r'\\192.168.116.106\TestResults'
SQUIRE_FOLDERS = {TestSystemNames.Squire1: "\SQUIREIP-1\\", TestSystemNames.Squire2: "\SQUIREIP-2\\",
			      TestSystemNames.Squire3: "\SQUIREIP-3\\", TestSystemNames.Squire4: "\SQUIREIP-4\\",
				  TestSystemNames.Squire5: "\SQUIREIP-5\\", TestSystemNames.Squire6: "\SQUIREIP-6\\",
				  TestSystemNames.Squire7: "\SQUIREIP-7\\", TestSystemNames.Squire8: "\SQUIREIP-8H\\",
				  TestSystemNames.Squire9: "\SQUIREIP-9H\\"}
				  
TEST_POSTFIXES = {TestNames.Drive: "_DRIVE", TestNames.Loop: "_LOOP", TestNames.IVVR: "_IVVR"}


class TestDirectory:
	def __init__(self, squireName):
		self.squireFolder = BUILD_BASE_PATH + SQUIRE_FOLDERS[squireName]
		

	def get_latest_test_result_path(self, testName):
		testPaths = []
		for entry in os.scandir(self.squireFolder):
			if entry.is_dir() and TEST_POSTFIXES[testName] in entry.name:
				testPaths.append(entry.name)
		testPaths.sort()
		return os.path.join(self.squireFolder, testPaths[-1]) + "\\"


if __name__ == '__main__':
	directory = TestDirectory(TestSystemNames.Squire1)
	print(directory.get_latest_test_result_path(TestNames.Drive))
	print(directory.get_latest_test_result_path(TestNames.Loop))
	print(directory.get_latest_test_result_path(TestNames.IVVR))
	