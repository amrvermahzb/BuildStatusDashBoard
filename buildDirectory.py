import os.path

BUILD_BASE_PATH = r'\\code1.emi.philips.com\storage\IGTS_WIP_Storage'
PRE_FIXES = {"CIBuild": "\CIBuilds\\", "Extended": "\ExtendedCIBuilds\\"}
POST_FIXES = {"CIBuild": "", "Extended": "_Coverage"}


class BuildDirectory:

    def __init__(self, unit_name, build_type):
        self.unit_name = unit_name
        self.build_type = build_type

    def get_build_path(self):
        build_path = BUILD_BASE_PATH + PRE_FIXES[self.build_type] + self.unit_name + r'\Allura_Main_' + self.unit_name + r'_PreInt' + POST_FIXES[self.build_type]
        if not os.path.isdir(build_path):
            build_path = "dir not found"
        return build_path

