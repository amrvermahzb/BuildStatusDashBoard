from tkinter import *
from tkinter.ttk import *
from qualityMetricsHistory import *
from unitCollection import *
from unit import *
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from configparser import ConfigParser 
from matplotlib.ticker import NullFormatter
from matplotlib.dates import MonthLocator, DateFormatter


class MainView:

    def __init__(self):
        # initialize user interface
        self.root = Tk()
        # self.root.attributes("-fullscreen", True)

        # data
        self.unit_collection = UnitCollection()
        self.qualityMetricsHistory = QualityMetricsHistory(self.unit_collection)

        # define begin date range
        self.chart_begin_date = '1-Dec-2020'
        self.chart_end_date = '31-Dec-2021'

        # define fonts
        self.large_font_bold = "Verdana 30 bold"
        self.large_font = "Verdana 30"
        self.medium_font_bold = "Verdana 17 bold"
        self.medium_font = "Verdana 17"
        self.small_font_bold = "Verdana 11 bold"
        self.small_font = "Verdana 8"
        self.extra_small_font = "Verdana 7"
        self.bg = "white"

        # define styles
        self.title_style = Style()
        self.title_style.configure("Background.TLabel", background="white")

        self.title_style = Style()
        self.title_style.configure("Title.TLabel", foreground="black", background="white", font=self.large_font_bold)

        self.image_style = Style()
        self.image_style.configure("Image.TLabel", background="white")

        self.title_style = Style()
        self.title_style.configure("Table.TLabel", background="white")

        self.table_row_header_style = Style()
        self.table_row_header_style.configure("TableRowHeader.TLabel", foreground="black", background="white", font=self.small_font, width=24, anchor=W, border=1)

        self.table_column_header_style = Style()
        self.table_column_header_style.configure("TableColumnHeader.TLabel", foreground="black", background="white", font=self.small_font_bold, width=6, anchor=W, border=1)

        self.table_cell_value_up_style = Style()
        self.table_cell_value_up_style.configure("TableCellValueUp.TLabel", foreground="white", background="red", font=self.small_font, width=8, anchor=W, border=1)

        self.table_cell_value_down_style = Style()
        self.table_cell_value_down_style.configure("TableCellValueDown.TLabel", foreground="white", background="green", font=self.small_font, width=8, anchor=W, border=1)

        self.table_cell_value_unchanged_style = Style()
        self.table_cell_value_unchanged_style.configure("TableCellValueUnchanged.TLabel", foreground="gray", background="white", font=self.extra_small_font, width=6, anchor=W, border=1)

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
        label_table = Label(label_content, style="Table.TLabel")
        label_table.grid(row=4, column=1, columnspan=3, pady=50)
        
        ###############  lets make the ui display customizable #####################
        configur = ConfigParser()
        configur.read('config.ini')
        self.trend_graph_param_list=[]
        no_of_trend_graph=int (configur.get('TrendParam','count') )
        if(no_of_trend_graph>3):
          no_of_trend_graph=3
        for i in range(no_of_trend_graph):
            self.trend_graph_param_list.append(configur.get('TrendParam','par'+str(i+1) ) )
        print('**********************************')
        print(self.trend_graph_param_list)
        print('**********************************')
        
        param_count=int (configur.get('DisplayParam','Number_of_param') )
        
        self.param_list=[];
        for i in range (param_count):
            self.param_list.append(configur.get('DisplayParam','par'+str(i+1) ) )
        #print(' list has ',self.param_list)
        
        r=2
        for value in self.param_list:
            label_table_row_header_1 = Label(label_table, text=value , style="TableRowHeader.TLabel") #text="Treat warnings not as errors" 
            label_table_row_header_1.grid(row=r, column=0)
            r=r+1;
            
       
        self.table_row_header_to_data_levels={}
        for value in self.param_list:
             self.table_row_header_to_data_levels[value]=[]
             
        col=1
        for index in range(len(self.unit_collection.units) + 1):
            label_table_column_header = Label(label_table, style="TableColumnHeader.TLabel")
            label_table_column_header.grid(row=1, column=col)
            if index < len(self.unit_collection.units):
                label_table_column_header.configure(text=self.unit_collection.units[index].unit_name)
            else:
                label_table_column_header.configure(text="Total")
            col=col+1
        
        currow=1
        for value in self.param_list:
            curcol=0
            currow=currow+1
            for index in range(len(self.unit_collection.units) + 1):
                curcol=curcol+1;
                label_for_today_data_to_display = Label(label_table, text="0", style="TableCellValueUnchanged.TLabel")
                label_for_today_data_to_display.grid(row=currow, column=curcol,padx=3,pady=3)
                self.table_row_header_to_data_levels[value].append(label_for_today_data_to_display)
            
        ######################################################################
        '''
        par1=configur.get('DisplayParam','par1')
        label_table_row_header_1 = Label(label_table, text=par1 , style="TableRowHeader.TLabel") #text="Treat warnings not as errors" 
        label_table_row_header_1.grid(row=2, column=1)
        
        par2=configur.get('DisplayParam','par2')
        label_table_row_header_1 = Label(label_table, text=par2 , style="TableRowHeader.TLabel")      #text="Wrong warning level"
        label_table_row_header_1.grid(row=3, column=1)
        
        par3=configur.get('DisplayParam','par3')
        label_table_row_header_2 = Label(label_table, text=par3 , style="TableRowHeader.TLabel")      #tet="Suppressed warnings"
        label_table_row_header_2.grid(row=4, column=1)
        
        par4=configur.get('DisplayParam','par4')
        label_table_row_header_3 = Label(label_table, text=par4 , style="TableRowHeader.TLabel")      #text="Actual warnings" 
        label_table_row_header_3.grid(row=5, column=1)
         
        #Amr label_table_row_header_3 = Label(label_table, style="TableRowHeader.TLabel")
        #Amr label_table_row_header_3.grid(row=6, column=1)
        
        par5=configur.get('DisplayParam','par5')
        label_table_row_header_3 = Label(label_table, text=par5 , style="TableRowHeader.TLabel")      #text="Coverity level 1"
        label_table_row_header_3.grid(row=6, column=1)
        par6=configur.get('DisplayParam','par6')
        label_table_row_header_3 = Label(label_table, text=par6 , style="TableRowHeader.TLabel")      #text="Coverity level 2"
        label_table_row_header_3.grid(row=7, column=1)

        label_table_row_header_3 = Label(label_table, style="TableRowHeader.TLabel")
        label_table_row_header_3.grid(row=9, column=1)
        
        par7=configur.get('DisplayParam','par7')
        label_table_row_header_3 = Label(label_table, text=par7, style="TableRowHeader.TLabel")      #text= "Security level 1" 
        label_table_row_header_3.grid(row=8, column=1)
        
        par8=configur.get('DisplayParam','par8')
        label_table_row_header_3 = Label(label_table, text=par8 , style="TableRowHeader.TLabel")     #text="Security level 2" 
        label_table_row_header_3.grid(row=9, column=1)
        
        par9=configur.get('DisplayParam','par9')
        label_table_row_header_3 = Label(label_table, text=par9 , style="TableRowHeader.TLabel")     #text="TQI" 
        label_table_row_header_3.grid(row=10, column=1)
        
        
        
                
        current_column = 2    
        self.labels_wrong_warning_level_data = []
        self.labels_treat_warnings_not_as_errors_data = []
        self.labels_suppressed_warnings_data = []
        self.labels_actual_warnings_data = []
        self.labels_coverity_level_1_data = []
        self.labels_coverity_level_2_data = []
        self.labels_security_level_1_data = []
        self.labels_security_level_2_data = []
        self.labels_TQI_data = []

        for index in range(len(self.unit_collection.units) + 1):
            label_table_column_header = Label(label_table, style="TableColumnHeader.TLabel")
            label_table_column_header.grid(row=1, column=current_column)

            if index < len(self.unit_collection.units):
                label_table_column_header.configure(text=self.unit_collection.units[index].unit_name)
            else:
                label_table_column_header.configure(text="Total")

            # treat warnings not as errors
            label_treat_warnings_not_as_errors_data = Label(label_table, text="0", style="TableCellValueUnchanged.TLabel")
            label_treat_warnings_not_as_errors_data.grid(row=2, column=current_column)
            self.labels_treat_warnings_not_as_errors_data.append(label_treat_warnings_not_as_errors_data)

            # wrong warning level
            label_wrong_warning_level_data = Label(label_table, text="0", style="TableCellValueUnchanged.TLabel")
            label_wrong_warning_level_data.grid(row=3, column=current_column)
            self.labels_wrong_warning_level_data.append(label_wrong_warning_level_data)

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
            
            # TQI
            self.label_TQI_data=Label(label_table, text="0", style="TableCellValueUnchanged.TLabel")
            self.label_TQI_data.grid(row=10,column=current_column)
            self.labels_TQI_data.append(self.label_TQI_data)
            current_column += 1
        '''
        print("end layout ui")

        self._update()
        self.root.mainloop()

    def _update_history_file(self):
        self.qualityMetricsHistory.update()
        return

    def _update_user_interface(self):
        print("begin update ui")
        
        i=1
        for item in self.trend_graph_param_list :
            i=i+1
            if(item=='Compiler warning score'):
               self._update_warnings_burn_down_chart()
            else:
            #self._update_coverity_burn_down_chart()   "Coverity level 1 errors"
               self._update_history_burn_down_chart_of_type(item,i) #"Coverity level 1"
            '''
            #self._update_security_burn_down_chart()    "Security level 1 errors"
            self._update_history_burn_down_chart_of_type(item,3)#
            print(' begin  my code ')
            '''
        self._update_table_With_values()#  amrendra
        #self._update_table_values()
            

        print("end update ui")

        return
        
    #get_history_of_type_in_par
    def _update_history_burn_down_chart_of_type(self,ertype,id_no):

        min_value = 0
        max_value =1200
        step = 200
        burn_down_show = False
        burn_down_begin_date = '1-Dec-2020'
        burn_down_begin_value = 6600
        burn_down_end_date = '31-Dec-2020'
        burn_down_end_value = 0
        
        historyData_Date_TotalCount_dict=self.qualityMetricsHistory.get_history_of_type_in_par(ertype)
        print(' history for type '+ertype+ '='+str(historyData_Date_TotalCount_dict ) )
        if(id_no==2):
           self._generate_burn_down_chart(ertype, min_value, max_value, step, burn_down_show, burn_down_begin_date, burn_down_begin_value, burn_down_end_date, burn_down_end_value, historyData_Date_TotalCount_dict, self.filename_coverity_burndown_graph)
           self.image_coverity_burndown_graph.configure(file=self.filename_coverity_burndown_graph)
        if(id_no==3):
           self._generate_burn_down_chart(ertype, min_value, max_value, step, burn_down_show, burn_down_begin_date, burn_down_begin_value, burn_down_end_date, burn_down_end_value, historyData_Date_TotalCount_dict, self.filename_security_burndown_graph)
           self.image_security_burndown_graph.configure(file=self.filename_security_burndown_graph)
        else:
            self._generate_burn_down_chart(ertype, min_value, max_value, step, burn_down_show, burn_down_begin_date, burn_down_begin_value, burn_down_end_date, burn_down_end_value, historyData_Date_TotalCount_dict, self.filename_warning_burndown_graph)
            self.image_warning_burndown_graph.configure(file=self.filename_warning_burndown_graph)
          
        

    def _update_warnings_burn_down_chart(self):
        min_value = 0
        max_value =9000
        step = 1000
        burn_down_show = False
        burn_down_begin_date = '1-Jan-2019'
        burn_down_begin_value = 6600
        burn_down_end_date = '31-Dec-2020'
        burn_down_end_value = 0
        data = self.qualityMetricsHistory.get_history_warning_suppression_indicator()

        self._generate_burn_down_chart("Compiler warning score", min_value, max_value, step, burn_down_show, burn_down_begin_date, burn_down_begin_value, burn_down_end_date, burn_down_end_value, data, self.filename_warning_burndown_graph)
        self.image_warning_burndown_graph.configure(file=self.filename_warning_burndown_graph)

    def _update_coverity_burn_down_chart(self):
        min_value = 0
        max_value = 600
        step = 100
        burn_down_show = True
        burn_down_begin_date = '12-Sep-2017'
        burn_down_begin_value = 546
        burn_down_end_date = '02-Jul-2019'
        burn_down_end_value = 0
        data = self.qualityMetricsHistory.get_history_coverity_level_1()

        self._generate_burn_down_chart("Coverity level 1 errors", min_value, max_value, step, burn_down_show, burn_down_begin_date, burn_down_begin_value, burn_down_end_date, burn_down_end_value, data, self.filename_coverity_burndown_graph)
        self.image_coverity_burndown_graph.configure(file=self.filename_coverity_burndown_graph)

    def _update_security_burn_down_chart(self):
        min_value = 0
        max_value = 2000
        step = 500
        burn_down_show = False
        burn_down_begin_date = '1-Jan-2019'
        burn_down_begin_value = 1100
        burn_down_end_date = '31-Dec-2019'
        burn_down_end_value = 0
        data = self.qualityMetricsHistory.get_history_security_level_1()

        self._generate_burn_down_chart("Security level 1 errors", min_value, max_value, step, burn_down_show, burn_down_begin_date, burn_down_begin_value, burn_down_end_date, burn_down_end_value, data, self.filename_security_burndown_graph)
        self.image_security_burndown_graph.configure(file=self.filename_security_burndown_graph)

    def _generate_burn_down_chart(self, name, min_y, max_y, step_y, burn_down_show, burn_down_begin_date, burn_down_begin_value, burn_down_end_date, burn_down_end_value, data, graph_filename):
        date_format = "%d-%b-%Y"

        plt.clf()

        # set range
        min_x = datetime.strptime(self.chart_begin_date, date_format)
        max_x = datetime.strptime(self.chart_end_date, date_format)
        #plt.xlim(min_x, max_x)

        # sort values by datetime
        dates = []
        values = []
       
        for key, value in sorted(data.items()):
            dates.append(key)
            values.append(value)
            
        min_val=min(values)-10
        max_val=max(values)+10
        print(':::::::::::::::::::::',min_val)
        print(dates)
        print(dates[0])
        print(dates[-1])
        print(values)
        print(':::::::::::::::::::::',max_val)
        plt.xlim(dates[0], dates[-1])
        history_interval_in_days=(dates[-1]-dates[0]).days
        # plot history data
        plt.plot_date(dates, values, "-")

        # plot burn down
        if burn_down_show:
            burn_down_begin_x = datetime.strptime(burn_down_begin_date, date_format)
            burn_down_end_x = datetime.strptime(burn_down_end_date, date_format)
            plt.plot([burn_down_begin_x, burn_down_end_x], [burn_down_begin_value, burn_down_end_value], '--r', label="Burndown")

        # plot labels
        plt.xlabel('Date')
        plt.title(name)

        # plot ticks
        years = mdates.YearLocator()  # every year
        months = mdates.MonthLocator()  # every month
        day=mdates.DayLocator()
        years_fmt = mdates.DateFormatter('%Y')
        dt_fmt=mdates.DateFormatter('%d-%m-%y')
        if(history_interval_in_days > 365 ):
           plt.gca().xaxis.set_major_locator(years)
           plt.gca().xaxis.set_minor_locator(months)
        elif(history_interval_in_days > 90 ):
           plt.gca().xaxis.set_major_locator(months)
           plt.gca().xaxis.set_minor_locator(mdates.WeekdayLocator(interval=2))
        elif( history_interval_in_days > 30 ):
           plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
           plt.gca().xaxis.set_minor_locator(mdates.WeekdayLocator(interval=1))
        elif( history_interval_in_days < 13 ):
           plt.gca().xaxis.set_major_locator(mdates.DayLocator())
           #plt.gca().xaxis.set_minor_locator(mdates.WeekdayLocator(interval=1))
        else:
           plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
           plt.gca().xaxis.set_minor_locator(mdates.DayLocator(interval=2))
           
        #plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y'))#dt_fmt)#years_fmt)
        #plt.gca().xaxis.set_minor_locator(day)#months)
        plt.gca().xaxis.set_minor_formatter(DateFormatter('%d'))
        
        #stp=8#int( (max_val-min_val)/8 )
        #plt.yticks(np.arange(min_val, max_val, step=stp))
       # plt.yticks(np.arange(min_y, max_y, step=step_y))

        # save image
        plt.savefig(graph_filename, bbox_inches='tight', dpi=70)
        
    ###################################################
    #implemented by Amrendra 
    #lets have one single function to update the statistics table with single call to 
    #qualityMetrices side
    def _update_table_With_values(self):
           print('________________________________________________________________________')
           value_dict={}
           delta_value_dict={}
           for value in self.param_list:
              value_dict[value]=self.qualityMetricsHistory.get_values_of_worksheet_lastrow(value)
             # print(' '+value + ' = '+str(value_dict[value]));
              delta_value_dict[value]=self.qualityMetricsHistory.get_deltas_of_worksheet_lastrow(value)
              #print(' '+value + ' = '+str(delta_value_dict[value]));
              
              for index in range(len(self.unit_collection.units) + 1):
                self._update_table_label(self.table_row_header_to_data_levels[value][index], value_dict[value][index], delta_value_dict[value][index])
           print('________________________________________________________________________')     
             
    '''
        values0=[]
        delta0=[]
        values1=[]
        delta1=[]
        values2=[]
        delta2=[]
        values3=[]
        delta3=[]
        values4=[]
        delta4=[]
        values5=[]
        delta5=[]
        values6=[]
        delta6=[]
        values7=[]
        dalta7=[]
        configur = ConfigParser()
        configur.read('config.ini')
        #delta = self.qualityMetricsHistory.get_deltas_wrong_warning_level()[index]
        print('________________________________________________________________________')
        
        par1=configur.get('DisplayParam','par1')
        value0=self.qualityMetricsHistory.get_values_of_worksheet_lastrow(par1)
        delta0=self.qualityMetricsHistory.get_deltas_of_worksheet_lastrow(par1)
        print(' '+par1 + ' = '+str(value0));
        print(' '+par1 + ' = '+str(delta0));
        
        par2=configur.get('DisplayParam','par2')
        value1=self.qualityMetricsHistory.get_values_of_worksheet_lastrow(par2)
        delta1=self.qualityMetricsHistory.get_deltas_of_worksheet_lastrow(par2)
        print(' '+par2 + ' = '+str(value1));
        print(' '+par2 + ' = '+str(delta1));
        
        par3=configur.get('DisplayParam','par3')
        value2=self.qualityMetricsHistory.get_values_of_worksheet_lastrow(par3)
        delta2=self.qualityMetricsHistory.get_deltas_of_worksheet_lastrow(par3)
        print(' '+par3 + ' = '+str(value2));
        print(' '+par3 + ' = '+str(delta2));
        
        par4=configur.get('DisplayParam','par4')
        value3=self.qualityMetricsHistory.get_values_of_worksheet_lastrow(par4)
        delta3=self.qualityMetricsHistory.get_deltas_of_worksheet_lastrow(par4)
        print(' '+par4 + ' = '+str(value3));
        print(' '+par4 + ' = '+str(delta3));
        
        par5=configur.get('DisplayParam','par5')
        value4=self.qualityMetricsHistory.get_values_of_worksheet_lastrow(par5)
        delta4=self.qualityMetricsHistory.get_deltas_of_worksheet_lastrow(par5)
        print(' '+par5 + ' = '+str(value4));
        print(' '+par5 + ' = '+str(delta4));
        
        par6=configur.get('DisplayParam','par6')
        value5=self.qualityMetricsHistory.get_values_of_worksheet_lastrow(par6)
        delta5=self.qualityMetricsHistory.get_deltas_of_worksheet_lastrow(par6)
        print(' '+par6 + ' = '+str(value5));
        print(' '+par6 + ' = '+str(delta5));
        
        par7=configur.get('DisplayParam','par7')
        value6=self.qualityMetricsHistory.get_values_of_worksheet_lastrow(par7)
        delta6=self.qualityMetricsHistory.get_deltas_of_worksheet_lastrow(par7)
        print(' '+par7 + ' = '+str(value6));
        print(' '+par7 + ' = '+str(delta6));
        
        par8=configur.get('DisplayParam','par8')
        value7=self.qualityMetricsHistory.get_values_of_worksheet_lastrow(par8)
        delta7=self.qualityMetricsHistory.get_deltas_of_worksheet_lastrow(par8)
        print(' '+par8 + ' = '+str(value7));
        print(' '+par8 + ' = '+str(delta7));
        
        par9=configur.get('DisplayParam','par9')
        value8=self.qualityMetricsHistory.get_values_of_worksheet_lastrow(par9)
        delta8=self.qualityMetricsHistory.get_deltas_of_worksheet_lastrow(par9)
        print(' '+par9 + ' = '+str(value8));
        print(' '+par9 + ' = '+str(delta8));
        
        for index in range(len(self.unit_collection.units) + 1):
             self._update_table_label(self.labels_TQI_data[index], value8[index], delta8[index])
    
        print('___________________________________________________________________')
    '''    
    
    
    ###################################################

    def _update_table_values(self):
        for index in range(len(self.unit_collection.units) + 1):
            value = self.qualityMetricsHistory.get_values_wrong_warning_level()[index]
            delta = self.qualityMetricsHistory.get_deltas_wrong_warning_level()[index]
            self._update_table_label(self.labels_wrong_warning_level_data[index], value, delta)

            value = self.qualityMetricsHistory.get_values_treat_warnings_not_as_errors()[index]
            delta = self.qualityMetricsHistory.get_deltas_treat_warnings_not_as_errors()[index]
            self._update_table_label(self.labels_treat_warnings_not_as_errors_data[index], value, delta)

            value = self.qualityMetricsHistory.get_values_suppressed_warnings()[index]
            delta = self.qualityMetricsHistory.get_deltas_suppressed_warnings()[index]
            self._update_table_label(self.labels_suppressed_warnings_data[index], value, delta)

            value = self.qualityMetricsHistory.get_values_actual_warnings()[index]
            delta = self.qualityMetricsHistory.get_deltas_actual_warnings()[index]
            self._update_table_label(self.labels_actual_warnings_data[index], value, delta)

            value = self.qualityMetricsHistory.get_values_coverity_level_1()[index]
            delta = self.qualityMetricsHistory.get_deltas_coverity_level_1()[index]
            self._update_table_label(self.labels_coverity_level_1_data[index], value, delta)

            value = self.qualityMetricsHistory.get_values_coverity_level_2()[index]
            delta = self.qualityMetricsHistory.get_deltas_coverity_level_2()[index]
            self._update_table_label(self.labels_coverity_level_2_data[index], value, delta)

            value = self.qualityMetricsHistory.get_values_security_level_1()[index]
            delta = self.qualityMetricsHistory.get_deltas_security_level_1()[index]
            self._update_table_label(self.labels_security_level_1_data[index], value, delta)

            value = self.qualityMetricsHistory.get_values_security_level_2()[index]
            delta = self.qualityMetricsHistory.get_deltas_security_level_2()[index]
            self._update_table_label(self.labels_security_level_2_data[index], value, delta)

    def _update_table_label(self, label, value, delta):
        style = "TableCellValueUnchanged.TLabel"
        if delta < 0:
            style = "TableCellValueDown.TLabel"
        if delta > 0:
            style = "TableCellValueUp.TLabel"
        label.configure(style=style)
        label.configure(text=str(round(value,1)))
        if delta != 0:
            label.configure(text=str(round(delta,1)) + "(" + str(round(value,1)) + ")")

    def _update(self):
        now = time.strftime("(snapshot %A %B %d %H:%M:%S)")
        self.root.title("Allura R8.x.100 Warning Settings Monitor v1.0  " + now)

        self._update_history_file()
        self._update_user_interface()

        # refresh only once every 5 minutes
        self.root.after(300000, self._update)


mainView = MainView()
