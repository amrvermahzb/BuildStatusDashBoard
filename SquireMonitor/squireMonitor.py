from testSystem import TestSystem
from testSystemNames import TestSystemNames
from testSets import TestSets


class SquireMonitor:
	def __init__(self):
		self.testSystems = []
		self.testSystems.append(TestSystem(TestSystemNames.Squire1, TestSets.get_squire_test_set()))
		self.testSystems.append(TestSystem(TestSystemNames.Squire2, TestSets.get_squire_test_set()))
		self.testSystems.append(TestSystem(TestSystemNames.Squire3, TestSets.get_squire_test_set()))
		self.testSystems.append(TestSystem(TestSystemNames.Squire4, TestSets.get_squire_test_set()))
		self.testSystems.append(TestSystem(TestSystemNames.Squire5, TestSets.get_squire_test_set()))
		self.testSystems.append(TestSystem(TestSystemNames.Squire6, TestSets.get_squire_test_set()))
		self.testSystems.append(TestSystem(TestSystemNames.Squire7, TestSets.get_squire_test_set()))
		self.testSystems.append(TestSystem(TestSystemNames.Squire8, TestSets.get_squire_test_set()))
		self.testSystems.append(TestSystem(TestSystemNames.Squire9, TestSets.get_squire_test_set()))
		self.testSystems.append(TestSystem(TestSystemNames.BV2, TestSets.get_continuous_integration_test_set()))
