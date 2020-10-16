import tkinter as tk
import controller.routines as routines
import controller.program_state as ps
from view.common_components import NavBarComponent, StatusTextComponent


class BronzePackFarmScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        NavBarComponent(master).grid(row=0, column=0)
        self.start_button = FarmBronzePackComponent(self)
        self.start_button.grid(row=1, column=0)
        self.status_text_component = StatusTextComponent(self)
        self.status_text_component.grid(row=2, column=0)


class FarmBronzePackComponent(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Button(
            self,
            text="Start Farming",
            fg="#48c732",
            command=lambda: ps.ProgramState.switch_thread(
                routines.farm_bronze_packs_sync_routine
            ),
        ).grid(row=0, column=0, pady=5)
        tk.Button(self, text="Stop", fg="#de190b", command=ps.ProgramState.stop_thread).grid(
            row=0, column=1
        )
