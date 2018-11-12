from testNames import TestNames


class TestSets:
    @staticmethod
    def get_squire_test_set():
        return [TestNames.Drive, TestNames.Loop, TestNames.IVVR]

    @staticmethod
    def get_continuous_integration_test_set():
        return [TestNames.Install, TestNames.Regression]
