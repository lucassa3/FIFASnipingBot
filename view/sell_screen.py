import tkinter as tk
import controller.routines as routines
import controller.program_state as ps
from view.common_components import NavBarComponent, StatusTextComponent


class SellScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        NavBarComponent(master).grid(row=0, column=0)
        self.sell_component = SellComponent(self)
        self.sell_component.grid(row=1, column=0)
        self.status_text_component = StatusTextComponent(self)
        self.status_text_component.grid(row=2, column=0)


class SellComponent(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Button(
            self,
            text="Start",
            fg="#48c732",
            command=lambda: ps.ProgramState.switch_thread(routines.sell_cards),
        ).grid(row=0, column=0, pady=5)
        tk.Button(self, text="Stop", fg="#de190b", command=ps.ProgramState.stop_thread).grid(
            row=0, column=1
        )
