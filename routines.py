from filter import Filter
from selenium_session import SeleniumSession
from filter_controller import FilterController
from utils import *
import threading
from program_state import ProgramState
from screens import SellScreen, SnipeScreen

def call_login(credentials):
    login(ProgramState.selenium_instance.getWebDriver(), credentials)

def async_sell_players(lbl):
    ProgramState.switch_thread(sell_cards, {"log_field" : lbl})

def async_snipe(**kwargs):
    ProgramState.switch_thread(snipe, kwargs)

def current_screen(screen):
    print(type(ProgramState.screen_controller._frame))
    print(screen)

    return type(ProgramState.screen_controller._frame) == screen

def sell_cards(log_field):
    if current_screen(SellScreen): log_field.configure(text="Going to transfers") 
    retry_cmd(goto_transfers, 1, 0, ProgramState.selenium_instance.getWebDriver())
    if current_screen(SellScreen): log_field.configure(text="Going to tradepile")
    retry_cmd(goto_tradepile, 0, 0, ProgramState.selenium_instance.getWebDriver())
    if current_screen(SellScreen): log_field.configure(text="Removing sold cards")
    retry_cmd(remove_sold, 1, 3, ProgramState.selenium_instance.getWebDriver())
    wait_loading(ProgramState.selenium_instance.getWebDriver(), 2)
    if current_screen(SellScreen): log_field.configure(text="Seling tradepile players")
    sell_tradepile_players(ProgramState.selenium_instance.getWebDriver())
    if current_screen(SellScreen): log_field.configure(text="All players sold")

def snipe(
    alt_positions, 
    alt_chem_styles,
    pos_mod_price, 
    quality, 
    chem_style, 
    league, 
    position, 
    nation,
    club, 
    max_price,
    lbl_total_players,
    lbl_total_profit):
    counter = 0
    tradepile_size = 0
    max_tradepile_size = 100
    cards_got = 0
    total_spent = 0
    total_earns = 0

    search_filter = Filter()
    
    controller = FilterController(
        alt_positions=alt_positions, 
        alt_chem_styles=alt_chem_styles,
        pos_mod_price=pos_mod_price, 
        target_max_price=max_price
    )

    retry_cmd(goto_transfers, 0, 0, ProgramState.selenium_instance.getWebDriver())
    tradepile_size = retry_cmd(get_tradepile_size, 1, 0, ProgramState.selenium_instance.getWebDriver())
    retry_cmd(goto_transfer_search, 0, 0, ProgramState.selenium_instance.getWebDriver())

    search_filter.update(
        ProgramState.selenium_instance.getWebDriver(), 
        quality=("Qualidade", quality),
        chem_style=("Estilos Entrosam.", chem_style), 
        league=("Liga", league),
        position=("Posição", position),
        nation=("Nacionalidade", nation),
        club=("Clube", club),
        max_price=("Máx.:", max_price)
    )

    while tradepile_size < max_tradepile_size:
        retry_cmd(confirm_search, 0, 0, ProgramState.selenium_instance.getWebDriver())

        result = buy_card(ProgramState.selenium_instance.getWebDriver(), sell=True)

        if result:
            tradepile_size += 1
            cards_got += 1
            total_spent += result[0]
            total_earns += result[1]*0.95
            if current_screen(SnipeScreen): lbl_total_players.configure(text=f"Total Players Bought : {str(cards_got)}")
            if current_screen(SnipeScreen): lbl_total_profit.configure(text=f"Total Profit : {str(total_earns-total_spent)}")
        
        retry_cmd(back_transfer_search, 0, 0, ProgramState.selenium_instance.getWebDriver())
        controller.manage_filter(ProgramState.selenium_instance.getWebDriver(), counter, search_filter)
        counter += 1