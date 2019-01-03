# Encapsulates warning setting XML report

import os
import xml.etree.ElementTree as ET


class BuildWarningMetricsReport:

    def __init__(self, filename):
        self.warning_count = 0

        if os.path.isfile(filename):
            tree = ET.parse(filename)
            root = tree.getroot()
            for solution in root.findall('visualstudio-results/solution'):
                self.warning_count += int(solution.attrib["warnings"])

    def get_build_warning_count(self):
        return self.warning_count
