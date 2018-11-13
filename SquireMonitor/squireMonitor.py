from testSystem import TestSystem
from testSystems import TestSystems
from tests import Tests


class SquireMonitor:
	def __init__(self):
		self.testSystems = []

		for systemName in TestSystems.squireSystems:
			self.testSystems.append(TestSystem(systemName, Tests.squireTestSet))
		for systemName in TestSystems.continuousIntegrationSystems:
			self.testSystems.append(TestSystem(systemName, Tests.continuousIntegrationTestSet))
