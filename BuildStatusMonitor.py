from tkinter import *
from datetime import *
import GetBuildStatus
import os.path
import time


def get_build_result(filename):
    with open(filename) as f:
        content = f.readlines()
    result = "failed"
    for line in content:
        if "overall-result" in line:
            if "success" in line:
                result = "successful"
    return result


def get_build_dates_info(dates):
    date_ci = dates[0]
    date_ext = dates[1]
    days_ago_ext = -1
    if date_ci != "" and date_ext != "":
        time_delta = date_ext - date_ci
        days_ago_ext = time_delta.days
    return date_ci, date_ext, days_ago_ext


class BuildMonitor(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.checkimage = PhotoImage(file="check_mark_70x70.png")
        self.questionimage = PhotoImage(file="question_mark_70x70.png")
        self.redcrossimage = PhotoImage(file="red_cross_70x70.png")
        self.runningimage = PhotoImage(file="run_70x70.png")
        
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(sticky=W+E+N+S)
        self.units = ["Acq", "AUI", "FSSys", "HostSW", "IDClient", "Infra", "IPSW", "SETool", "UI", "UIM", "View",
                      "VxW"]
        self.numUnits = 12
        self.numBuildTypes = 2
        self.buildLabels = [[0] * self.numBuildTypes for i in range(self.numUnits)]
        self.update()

    def create_label(self, part, result, date_, days_ago, r, c):
        text_date = date_.__str__()
        if text_date != "":
            text = part + " " + result + " (" + text_date + ")"
            if days_ago < 0:
                text = text + " *****"
        else:
            text = part + " " + result

        var = StringVar()
        var.set(text)
        col = "red"
        imageref = self.redcrossimage
        if result == "successful":
            col = "green"
            imageref = self.checkimage
        elif result == "not found":
            col = "grey"
            imageref = self.questionimage
        elif result == "not available":
            col = "blue"
            imageref = self.runningimage
        label = self.buildLabels[r-1][c-1]
        if label == 0:
            # create label only at first time
            label = Label(self, textvariable=var, anchor=W, padx=20, compound=LEFT, relief=RAISED, bg=col, image=imageref, font=('Helvetica', 17, 'bold'))
            self.buildLabels[r - 1][c - 1] = label
        else:
            # else update label text and color
            label.config(textvariable=var, bg=col, image=imageref)
        self.rowconfigure(r, weight=1)
        self.columnconfigure(c, weight=1)
        label.grid(row=r, column=c, sticky=W+E+N+S)
        
    def create_labels(self, name, results, date_info, row_index):
        date_ci = date_info[0]
        date_ext = date_info[1]
        days_ago_ext = date_info[2]
        self.create_label(name + " CIBuild", results[0], date_ci, 0, row_index, 1)
        self.create_label(name + " Extended", results[1], date_ext, days_ago_ext, row_index, 2)

    def update(self):
        row = 1
        now = time.strftime("(snapshot %A %B %d %H:%M)")
        self.master.title("Allura R8.x.100 Build Status Monitor v3.1  " + now)
        for unit in self.units:
            build_info = GetBuildStatus.latest_unit_build_info(unit)
            build_results = []
            build_dates = []
            for build_date, path in build_info:
                if build_date == "<nodate>":
                    build_dates.append("")
                else:
                    build_dates.append(datetime.strptime(build_date, "%Y-%m-%d").date())
                if path == "<nopath>":
                    build_results.append("not found")
                else:
                    build_file = path + r'\BuildInformation.xml'
                    if os.path.isfile(build_file):
                        build_results.append(get_build_result(build_file))
                    else:
                        build_results.append("not available")

            date_info = get_build_dates_info(build_dates)
            self.create_labels(unit, build_results, date_info, row)
            row = row + 1
       

def main():
    root = Tk()
    root.state("zoomed") # Not portable; works on some platforms like Windows and macOS, want portable code use:  
                         # w, h = root.winfo_screenwidth(), root.winfo_screenheight() 
                         # root.geometry("%dx%d+0+0" % (w, h))
    monitor = BuildMonitor(master=root)
    root.after(300000, monitor.update) # refresh only once every 5 minutes
    root.mainloop()
  
if __name__ == '__main__':
    main()