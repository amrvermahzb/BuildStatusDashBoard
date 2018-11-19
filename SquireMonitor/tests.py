# Copyright (c) 2018 Koninklijke Philips N.V.
from enum import Enum


class Tests:
    class Names(Enum):
        Drive = 1
        Loop = 2
        IVVR = 3
        Install = 4
        Nightbatch = 5
        Regressioncheck = 6

    squireTestSet = [Names.Drive,
                     Names.Loop,
                     Names.IVVR]

    continuousIntegrationTestSet = [Names.Install,
                                    Names.Nightbatch,
                                    Names.Regressioncheck]
