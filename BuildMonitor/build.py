from stat import ST_CTIME
import os
import time
from time import strftime
from buildDirectory import *


class Build:

    def __init__(self, unit_name, build_type):
        self.unit_name = unit_name
        self.build_type = build_type
        self.build_dir = BuildDirectory(unit_name, build_type)

    def get_latest_build_date_and_path(self):
        dir_path = self.build_dir.get_build_path()

        if dir_path == "dir not found":
            return "<nodate>", "<nopath>"

        # get all entries in the directory w/ stats
        entries = (os.path.join(dir_path, fn) for fn in os.listdir(dir_path))
        entries = ((os.stat(path), path) for path in entries)

        # leave only regular files, insert creation date
        entries = ((stat[ST_CTIME], path)
                   for stat, path in entries)
        # NOTE: on Windows `ST_CTIME` is a creation date
        #  but on Unix it could be something else
        # NOTE: use `ST_MTIME` to sort by a modification date
        entry = sorted(entries)[-1]
        return strftime("%Y-%m-%d", time.strptime(time.ctime(entry[0]))), entry[1]

    def get_build_log_file(self):
        return self.get_latest_build_date_and_path()[1] + r'\BuildInformation.xml'

    def get_latest_build_date(self):
        return self.get_latest_build_date_and_path()[0]

    def get_latest_build_result(self):
        filename = self.get_build_log_file()

        result = "failed"
        if os.path.exists(filename):
            with open(filename) as f:
                content = f.readlines()

            for line in content:
                if "overall-result" in line:
                    if "success" in line:
                        result = "successful"

        return result

