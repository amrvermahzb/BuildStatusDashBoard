from stat import ST_CTIME
import os
import time
from time import strftime

BUILD_BASE_PATH = r'\\code1.emi.philips.com\storage\IGTS_WIP_Storage'


def latest_unit_build_info(unit):
    path_ci = build_path(unit, "\CIBuilds\\")
    path_ext = build_path(unit, "\ExtendedCIBuilds\\", "_Coverage")
    return latest_build_date_and_path(path_ci), \
           latest_build_date_and_path(path_ext)


def build_path(unit, build_type, post_fix=""):
    base_path = BUILD_BASE_PATH + build_type + unit + r'\Allura_Win10_' + unit
    path = base_path + r'_PreInt' + post_fix
    if not os.path.isdir(path):
        path = base_path + r'_Int' + post_fix
        if not os.path.isdir(path):
            path = "dir not found"
    return path


def latest_build_date_and_path(dir_path):
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
