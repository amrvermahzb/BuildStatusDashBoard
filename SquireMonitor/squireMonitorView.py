# Copyright (c) 2018 Koninklijke Philips N.V.
from squireMonitor import SquireMonitor
from testSystems import TestSystems
from tests import Tests
import tkinter as tk
from datetime import datetime


class SquireMonitorView(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        checkimage = tk.PhotoImage(file="check_mark_70x70.png")
        questionimage = tk.PhotoImage(file="question_mark_70x70.png")
        redcrossimage = tk.PhotoImage(file="red_cross_70x70.png")

        self.systemDisplayNames = {TestSystems.Names.Squire1: "SQ1", TestSystems.Names.Squire2: "SQ2",
                                   TestSystems.Names.Squire3: "SQ3", TestSystems.Names.Squire4: "SQ4",
                                   TestSystems.Names.Squire5: "SQ5", TestSystems.Names.Squire6: "SQ6",
                                   TestSystems.Names.Squire7: "SQ7", TestSystems.Names.Squire8: "SQ8",
                                   TestSystems.Names.Squire9: "SQ9", TestSystems.Names.BV2: "BV2", }

        self.testDisplayNames = {Tests.Names.Drive: "DRIVE", Tests.Names.Loop: "LOOP", Tests.Names.IVVR: "IVVR",
                                 Tests.Names.IPISLIB: "IPISLIB", Tests.Names.Reviewing: "Reviewing",
                                 Tests.Names.Tsm: "TSM",
                                 Tests.Names.Install: "Install", Tests.Names.Nightbatch: "Nightbatch",
                                 Tests.Names.Regressioncheck: "Regressioncheck"}
        self.labelColors = {"Failure": "red",
                            "Failed": "red",
                            "FAILED": "red",
                            "AbortedWithErrors": "red",
                            "AbortedNoErrors": "red",
                            "Unknown": "red",
                            "Success": "green",
                            "Passed": "green",
                            "PASSED": "green",
                            "Not found": "grey"}

        self.resultImage = {"Failure": redcrossimage,
                            "Failed": redcrossimage,
                            "FAILED": redcrossimage,
                            "AbortedWithErrors": redcrossimage,
                            "AbortedNoErrors": redcrossimage,
                            "Unknown": redcrossimage,
                            "Success": checkimage,
                            "Passed": checkimage,
                            "PASSED": checkimage,
                            "Not found": questionimage}

        self.squireMonitor = SquireMonitor()
        self.testSystemCount = len(TestSystems.Names)
        self.testCount = len(Tests.Names)

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(sticky=tk.W + tk.E + tk.N + tk.S)

        self.buildLabels = [[0] * self.testCount for i in range(self.testSystemCount)]
        self.update()

    def _update_label(self, r, c, testSystemName, result):
        label = self.buildLabels[r - 1][c - 1]
        labelText = self.systemDisplayNames[testSystemName] + " " + \
                    self.testDisplayNames[result.testName] + "\n" + \
                    result.get_latest_result_date()

        if result.is_overdue():
            labelText = labelText + "\n<<overdue>>"

        latestResult = result.get_latest_result()
        if latestResult not in self.labelColors or latestResult not in self.resultImage:
            latestResult = "Not found"

        content = tk.StringVar()
        content.set(labelText)
        if label == 0:
            # create label only at first time
            label = tk.Label(self, textvariable=content, anchor=tk.W, padx=20, compound=tk.LEFT, relief=tk.RAISED,
                             bg=self.labelColors[latestResult], image=self.resultImage[latestResult],
                             font=('Helvetica', 15, 'bold'))
            self.buildLabels[r - 1][c - 1] = label
        else:
            # else update label text and color
            label.config(textvariable=content, bg=self.labelColors[latestResult], image=self.resultImage[latestResult])
        self.rowconfigure(r, weight=1)
        self.columnconfigure(c, weight=1)
        label.grid(row=r, column=c, sticky=tk.W + tk.E + tk.N + tk.S)

    def update(self):
        row = 1
        now = datetime.now()
        self.master.title("IP-Lab Test Status Monitor v1.5  " + now.strftime('%Y-%m-%d'))
        print("Updating status: " + now.strftime('%Y-%m-%d %H:%M:%S'))

        for testSystem in self.squireMonitor.testSystems:
            column = 1
            testSystem.update_results()
            for result in testSystem.testResults:
                self._update_label(row, column, testSystem.name, result)

                column += 1
            row += 1

        # refresh hourly
        self.master.after(3600000, self.update)


if __name__ == '__main__':
    root = tk.Tk()
    root.state("zoomed")  # Not portable; works on some platforms like Windows and macOS, want portable code use:
    # w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    # root.geometry("%dx%d+0+0" % (w, h))
    squireMonitorView = SquireMonitorView(root)
    root.mainloop()
