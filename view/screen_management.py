import tkinter as tk
from view.sell_screen import SellScreen
from view.snipe_screen import SnipeScreen
from view.full_routine_screen import FullRoutineScreen
from view.farm_bronze_pack_screen import BronzePackFarmScreen
from view.common_components import NavBarComponent


class ScreenController(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.built_frames = {
            "sell_screen": SellScreen(self),
            "snipe_screen": SnipeScreen(self),
            "full_routine": FullRoutineScreen(self),
            "farm_bronze_pack_routine": BronzePackFarmScreen(self),
            "start_page": StartPage(self),
        }
        self.switch_frame("start_page")

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        if frame_class in self.built_frames:
            new_frame = self.built_frames[frame_class]
        else:
            raise ValueError("Unknown frame")

        if self._frame is not None:
            self._frame.grid_remove()
        self._frame = new_frame
        self._frame.grid()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        NavBarComponent(master).grid(row=0, column=0)
        tk.Label(self, text="Welcome to FIFA 21 Bot!").grid(row=1, column=0, pady=20)
        tk.Label(self, text="Made by Lucas Astur").grid(row=2, column=0, pady=20)
