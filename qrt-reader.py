from ttkbootstrap import Style
import tkinter as tk
from tkinter import ttk
from application import DisplayWindow, ProcessWindow

class Navbar(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.label = ttk.Label(self, text="Navigation Bar", style="primary.Inverse.TLabel").pack()

class Statusbar(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.statustext = ttk.Label(self, text="Ready...", style="info.Inverse.TLabel")
        self.statustext.pack(side="left", fill="both", padx=5, pady=5 )

class Main(ttk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        ttk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.displaywindow = DisplayWindow(self, style="TFrame")
        self.processwindow = ProcessWindow(self, style="secondary.TFrame")

        self.displaywindow.pack(side="left", fill="both", expand=True)
        self.processwindow.pack(side="left", fill="both", )

class MainApplication(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.navbar = Navbar(self, style="primary.TFrame")
        self.main = Main(self, style="TFrame")
        self.statusbar = Statusbar(self, style="info.TFrame")

        #self.navbar.pack(side="top", fill="x")
        self.main.pack(side="top", fill="both", expand=True)
        self.statusbar.pack(side="bottom", fill="x")

if __name__ == "__main__":
    style = Style()
    root = style.master
    root.wm_title("QRT Analysis")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()