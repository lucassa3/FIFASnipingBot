import tkinter as tk
from view.common_components import NavBarComponent, FarmBronzePackComponent


class BronzePackFarmScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        NavBarComponent(master).grid(row=0, column=0)
        self.start_button = FarmBronzePackComponent(self)
        self.start_button.grid(row=1, column=0)
