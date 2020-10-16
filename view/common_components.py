import tkinter as tk
import controller.routines as routines


class NavBarComponent(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Button(
            self,
            text="Sell Tradepile",
            command=lambda: master.switch_frame("sell_screen"),
        ).grid(row=0, column=0)
        tk.Button(
            self,
            text="Snipe Players",
            command=lambda: master.switch_frame("snipe_screen"),
        ).grid(row=0, column=1)
        tk.Button(
            self,
            text="Full Routine",
            command=lambda: master.switch_frame("full_routine"),
        ).grid(row=0, column=2)
        tk.Button(
            self,
            text="Farm Bronze Packs",
            command=lambda: master.switch_frame("farm_bronze_pack_routine"),
        ).grid(row=0, column=3)


class StartStopComponent(tk.Frame):
    def __init__(
        self,
        master,
        full_routine=False,
        start_button_label="Start",
        stop_button_label="Stop",
    ):
        tk.Frame.__init__(self, master)

        if full_routine:
            tk.Button(
                self,
                text="Sell and " + start_button_label,
                fg="#48c732",
                command=lambda: routines.async_full_routine(
                    **{
                        "alt_chem_styles": int(master.alt_chem_styles.get())
                        if master.alt_chem_styles.get()
                        else 0,
                        "name": master.name.get(),
                        "quality": master.quality.get(),
                        "rarity": master.rarity.get(),
                        "chem_style": master.chem_style.get(),
                        "league": master.league.get(),
                        "position": master.position.get(),
                        "nation": master.nation.get(),
                        "club": master.club.get(),
                        "max_price": int(master.max_price.get())
                        if master.max_price.get()
                        else 0,
                    }
                ),
            ).grid(row=0, column=0)
        else:
            tk.Button(
                self,
                text=start_button_label,
                fg="#48c732",
                command=lambda: routines.async_snipe(
                    **{
                        "alt_chem_styles": int(master.alt_chem_styles.get())
                        if master.alt_chem_styles.get()
                        else 0,
                        "name": master.name.get(),
                        "quality": master.quality.get(),
                        "rarity": master.rarity.get(),
                        "chem_style": master.chem_style.get(),
                        "league": master.league.get(),
                        "position": master.position.get(),
                        "nation": master.nation.get(),
                        "club": master.club.get(),
                        "sell_player": master.lookup_sell_player_var.get(),
                        "max_price": int(master.max_price.get())
                        if master.max_price.get()
                        else 0,
                    }
                ),
            ).grid(row=0, column=0)

        tk.Button(
            self, text=stop_button_label, fg="#de190b", command=routines.stop_program
        ).grid(row=0, column=1)


class StatusTextComponent(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Status:").grid(row=0, column=0)

        self.status = tk.Label(self, text="")
        self.status.grid(row=1, column=0)


class SnipeFormComponent(tk.Frame):
    def __init__(self, master, full_routine_form=False):
        tk.Frame.__init__(self, master)

        tk.Label(self, text="Name:").grid(row=0, column=0)
        self.name = tk.Entry(self)
        self.name.grid(row=0, column=1, pady=20, padx=10)

        tk.Label(self, text="Rarity:").grid(row=0, column=2)
        self.rarity = tk.Entry(self)
        self.rarity.grid(row=0, column=3)

        tk.Label(self, text="Quality:").grid(row=1, column=0)
        self.quality = tk.Entry(self)
        self.quality.grid(row=1, column=1)

        tk.Label(self, text="Chem Style:").grid(row=2, column=0)
        self.chem_style = tk.Entry(self)
        self.chem_style.grid(row=2, column=1)

        tk.Label(self, text="League:").grid(row=3, column=0, pady=(0, 30))
        self.league = tk.Entry(self)
        self.league.grid(row=3, column=1, pady=(0, 35))

        tk.Label(self, text="Position:").grid(row=1, column=2)
        self.position = tk.Entry(self)
        self.position.grid(row=1, column=3, padx=10)

        tk.Label(self, text="Nation:").grid(row=2, column=2)
        self.nation = tk.Entry(self)
        self.nation.grid(row=2, column=3)

        tk.Label(self, text="Club:").grid(row=3, column=2, pady=(0, 35))
        self.club = tk.Entry(self)
        self.club.grid(row=3, column=3, pady=(0, 35))

        tk.Label(self, text="Alternate Chem Styles:").grid(row=4, column=0)
        self.alt_chem_styles = tk.Entry(self)
        self.alt_chem_styles.grid(row=4, column=1)

        tk.Label(self, text="Max Price:").grid(row=4, column=2)
        self.max_price = tk.Entry(self)
        self.max_price.grid(row=4, column=3)

        self.lookup_sell_player_var = tk.IntVar()
        tk.Label(self, text="Do not sell players:").grid(row=5, column=0)
        self.sell_player = tk.Checkbutton(self, variable=self.lookup_sell_player_var)
        self.sell_player.grid(row=5, column=1)

        StartStopComponent(self, full_routine_form).grid(
            row=9, column=0, columnspan=4, pady=20
        )

        tk.Label(self, text="Status:").grid(row=10, column=0)

        tk.Label(self, text="Total Players Bought:").grid(row=11, column=0)
        tk.Label(self, text="Total Profit:").grid(row=12, column=0)

        self.lbl_total_players = tk.Label(self, text="0", relief="groove", width=6)
        self.lbl_total_players.config(font=("Arial", 24))
        self.lbl_total_players.grid(row=11, column=1)

        self.lbl_total_profit = tk.Label(self, text="0", relief="groove", width=6)
        self.lbl_total_profit.config(font=("Arial", 24))
        self.lbl_total_profit.grid(row=12, column=1)
