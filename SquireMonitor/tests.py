# Copyright (c) 2018 Koninklijke Philips N.V.
from enum import Enum


class Tests:
    class Names(Enum):
        Drive = 1
        Loop = 2
        IVVR = 3
        IPISLIB = 4
        Reviewing = 5
        Tsm = 6
        Install = 7
        Nightbatch = 8
        Regressioncheck = 9

    squireTestSet = [Names.Drive,
                     Names.Loop,
                     Names.IVVR,
                     Names.IPISLIB,
                     Names.Reviewing,
                     Names.Tsm]

    continuousIntegrationTestSet = [Names.Install,
                                    Names.Nightbatch,
                                    Names.Regressioncheck]
