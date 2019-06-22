import routines as routines
import tkinter as tk

class ScreenController(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()


class NavBarComponent(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(self, text="Sell Tradepile",
                  command=lambda: master.master.switch_frame(SellScreen)).grid(row = 0,column = 0)
        tk.Button(self, text="Snipe Players",
                  command=lambda: master.master.switch_frame(SnipeScreen)).grid(row = 0,column = 1)


class SellComponent(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Status:").grid(row = 1,column = 0)
        self.lbl = tk.Label(self, text="")
        self.lbl.grid(row = 2,column = 0)

        tk.Button(
            self, 
            text="Start",
            command=lambda: routines.async_sell_players(self.lbl)
        ).grid(row = 0,column = 0, pady=5)


class SnipeFormComponent(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        tk.Label(self, text="Name:").grid(row = 0, column = 0)
        self.name = tk.Entry(self)
        self.name.grid(row = 0, column = 1, pady=20)


        tk.Label(self, text="Quality:").grid(row = 1,column = 0)
        self.quality = tk.Entry(self)
        self.quality.grid(row = 1, column = 1)

        tk.Label(self, text="Chem Style:").grid(row = 2,column = 0)
        self.chem_style = tk.Entry(self)
        self.chem_style.grid(row = 2, column = 1)

        tk.Label(self, text="League:").grid(row = 3,column = 0)
        self.league = tk.Entry(self)
        self.league.grid(row = 3, column = 1)


        tk.Label(self, text="Position:").grid(row = 1,column = 2)
        self.position = tk.Entry(self)
        self.position.grid(row = 1, column = 3)

        tk.Label(self, text="Nation:").grid(row = 2,column = 2)
        self.nation = tk.Entry(self)
        self.nation.grid(row = 2, column = 3)

        tk.Label(self, text="Club:").grid(row = 3,column = 2)
        self.club = tk.Entry(self)
        self.club.grid(row = 3, column = 3)


        tk.Label(self, text="Alternate Positions:").grid(row = 4,column = 0, pady=(20,0))
        self.alt_positions = tk.Entry(self)
        self.alt_positions.grid(row = 4, column = 1, pady=(20,0))

        tk.Label(self, text="Alternate Chem Styles:").grid(row = 5,column = 0)
        self.alt_chem_styles = tk.Entry(self)
        self.alt_chem_styles.grid(row = 5, column = 1)


        tk.Label(self, text="Max Price:").grid(row = 4,column = 2, pady=(20,0))
        self.max_price = tk.Entry(self)
        self.max_price.grid(row = 4, column = 3, pady=(20,0))


        self.pos_mod_price = 0
        tk.Checkbutton(self, text="Position modifies price?", variable=self.pos_mod_price).grid(row = 5,column = 2, columnspan=2, padx=30)


        tk.Label(self, text="Status:").grid(row = 10, column = 0)
        self.lbl_total_players = tk.Label(self, text="Total Players Bought:")
        self.lbl_total_players.grid(row = 11, column = 0)
        self.lbl_total_profit = tk.Label(self, text="Total Profit:")
        self.lbl_total_profit.grid(row = 12, column = 0)
        tk.Button(
            self, 
            text="Submit",
            command=lambda: routines.async_snipe(
                **{
                    "alt_positions" : int(self.alt_positions.get()) if self.alt_positions.get() else 0, 
                    "alt_chem_styles" : int(self.alt_chem_styles.get()) if self.alt_chem_styles.get() else 0,
                    "pos_mod_price" : self.pos_mod_price,
                    "quality" : self.quality.get(),
                    "chem_style" : self.chem_style.get(),
                    "league" : self.league.get(),
                    "position" : self.position.get(),
                    "nation" : self.nation.get(),
                    "club" : self.club.get(),
                    "max_price" : int(self.max_price.get()) if self.max_price.get() else 0,
                    "lbl_total_players" : self.lbl_total_players,
                    "lbl_total_profit" : self.lbl_total_profit
                }
            )
        ).grid(row = 9, column = 0, columnspan=4, pady=20)


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        NavBarComponent(self).grid(row = 0, column = 0)


class SellScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        NavBarComponent(self).grid(row = 0, column = 0)
        SellComponent(self).grid(row = 1, column = 0)
        

class SnipeScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        NavBarComponent(self).grid(row = 0, column = 0)
        SnipeFormComponent(self).grid(row = 1, column = 0)