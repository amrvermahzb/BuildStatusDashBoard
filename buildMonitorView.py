import tkinter as tk
from datetime import *
from buildMonitor import *
from build import *

LABEL_COLORS = {"failed": "red", "successful": "green", "not found": "grey", "not available": "blue"}


class BuildMonitorView(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        checkimage = tk.PhotoImage(file="check_mark_70x70.png")
        questionimage = tk.PhotoImage(file="question_mark_70x70.png")
        redcrossimage = tk.PhotoImage(file="red_cross_70x70.png")
        runningimage = tk.PhotoImage(file="run_70x70.png")

        self.result_color = {"successful": "green",
                             "not found": "grey",
                             "not available": "blue",
                             "failed": "red"}
        self.result_image = {"successful": checkimage,
                             "not found": questionimage,
                             "not available": runningimage,
                             "failed": redcrossimage}

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(sticky=tk.W+tk.E+tk.N+tk.S)
        self.buildMonitor = BuildMonitor()
        self.numUnits = len(self.buildMonitor.Units)
        self.numBuildTypes = len(build_types)
        self.buildLabels = [[0] * self.numBuildTypes for i in range(self.numUnits)]
        self.update()

    @staticmethod
    def get_label_color(build_result):
        return LABEL_COLORS[build_result]

    @staticmethod
    def get_label_text(build_label, build_date, build_result, build_date_according_build_order):
        text_date = build_date.__str__()
        if text_date != "":
            text = "    " + build_label + " " + build_result + " (" + text_date + ")"
            if not build_date_according_build_order:
                text = text + " <<overdue>>"
        else:
            text = build_label + " " + build_result

        return text

    def create_label(self, r, c, build_label, build_date, build_result, build_date_according_build_order):
        text = tk.StringVar()
        text.set(self.get_label_text(build_label, build_date, build_result, build_date_according_build_order))

        label = self.buildLabels[r - 1][c - 1]
        if label == 0:
            # create label only at first time
            label = tk.Label(self, textvariable=text, anchor=tk.W, padx=20, compound=tk.LEFT, relief=tk.RAISED,
                             bg=self.result_color[build_result], image=self.result_image[build_result],
                             font=('Helvetica', 17, 'bold'))
            self.buildLabels[r - 1][c - 1] = label
        else:
            # else update label text and color
            label.config(textvariable=text, bg=self.result_color[build_result], image=self.result_image[build_result])

        self.rowconfigure(r, weight=1)
        self.columnconfigure(c, weight=1)
        label.grid(row=r, column=c, sticky=tk.W + tk.E + tk.N + tk.S)

    def update(self):
        row = 1
        now = time.strftime("(snapshot %A %B %d %H:%M)")
        self.master.title("Allura R8.x.100 Build Status Monitor v3.2  " + now)
        for unit in self.buildMonitor.Units:
            column = 1

            previous_build_date = ""

            for build in unit.builds:
                build_label = unit.unit_name + '_' + build.build_type
                build_date = build.get_latest_build_date()
                build_result = build.get_latest_build_result()

                build_date_according_build_order = True
                if previous_build_date != "" and build_date < previous_build_date:
                    build_date_according_build_order = False

                previous_build_date = build_date

                self.create_label(row, column, build_label, build_date, build_result, build_date_according_build_order)
                column += 1

            row += 1

        # refresh only once every 5 minutes
        self.master.after(300000, self.update)


def main():
    root = tk.Tk()
    root.state("zoomed")  # Not portable; works on some platforms like Windows and macOS, want portable code use:
                          # w, h = root.winfo_screenwidth(), root.winfo_screenheight()
                          # root.geometry("%dx%d+0+0" % (w, h))
    BuildMonitorView(master=root)
    root.mainloop()


if __name__ == '__main__':
    main()
