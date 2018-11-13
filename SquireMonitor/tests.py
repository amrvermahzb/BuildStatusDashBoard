from enum import Enum


class Tests:
    class Names(Enum):
        Drive = 1
        Loop = 2
        IVVR = 3
        Install = 4
        Regression = 5

    squireTestSet = [Names.Drive,
                     Names.Loop,
                     Names.IVVR]

    continuousIntegrationTestSet = [Names.Install,
                                    Names.Regression]
