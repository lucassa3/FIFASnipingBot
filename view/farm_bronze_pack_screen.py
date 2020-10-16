import tkinter as tk
from view.common_components import NavBarComponent
import controller.routines as routines


class BronzePackFarmScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        NavBarComponent(master).grid(row=0, column=0)
        self.start_button = FarmBronzePackComponent(self)
        self.start_button.grid(row=1, column=0)


class FarmBronzePackComponent(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Button(
            self,
            text="Start Farming",
            fg="#48c732",
            command=lambda: routines.async_farm_bronze_packs(),
        ).grid(row=0, column=0, pady=5)
        tk.Button(self, text="Stop", fg="#de190b", command=routines.stop_program).grid(
            row=0, column=1
        )
