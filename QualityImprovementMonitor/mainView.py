from tkinter import *
from tkinter.ttk import *
from warningSettingsHistory import *
from unitCollection import *
from unit import *
from datetime import datetime
import pandas as panda
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


class MainView:

    def __init__(self):
        # initialize user interface
        self.root = Tk()
        # self.root.attributes("-fullscreen", True)

        # data
        self.unit_collection = UnitCollection()
        self.warning_settings_history = WarningSettingsHistory(self.unit_collection)

        # define fonts
        self.large_font_bold = "Verdana 30 bold"
        self.large_font = "Verdana 30"
        self.medium_font_bold = "Verdana 17 bold"
        self.medium_font = "Verdana 17"
        self.small_font_bold = "Verdana 11 bold"
        self.small_font = "Verdana 11"
        self.extra_small_font = "Verdana 7"
        self.bg = "white"

        # define styles
        self.title_style = Style()
        self.title_style.configure("Background.TLabel", background="white")

        self.title_style = Style()
        self.title_style.configure("Title.TLabel", foreground="black", background="white", font=self.large_font_bold)

        self.image_style = Style()
        self.image_style.configure("Image.TLabel", borderwidth=0, highlightthickness=0)

        self.table_row_header_style = Style()
        self.table_row_header_style.configure("TableRowHeader.TLabel", foreground="black", background="white", font=self.small_font, width=25, anchor=W, border=1)

        self.table_column_header_style = Style()
        self.table_column_header_style.configure("TableColumnHeader.TLabel", foreground="black", background="white", font=self.small_font_bold, width=8, anchor=CENTER, border=1)

        self.table_cell_value_up_style = Style()
        self.table_cell_value_up_style.configure("TableCellValueUp.TLabel", foreground="white", background="red", font=self.small_font, width=8, anchor=CENTER, border=1)

        self.table_cell_value_down_style = Style()
        self.table_cell_value_down_style.configure("TableCellValueDown.TLabel", foreground="white", background="green", font=self.small_font, width=8, anchor=CENTER, border=1)

        self.table_cell_value_unchanged_style = Style()
        self.table_cell_value_unchanged_style.configure("TableCellValueUnchanged.TLabel", foreground="gray", background="white", font=self.extra_small_font, width=8, anchor=CENTER, border=1)

        print("begin layout ui")

        # define user interface layout
        self.root.configure(bg=self.bg)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry('%sx%s' % (screen_width, screen_height))

        label_content = Label(self.root, style="Background.TLabel")
        label_content.grid(rowspan=4, columnspan=3)
        #label_content.configure(width=screen_width, height=screen_height)

        # Title
        label_title = Label(label_content, text="Allura quality improvement dashboard", style="Title.TLabel")
        label_title.grid(row=1, column=1, columnspan=3)

        # Burndown charts
        self.filename_warning_burndown_graph = "WarningBurndown.png"
        self.image_warning_burndown_graph = PhotoImage(file=self.filename_warning_burndown_graph)
        label_warning_burndown_graph = Label(label_content, image=self.image_warning_burndown_graph, style="Image.TLabel")
        label_warning_burndown_graph.grid(row=2, column=1)

        self.filename_coverity_burndown_graph = "CoverityBurndown.png"
        self.image_coverity_burndown_graph = PhotoImage(file=self.filename_coverity_burndown_graph)
        label_coverity_burndown_graph = Label(label_content, image=self.image_coverity_burndown_graph, style="Image.TLabel")
        label_coverity_burndown_graph.grid(row=2, column=2)

        self.filename_security_burndown_graph = "SecurityBurndown.png"
        self.image_security_burndown_graph = PhotoImage(file=self.filename_security_burndown_graph)
        label_security_burndown_graph = Label(label_content, image=self.image_security_burndown_graph, style="Image.TLabel")
        label_security_burndown_graph.grid(row=2, column=3)

        # Warning info details
        label_table = Label(label_content, style="Background.TLabel")
        label_table.grid(row=4, column=1, columnspan=3)

        label_table_row_header_1 = Label(label_table, text="Wrong warning level", style="TableRowHeader.TLabel")
        label_table_row_header_1.grid(row=2, column=1)
        label_table_row_header_1 = Label(label_table, text="Treat warnings not as errors", style="TableRowHeader.TLabel")
        label_table_row_header_1.grid(row=3, column=1)
        label_table_row_header_2 = Label(label_table, text="Suppressed warnings", style="TableRowHeader.TLabel")
        label_table_row_header_2.grid(row=4, column=1)
        label_table_row_header_3 = Label(label_table, text="Actual warnings", style="TableRowHeader.TLabel")
        label_table_row_header_3.grid(row=5, column=1)
        label_table_row_header_3 = Label(label_table, text="Coverity level 1", style="TableRowHeader.TLabel")
        label_table_row_header_3.grid(row=6, column=1)
        label_table_row_header_3 = Label(label_table, text="Coverity level 2", style="TableRowHeader.TLabel")
        label_table_row_header_3.grid(row=7, column=1)
        label_table_row_header_3 = Label(label_table, text="Security level 1", style="TableRowHeader.TLabel")
        label_table_row_header_3.grid(row=8, column=1)
        label_table_row_header_3 = Label(label_table, text="Security level 2", style="TableRowHeader.TLabel")
        label_table_row_header_3.grid(row=9, column=1)

        current_column = 2

        self.labels_wrong_warning_level_data = []
        self.labels_treat_warnings_not_as_errors_data = []
        self.labels_suppressed_warnings_data = []
        self.labels_actual_warnings_data = []
        self.labels_coverity_level_1_data = []
        self.labels_coverity_level_2_data = []
        self.labels_security_level_1_data = []
        self.labels_security_level_2_data = []

        for index in range(len(self.unit_collection.units) + 1):
            label_table_column_header = Label(label_table, style="TableColumnHeader.TLabel")
            label_table_column_header.grid(row=1, column=current_column)

            if index < len(self.unit_collection.units):
                label_table_column_header.configure(text=self.unit_collection.units[index].unit_name)
            else:
                label_table_column_header.configure(text="Total")

            # wrong warning level
            label_wrong_warning_level_data = Label(label_table, text="0", style="TableCellValueUnchanged.TLabel")
            label_wrong_warning_level_data.grid(row=2, column=current_column)
            self.labels_wrong_warning_level_data.append(label_wrong_warning_level_data)

            # treat warnings not as errors
            label_treat_warnings_not_as_errors_data = Label(label_table, text="0", style="TableCellValueUnchanged.TLabel")
            label_treat_warnings_not_as_errors_data.grid(row=3, column=current_column)
            self.labels_treat_warnings_not_as_errors_data.append(label_treat_warnings_not_as_errors_data)

            # suppressed warnings
            label_suppressed_warnings_data = Label(label_table, text="0", style="TableCellValueUnchanged.TLabel")
            label_suppressed_warnings_data.grid(row=4, column=current_column)
            self.labels_suppressed_warnings_data.append(label_suppressed_warnings_data)

            # actual warnings
            label_actual_warnings_data = Label(label_table, text="0", style="TableCellValueUnchanged.TLabel")
            label_actual_warnings_data.grid(row=5, column=current_column)
            self.labels_actual_warnings_data.append(label_actual_warnings_data)

            # coverity level 1
            label_coverity_level_1_data = Label(label_table, text="0", style="TableCellValueUnchanged.TLabel")
            label_coverity_level_1_data.grid(row=6, column=current_column)
            self.labels_coverity_level_1_data.append(label_coverity_level_1_data)

            # coverity level 2
            self.label_coverity_level_2_data = Label(label_table, text="0", style="TableCellValueUnchanged.TLabel")
            self.label_coverity_level_2_data.grid(row=7, column=current_column)
            self.labels_coverity_level_2_data.append(self.label_coverity_level_2_data)

            # security level 1
            label_security_level_1_data = Label(label_table, text="0", style="TableCellValueUnchanged.TLabel")
            label_security_level_1_data.grid(row=8, column=current_column)
            self.labels_security_level_1_data.append(label_security_level_1_data)

            # security level 2
            self.label_security_level_2_data = Label(label_table, text="0", style="TableCellValueUnchanged.TLabel")
            self.label_security_level_2_data.grid(row=9, column=current_column)
            self.labels_security_level_2_data.append(self.label_security_level_2_data)

            current_column += 1

        print("end layout ui")

        self._update()
        self.root.mainloop()

    def _update_history_file(self):
        self.warning_settings_history.update()
        return

    def _update_user_interface(self):
        print("begin update ui")
        date_format = "%d-%b-%Y"
        day1 = datetime.strptime('12-Sep-2017', date_format)
        day2 = datetime.strptime('02-Jul-2019', date_format)

        worksheet_name = self.warning_settings_history.worksheet_names[4]
        self._generate_burn_down_chart(worksheet_name, day1, day2, 6600, 0, 0, 8000, 500, self.filename_warning_burndown_graph)
        self.image_warning_burndown_graph.configure(file=self.filename_warning_burndown_graph)

        worksheet_name = self.warning_settings_history.worksheet_names[5]
        self._generate_burn_down_chart(worksheet_name, day1, day2, 546, 0, 0, 600, 100, self.filename_coverity_burndown_graph)
        self.image_coverity_burndown_graph.configure(file=self.filename_coverity_burndown_graph)

        worksheet_name = self.warning_settings_history.worksheet_names[7]
        self._generate_burn_down_chart(worksheet_name, day1, day2, 2260, 0, 0, 2500, 500, self.filename_security_burndown_graph)
        self.image_security_burndown_graph.configure(file=self.filename_security_burndown_graph)

        for index in range(len(self.unit_collection.units) + 1):
            value = self.warning_settings_history.get_values_wrong_warning_level()[index]
            delta = self.warning_settings_history.get_deltas_wrong_warning_level()[index]
            self._update_table_label(self.labels_wrong_warning_level_data[index], value, delta)

            value = self.warning_settings_history.get_values_treat_warnings_not_as_errors()[index]
            delta = self.warning_settings_history.get_deltas_treat_warnings_not_as_errors()[index]
            self._update_table_label(self.labels_treat_warnings_not_as_errors_data[index], value, delta)

            value = self.warning_settings_history.get_values_suppressed_warnings()[index]
            delta = self.warning_settings_history.get_deltas_suppressed_warnings()[index]
            self._update_table_label(self.labels_suppressed_warnings_data[index], value, delta)

            value = self.warning_settings_history.get_values_actual_warnings()[index]
            delta = self.warning_settings_history.get_deltas_actual_warnings()[index]
            self._update_table_label(self.labels_actual_warnings_data[index], value, delta)

            value = self.warning_settings_history.get_values_coverity_level_1()[index]
            delta = self.warning_settings_history.get_deltas_coverity_level_1()[index]
            self._update_table_label(self.labels_coverity_level_1_data[index], value, delta)

            value = self.warning_settings_history.get_values_coverity_level_2()[index]
            delta = self.warning_settings_history.get_deltas_coverity_level_2()[index]
            self._update_table_label(self.labels_coverity_level_2_data[index], value, delta)

            value = self.warning_settings_history.get_values_security_level_1()[index]
            delta = self.warning_settings_history.get_deltas_security_level_1()[index]
            self._update_table_label(self.labels_security_level_1_data[index], value, delta)

            value = self.warning_settings_history.get_values_security_level_2()[index]
            delta = self.warning_settings_history.get_deltas_security_level_2()[index]
            self._update_table_label(self.labels_security_level_2_data[index], value, delta)

        print("end update ui")

        return

    def _update_table_label(self, label, value, delta):
        style = "TableCellValueUnchanged.TLabel"
        if delta < 0:
            style = "TableCellValueDown.TLabel"
        if delta > 0:
            style = "TableCellValueUp.TLabel"
        label.configure(style=style)
        label.configure(text=str(value))
        if delta != 0:
            label.configure(text=str(delta))

    def _generate_burn_down_chart(self, worksheet_name, begin_date, end_date, burn_down_begin_y, burn_down_end_y, min_y, max_y, step_y, graph_filename):
        plt.clf()

        # set date range
        plt.xlim(begin_date, end_date)

        # read excel and plot data
        data_frame = panda.ExcelFile(self.warning_settings_history.filename).parse(worksheet_name)
        df = panda.DataFrame(
            {'x': data_frame['Date'],
             'Total': data_frame['Total']})
        for column in df.drop('x', axis=1):
            plt.plot(df['x'], df[column], label=column)

        # plot burndown
        plt.plot([begin_date, end_date], [burn_down_begin_y, burn_down_end_y], '--r', label="Burndown")

        # plot labels
        plt.xlabel('Date')
        plt.ylabel(worksheet_name)
        plt.title(worksheet_name + ' burndown')

        # plot ticks
        years = mdates.YearLocator()  # every year
        months = mdates.MonthLocator()  # every month
        years_fmt = mdates.DateFormatter('%Y')
        plt.gca().xaxis.set_major_locator(years)
        plt.gca().xaxis.set_major_formatter(years_fmt)
        plt.gca().xaxis.set_minor_locator(months)
        plt.yticks(np.arange(min_y, max_y, step=step_y))

        # plot legend
        #plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=None)

        # plot grid
        # plt.grid(True)
        # plt.grid(linewidth='0.5', color='black')
        # plt.tight_layout()

        # save image
        plt.savefig(graph_filename, bbox_inches='tight', dpi=100)


    def _update(self):
        now = time.strftime("(snapshot %A %B %d %H:%M:%S)")
        self.root.title("Allura R8.x.100 Warning Settings Monitor v1.0  " + now)

        self._update_history_file()
        self._update_user_interface()

        # refresh only once every 5 minutes
        self.root.after(300000, self._update)


mainView = MainView()
