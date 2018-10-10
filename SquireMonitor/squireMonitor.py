from testSystem import TestSystem
from testSystemNames import TestSystemNames

class SquireMonitor:
	def __init__(self):
		self.testSystems = []
		self.testSystems.append(TestSystem(TestSystemNames.Squire1))
		self.testSystems.append(TestSystem(TestSystemNames.Squire2))
		self.testSystems.append(TestSystem(TestSystemNames.Squire3))
		self.testSystems.append(TestSystem(TestSystemNames.Squire4))
		self.testSystems.append(TestSystem(TestSystemNames.Squire5))
		self.testSystems.append(TestSystem(TestSystemNames.Squire6))
		self.testSystems.append(TestSystem(TestSystemNames.Squire7))
		self.testSystems.append(TestSystem(TestSystemNames.Squire8))
		self.testSystems.append(TestSystem(TestSystemNames.Squire9))