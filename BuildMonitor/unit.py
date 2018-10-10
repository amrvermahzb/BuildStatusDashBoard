from build import *

# Build types defined in build order
build_types = "CIBuild", "Extended"


class Unit:

    def __init__(self, unit_name):
        self.unit_name = unit_name
        self.builds = []

        for build_type in build_types:
            # Build types appended in build order
            self.builds.append(Build(unit_name, build_type))