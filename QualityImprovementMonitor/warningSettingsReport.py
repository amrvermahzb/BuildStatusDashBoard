# Encapsulates warning setting XML report

import os
import xml.etree.ElementTree as ET


class WarningSettingsReport:

    def __init__(self, filename):
        self.project_files_with_wrong_warning_level = 0
        self.project_files_which_treat_warnings_not_as_errors = 0
        self.project_files_with_disabled_warning_catagories = 0
        self.project_files_with_disabled_warnings = 0
        self.source_files_with_wrong_warning_level = 0
        self.source_files_with_disabled_warnings = 0
        self.source_files_with_deprecated_code = 0

        if os.path.isfile(filename):
            tree = ET.parse(filename)
            root = tree.getroot()

            attribute_name = "errors"
            element = root.find("{urn:dsi-schema}ProjectFilesWithWrongWarningLevel")
            self.project_files_with_wrong_warning_level = int(element.attrib[attribute_name])

            element = root.find("{urn:dsi-schema}ProjectFilesWhichTreatWarningsNotAsErrors")
            self.project_files_which_treat_warnings_not_as_errors = int(element.attrib[attribute_name])

            element = root.find("{urn:dsi-schema}ProjectFilesWithDisabledWarningCatagories")
            self.project_files_with_disabled_warning_catagories = int(element.attrib[attribute_name])

            element = root.find("{urn:dsi-schema}ProjectFilesWithDisabledWarnings")
            self.project_files_with_disabled_warnings = int(element.attrib[attribute_name])

            element = root.find("{urn:dsi-schema}SourceFilesWithWrongWarningLevel")
            self.source_files_with_wrong_warning_level = int(element.attrib[attribute_name])

            element = root.find("{urn:dsi-schema}SourceFilesWithDisabledWarnings")
            self.source_files_with_disabled_warnings = int(element.attrib[attribute_name])

            element = root.find("{urn:dsi-schema}SourceFilesWithDeprecatedCode")
            self.source_files_with_deprecated_code = int(element.attrib[attribute_name])

    def get_wrong_warning_level_count(self):
        return self.project_files_with_wrong_warning_level + \
               self.source_files_with_wrong_warning_level

    def get_treat_warnings_not_as_errors_count(self):
        return self.project_files_which_treat_warnings_not_as_errors

    def get_suppressed_warning_count(self):
        return self.project_files_with_disabled_warning_catagories + \
               self.project_files_with_disabled_warnings + \
               self.source_files_with_disabled_warnings + \
               self.source_files_with_deprecated_code

    def get_deprecated_code_count(self):
        return self.source_files_with_deprecated_code



