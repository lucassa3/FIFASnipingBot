import tkinter as tk
from view.common_components import NavBarComponent, SellComponent, StatusTextComponent


class SellScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        NavBarComponent(master).grid(row=0, column=0)
        self.sell_component = SellComponent(self)
        self.sell_component.grid(row=1, column=0)
        self.status_text_component = StatusTextComponent(self)
        self.status_text_component.grid(row=2, column=0)
