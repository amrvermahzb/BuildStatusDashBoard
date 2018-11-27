# Copyright (c) 2018 Koninklijke Philips N.V.
from enum import Enum


class Tests:
    class Names(Enum):
        Drive = 1
        Loop = 2
        IVVR = 3
        IPISLIB = 4
        Reviewing = 5
        Install = 6
        Nightbatch = 7
        Regressioncheck = 8

    squireTestSet = [Names.Drive,
                     Names.Loop,
                     Names.IVVR,
                     Names.IPISLIB,
                     Names.Reviewing]

    continuousIntegrationTestSet = [Names.Install,
                                    Names.Nightbatch,
                                    Names.Regressioncheck]
