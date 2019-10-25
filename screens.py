import routines as routines
import tkinter as tk

class ScreenController(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.built_frames = {
            "sell_screen" : SellScreen(self),
            "snipe_screen" : SnipeScreen(self),
            "full_routine" : FullRoutineScreen(self),
            "start_page" : StartPage(self)
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


class NavBarComponent(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(self, text="Sell Tradepile",
                  command=lambda: master.switch_frame("sell_screen")).grid(row = 0,column = 0)
        tk.Button(self, text="Snipe Players",
                  command=lambda: master.switch_frame("snipe_screen")).grid(row = 0,column = 1)
        tk.Button(self, text="Full Routine",
                  command=lambda: master.switch_frame("full_routine")).grid(row = 0,column = 2)

class StartStopComponent(tk.Frame):
    def __init__(self, master, full_routine=False, start_button_label="Start", stop_button_label="Stop"):
        tk.Frame.__init__(self, master)

        if full_routine:
            tk.Button(
                self, 
                text="Sell and " + start_button_label,
                fg="#48c732",
                command=lambda: routines.async_full_routine(**{
                    "alt_positions" : int(master.alt_positions.get()) if master.alt_positions.get() else 0, 
                    "alt_chem_styles" : int(master.alt_chem_styles.get()) if master.alt_chem_styles.get() else 0,
                    "name" : master.name.get(),
                    "quality" : master.quality.get(),
                    "chem_style" : master.chem_style.get(),
                    "league" : master.league.get(),
                    "position" : master.position.get(),
                    "nation" : master.nation.get(),
                    "club" : master.club.get(),
                    "max_price" : int(master.max_price.get()) if master.max_price.get() else 0
                })
            ).grid(row = 0,column = 0)
        else:
            tk.Button(
                self, 
                text=start_button_label,
                fg="#48c732",
                command=lambda: routines.async_snipe(**{
                    "alt_positions" : int(master.alt_positions.get()) if master.alt_positions.get() else 0, 
                    "alt_chem_styles" : int(master.alt_chem_styles.get()) if master.alt_chem_styles.get() else 0,
                    "name" : master.name.get(),
                    "quality" : master.quality.get(),
                    "chem_style" : master.chem_style.get(),
                    "league" : master.league.get(),
                    "position" : master.position.get(),
                    "nation" : master.nation.get(),
                    "club" : master.club.get(),
                    "max_price" : int(master.max_price.get()) if master.max_price.get() else 0
                })
            ).grid(row = 0,column = 0)

        tk.Button(
            self, 
            text=stop_button_label,
            fg="#de190b",
            command=routines.stop_program
        ).grid(row = 0,column = 1)


# class StartStopConsumableComponent(tk.Frame):
#     def __init__(self, master, full_routine=False, start_button_label="Start", stop_button_label="Stop"):
#         tk.Frame.__init__(self, master)

#         tk.Button(
#             self, 
#             text=start_button_label,
#             fg="#48c732",
#             command=lambda: routines.async_full_routine(**{
#                 "consumable_type" : master.name.get(), 
#                 "chem_type" : master.name.get(),
#             })
#         ).grid(row = 0,column = 0)

#         tk.Button(
#             self, 
#             text=stop_button_label,
#             fg="#de190b",
#             command=routines.stop_program
#         ).grid(row = 0,column = 1)

class SellComponent(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Status:").grid(row = 1,column = 0)
        self.lbl = tk.Label(self, text="")
        self.lbl.grid(row = 2,column = 0)

        tk.Button(
            self, 
            text="Start",
            fg="#48c732",
            command=lambda: routines.async_sell_players()
        ).grid(row = 0,column = 0, pady=5)


class SnipeFormComponent(tk.Frame):
    def __init__(self, master, full_routine_form=False):
        tk.Frame.__init__(self, master)
        
        tk.Label(self, text="Name:").grid(row = 0, column = 0)
        self.name = tk.Entry(self)
        self.name.grid(row = 0, column = 1, pady=20, padx=10)


        tk.Label(self, text="Quality:").grid(row = 1,column = 0)
        self.quality = tk.Entry(self)
        self.quality.grid(row = 1, column = 1)

        tk.Label(self, text="Chem Style:").grid(row = 2,column = 0)
        self.chem_style = tk.Entry(self)
        self.chem_style.grid(row = 2, column = 1)

        tk.Label(self, text="League:").grid(row = 3,column = 0, pady=(0,30))
        self.league = tk.Entry(self)
        self.league.grid(row = 3, column = 1, pady=(0,35))


        tk.Label(self, text="Position:").grid(row = 1,column = 2)
        self.position = tk.Entry(self)
        self.position.grid(row = 1, column = 3, padx=10)

        tk.Label(self, text="Nation:").grid(row = 2,column = 2)
        self.nation = tk.Entry(self)
        self.nation.grid(row = 2, column = 3)

        tk.Label(self, text="Club:").grid(row = 3,column = 2, pady=(0,35))
        self.club = tk.Entry(self)
        self.club.grid(row = 3, column = 3, pady=(0,35))


        tk.Label(self, text="Alternate Positions:").grid(row = 4,column = 0)
        self.alt_positions = tk.Entry(self)
        self.alt_positions.grid(row = 4, column = 1)

        tk.Label(self, text="Alternate Chem Styles:").grid(row = 5,column = 0)
        self.alt_chem_styles = tk.Entry(self)
        self.alt_chem_styles.grid(row = 5, column = 1)


        tk.Label(self, text="Max Price:").grid(row = 4,column = 2)
        self.max_price = tk.Entry(self)
        self.max_price.grid(row = 4, column = 3)

        if full_routine_form:
            StartStopComponent(self, full_routine=True).grid(row = 9, column = 0, columnspan=4, pady=20)
        else:
            StartStopComponent(self, full_routine=False).grid(row = 9, column = 0, columnspan=4, pady=20)

        tk.Label(self, text="Status:").grid(row = 10, column = 0)

        tk.Label(self, text="Total Players Bought:").grid(row = 11, column = 0)
        tk.Label(self, text="Total Profit:").grid(row = 12, column = 0)

        self.lbl_total_players = tk.Label(self, text="0", relief="groove", width=15)
        self.lbl_total_players.grid(row = 11, column = 1)
        self.lbl_total_profit = tk.Label(self, text="0", relief="groove", width=15)
        self.lbl_total_profit.grid(row = 12, column = 1)

# class SnipeConsumableFormComponent(tk.Frame):
#     def __init__(self, master):
#         tk.Frame.__init__(self, master)

#         tk.Label(self, text="Item Type:").grid(row = 0, column = 0, pady=(0,35))
#         self.consumable_type = tk.Entry(self)
#         self.consumable_type.grid(row = 1, column = 1, pady=(0,35))


#         tk.Label(self, text="Item:").grid(row = 0, column = 2, pady=(0,35))
#         self.chem_type = tk.Entry(self)
#         self.chem_type.grid(row = 3, column = 3, pady=(0,35))


#         tk.Label(self, text="Max Price:").grid(row = 1, column = 0)
#         self.consumable_type = tk.Entry(self)
#         self.max_price.grid(row = 1, column = 1)


#         StartStopConsumbaleComponent(self, full_routine=False).grid(row = 9, column = 0, columnspan=4, pady=20)

#         tk.Label(self, text="Status:").grid(row = 10, column = 0)

#         tk.Label(self, text="Total Cards Bought:").grid(row = 11, column = 0)
#         tk.Label(self, text="Total Profit:").grid(row = 12, column = 0)

#         self.lbl_total_players = tk.Label(self, text="0", relief="groove", width=15)
#         self.lbl_total_players.grid(row = 11, column = 1)
#         self.lbl_total_profit = tk.Label(self, text="0", relief="groove", width=15)
#         self.lbl_total_profit.grid(row = 12, column = 1)

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        NavBarComponent(master).grid(row = 0, column = 0)
        tk.Label(self, text="Welcome to this marvelous FIFA 20 Bot!").grid(row = 1, column = 0, pady=20)
        tk.Label(self, text="Made with love by Lucas Astur").grid(row = 2,column = 0, pady=20)


class SellScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        NavBarComponent(master).grid(row = 0, column = 0)
        self.sell_component = SellComponent(self)
        self.sell_component.grid(row = 1, column = 0)
        

class SnipeScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        NavBarComponent(master).grid(row = 0, column = 0)
        self.snipe_form_component = SnipeFormComponent(self)
        self.snipe_form_component.grid(row = 1, column = 0)

class FullRoutineScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        NavBarComponent(master).grid(row = 0, column = 0)
        self.snipe_form_component = SnipeFormComponent(self, full_routine_form=True)
        self.snipe_form_component.grid(row = 1, column = 0)