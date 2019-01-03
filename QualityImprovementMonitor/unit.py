# Encapsulated build of unit used to update the dashboard

from stat import ST_CTIME
import os
import time
import datetime
from time import strftime
from warningSettingsReport import *
from buildWarningMetricsReport import *
from ticsMetricsReport import *

BUILD_BASE_PATH = r'\\code1.emi.philips.com\storage\IGTS_WIP_Storage\CIBuilds'


class Unit:

    def __init__(self, unit_name):
        self.unit_name = unit_name
        self.last_successful_build_path = "<nopath>"

    def get_latest_build_wrong_warning_level_count(self):
        report = self._get_latest_build_warning_setting_report()
        return report.get_wrong_warning_level_count()

    def get_latest_build_treat_warnings_not_as_errors_count(self):
        report = self._get_latest_build_warning_setting_report()
        return report.get_treat_warnings_not_as_errors_count()

    def get_latest_build_suppressed_warning_count(self):
        report = self._get_latest_build_warning_setting_report()
        return report.get_suppressed_warning_count()

    def get_latest_build_actual_warning_count(self):
        report = self._get_latest_build_actual_warnings_report()
        return report.get_build_warning_count()

    def get_latest_build_total_warning_count(self):
        return self.get_latest_build_actual_warning_count() + self.get_latest_build_suppressed_warning_count()

    def get_latest_build_coverity_error_count(self, level):
        report = TicsMetricsReport(self.unit_name)
        return report.get_coverity_errors(level)

    def get_latest_build_security_error_count(self, level):
        report = TicsMetricsReport(self.unit_name)
        return report.get_security_errors(level)

    def _get_latest_build_warning_setting_report(self):
        filename = self.last_successful_build_path + r'\Logging\GENERATE\warning_settings_report.xml'
        return WarningSettingsReport(filename)

    def _get_latest_build_actual_warnings_report(self):
        filename = self.last_successful_build_path + r'\Logging\GENERATE\Reports\VisualStudioBuildTotals.xml'
        return BuildWarningMetricsReport(filename)

    def update_path_last_successful_build(self):
        build_directory_root = self._get_build_directory_root()

        if build_directory_root == "dir not found":
            return "<nopath>"

        self.last_successful_build_path = "<nopath>"
        last_successful_build_date = 0

        for relative_build_dir in os.listdir(build_directory_root):
            absolute_build_dir = os.path.join(build_directory_root, relative_build_dir)
            build_date = self._get_build_date(absolute_build_dir)
            build_success = self._is_build_successful(absolute_build_dir)

            if build_success and build_date > last_successful_build_date:
                self.last_successful_build_path = absolute_build_dir

        print("get latest build unit=" + self.unit_name + " path=" + self.last_successful_build_path)
        return self.last_successful_build_path

    def _get_build_directory_root(self):
        stream_name = r'Allura_Main_' + self.unit_name + r'_PreInt'
        build_path = os.path.join(BUILD_BASE_PATH, self.unit_name, stream_name)
        if not os.path.isdir(build_path):
            build_path = "dir not found"
        return build_path

    def _get_build_date(self, build_dir):
        return os.stat(build_dir)[ST_CTIME]

    def _is_build_successful(self, build_dir):
        result = False

        filename = build_dir + r'\BuildInformation.xml'
        if os.path.isfile(filename):
            with open(filename) as f:
                content = f.readlines()

                for line in content:
                    if "overall-result" in line:
                        if "success" in line:
                            result = True
        return result
