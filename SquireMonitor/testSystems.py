# Copyright (c) 2018 Koninklijke Philips N.V.
from enum import Enum


class TestSystems:
    class Names(Enum):
        Squire1 = 1
        Squire2 = 2
        Squire3 = 3
        Squire4 = 4
        Squire5 = 5
        Squire6 = 6
        Squire7 = 7
        Squire8 = 8
        Squire9 = 9
        BV2 = 10

    squireSystems = [Names.Squire1,
                     Names.Squire2,
                     Names.Squire3,
                     Names.Squire4,
                     Names.Squire5,
                     Names.Squire6,
                     Names.Squire7,
                     Names.Squire8,
                     Names.Squire9]

    continuousIntegrationSystems = [Names.BV2]
