# Encapsulates warning setting history Excel report
# The report is updated with data from the warning settings report

import os
from openpyxl import *
from datetime import *


class QualityMetricsHistory:

    def __init__(self, unit_collection):
        self.unit_collection = unit_collection
        self.filename = r'QualityMetricsHistory.xlsx'
        self.worksheet_names = ["Wrong warning level", "Treat warning not as error", "Suppressed warnings", "Actual warnings", "Total warnings", "Coverity level 1", "Coverity level 2", "Security level 1", "Security level 2"]

        if not os.path.isfile(self.filename):
            self._create_workbook()

    def update(self):
        print("begin update history")

        date_format = "%d-%b-%Y"
        today = date.today()
        time_stamp = today.strftime(date_format)

        for unit in self.unit_collection.units:
            unit.update_path_last_successful_build()

        wb = load_workbook(self.filename)
        self._fill_worksheet_wrong_warning_level(wb.worksheets[0], time_stamp)
        self._fill_worksheet_treat_warnings_not_as_errors(wb.worksheets[1], time_stamp)
        self._fill_worksheet_suppressed_warnings(wb.worksheets[2], time_stamp)
        self._fill_worksheet_actual_warnings(wb.worksheets[3], time_stamp)
        self._fill_worksheet_total_warnings(wb.worksheets[4], time_stamp)
        self._fill_worksheet_coverity_warnings(wb.worksheets[5], time_stamp, 1)
        self._fill_worksheet_coverity_warnings(wb.worksheets[6], time_stamp, 2)
        self._fill_worksheet_security_warnings(wb.worksheets[7], time_stamp, 1)
        self._fill_worksheet_security_warnings(wb.worksheets[8], time_stamp, 2)

        wb.save(self.filename)

        print("end update history")

    def get_current_suppressed_warning_count(self):
        suppressed_warnings_for_all_units = 0

        for unit in self.unit_collection.units:
            suppressed_warnings_for_all_units += unit.get_latest_build_suppressed_warning_count()
        return suppressed_warnings_for_all_units

    def get_current_actual_warnings_count(self):
        actual_warnings_for_all_units = 0

        for unit in self.unit_collection.units:
            actual_warnings_for_all_units += unit.get_latest_build_actual_warning_count()
        return actual_warnings_for_all_units

    def get_current_total_warnings_count(self):
        total_warnings_for_all_units = 0

        for unit in self.unit_collection.units:
            total_warnings_for_all_units += unit.get_latest_build_total_warning_count()
        return total_warnings_for_all_units

    def get_values_wrong_warning_level(self):
        wb = load_workbook(self.filename)
        return self._get_values(wb.worksheets[0])

    def get_deltas_wrong_warning_level(self):
        wb = load_workbook(self.filename)
        return self._get_deltas(wb.worksheets[0])

    def get_values_treat_warnings_not_as_errors(self):
        wb = load_workbook(self.filename)
        return self._get_values(wb.worksheets[1])

    def get_deltas_treat_warnings_not_as_errors(self):
        wb = load_workbook(self.filename)
        return self._get_deltas(wb.worksheets[1])

    def get_values_suppressed_warnings(self):
        wb = load_workbook(self.filename)
        return self._get_values(wb.worksheets[2])

    def get_deltas_suppressed_warnings(self):
        wb = load_workbook(self.filename)
        return self._get_deltas(wb.worksheets[2])

    def get_values_actual_warnings(self):
        wb = load_workbook(self.filename)
        return self._get_values(wb.worksheets[3])

    def get_deltas_actual_warnings(self):
        wb = load_workbook(self.filename)
        return self._get_deltas(wb.worksheets[3])

    def get_history_total_warnings(self):
        wb = load_workbook(self.filename)
        return self._get_history(wb.worksheets[4])

    def get_values_coverity_level_1(self):
        wb = load_workbook(self.filename)
        return self._get_values(wb.worksheets[5])

    def get_deltas_coverity_level_1(self):
        wb = load_workbook(self.filename)
        return self._get_deltas(wb.worksheets[5])

    def get_history_coverity_level_1(self):
        wb = load_workbook(self.filename)
        return self._get_history(wb.worksheets[5])

    def get_values_coverity_level_2(self):
        wb = load_workbook(self.filename)
        return self._get_values(wb.worksheets[6])

    def get_deltas_coverity_level_2(self):
        wb = load_workbook(self.filename)
        return self._get_deltas(wb.worksheets[6])

    def get_values_security_level_1(self):
        wb = load_workbook(self.filename)
        return self._get_values(wb.worksheets[7])

    def get_deltas_security_level_1(self):
        wb = load_workbook(self.filename)
        return self._get_deltas(wb.worksheets[7])

    def get_history_security_level_1(self):
        wb = load_workbook(self.filename)
        return self._get_history(wb.worksheets[7])

    def get_values_security_level_2(self):
        wb = load_workbook(self.filename)
        return self._get_values(wb.worksheets[8])

    def get_deltas_security_level_2(self):
        wb = load_workbook(self.filename)
        return self._get_deltas(wb.worksheets[8])

    def _create_workbook(self):
        wb = Workbook()

        for index in range(9):
            if index != 0:
                wb.create_sheet()

            self._fill_worksheet_headers(wb.worksheets[index], self.worksheet_names[index])

        wb.save(self.filename)

    def _fill_worksheet_headers(self, worksheet, title):
        worksheet.title = title

        current_column = 1

        worksheet.cell(1, current_column).value = "Date"
        current_column += 1
        for unit in self.unit_collection.units:
            worksheet.cell(1, current_column).value = unit.unit_name
            current_column += 1
        worksheet.cell(1, current_column).value = "Total"

    def _fill_worksheet_wrong_warning_level(self, worksheet, time_stamp):
        count_for_all_units = []
        for unit in self.unit_collection.units:
            count_for_unit = unit.get_latest_build_wrong_warning_level_count()
            count_for_all_units.append(count_for_unit)
        self._fill_worksheet(worksheet, time_stamp, count_for_all_units)

    def _fill_worksheet_treat_warnings_not_as_errors(self, worksheet, time_stamp):
        count_for_all_units = []
        for unit in self.unit_collection.units:
            count_for_unit = unit.get_latest_build_treat_warnings_not_as_errors_count()
            count_for_all_units.append(count_for_unit)
        self._fill_worksheet(worksheet, time_stamp, count_for_all_units)

    def _fill_worksheet_suppressed_warnings(self, worksheet, time_stamp):
        count_for_all_units = []
        for unit in self.unit_collection.units:
            count_for_unit = unit.get_latest_build_suppressed_warning_count()
            count_for_all_units.append(count_for_unit)
        self._fill_worksheet(worksheet, time_stamp, count_for_all_units)

    def _fill_worksheet_actual_warnings(self, worksheet, time_stamp):
        count_for_all_units = []
        for unit in self.unit_collection.units:
            count_for_unit = unit.get_latest_build_actual_warning_count()
            count_for_all_units.append(count_for_unit)
        self._fill_worksheet(worksheet, time_stamp, count_for_all_units)

    def _fill_worksheet_total_warnings(self, worksheet, time_stamp):
        count_for_all_units = []
        for unit in self.unit_collection.units:
            count_for_unit = unit.get_latest_build_suppressed_warning_count() + \
                                  unit.get_latest_build_actual_warning_count()
            count_for_all_units.append(count_for_unit)
        self._fill_worksheet(worksheet, time_stamp, count_for_all_units)

    def _fill_worksheet_coverity_warnings(self, worksheet, time_stamp, level):
        count_for_all_units = []
        for unit in self.unit_collection.units:
            count_for_unit = unit.get_latest_build_coverity_error_count(level)
            count_for_all_units.append(count_for_unit)

        self._fill_worksheet(worksheet, time_stamp, count_for_all_units)

    def _fill_worksheet_security_warnings(self, worksheet, time_stamp, level):
        count_for_all_units = []
        for unit in self.unit_collection.units:
            count_for_unit = unit.get_latest_build_security_error_count(level)
            count_for_all_units.append(count_for_unit)

        self._fill_worksheet(worksheet, time_stamp, count_for_all_units)

    def _fill_worksheet(self, worksheet, time_stamp, count_for_all_units):
        current_column = 1
        current_row = worksheet.max_row

        last_time_stamp = worksheet.cell(current_row, 1).value
        if not last_time_stamp == time_stamp:
            current_row += 1

        total = 0
        worksheet.cell(current_row, current_column).value = time_stamp
        current_column += 1
        for count in count_for_all_units:
            total += count
            worksheet.cell(current_row, current_column).value = count
            current_column += 1
        worksheet.cell(current_row, current_column).value = total

    def _get_values(self, worksheet):
        values = []
        current_row = worksheet.max_row

        for index in range(len(self.unit_collection.units)+1):
            current_column = index + 2
            actual_value = worksheet.cell(current_row, current_column).value
            values.append(actual_value)
            current_column += 1
        return values

    def _get_deltas(self, worksheet):
        deltas = []
        current_row = worksheet.max_row

        for index in range(len(self.unit_collection.units)+1):
            current_column = index + 2
            actual_value = worksheet.cell(current_row, current_column).value
            if current_row > 2:
                previous_value = worksheet.cell(current_row - 1, current_column).value
                deltas.append(actual_value - previous_value)
            else:
                deltas.append(0)
        return deltas

    def _get_history(self, worksheet):
        totals = {}
        date_column = 1
        totals_column = len(self.unit_collection.units) + 2

        for current_row in range(2, worksheet.max_row):
            date = worksheet.cell(current_row, date_column).value
            total = worksheet.cell(current_row, totals_column).value
            totals[date] = total
        return totals