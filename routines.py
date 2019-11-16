from filter import Filter
from selenium_session import SeleniumSession
from filter_controller import FilterController
from utils import *
import threading
from program_state import ProgramState
from screens import SellScreen, SnipeScreen, FullRoutineScreen

def call_login(credentials):
    login(ProgramState.selenium_instance.getWebDriver(), credentials)

def async_sell_players():
    ProgramState.switch_thread(sell_cards)

def async_snipe(**kwargs):
    print(kwargs["sell_player"])
    ProgramState.switch_thread(snipe, kwargs)

def async_full_routine(**kwargs):
    ProgramState.switch_thread(full_routine, kwargs)

def stop_program():
    ProgramState.stop_thread()

def full_routine(**kwargs):
    sell_cards()
    snipe(**kwargs)

def current_screen(screens):
    return type(ProgramState.screen_controller._frame) in screens

def get_frame():
    return ProgramState.screen_controller._frame

def sell_cards():
    if current_screen([SellScreen]): get_frame().sell_component.lbl.configure(text="Going to transfers") 
    retry_cmd(goto_transfers, 1, 0, ProgramState.selenium_instance.getWebDriver())
    if current_screen([SellScreen]): get_frame().sell_component.lbl.configure(text="Going to tradepile")
    retry_cmd(goto_tradepile, 0, 0, ProgramState.selenium_instance.getWebDriver())
    if current_screen([SellScreen]): get_frame().sell_component.lbl.configure(text="Removing sold cards")
    retry_cmd(remove_sold, 1, 3, ProgramState.selenium_instance.getWebDriver())
    wait_loading(ProgramState.selenium_instance.getWebDriver(), 2)
    if current_screen([SellScreen]): get_frame().sell_component.lbl.configure(text="Selling tradepile players")
    sell_tradepile_players(ProgramState.selenium_instance.getWebDriver())
    if current_screen([SellScreen]): get_frame().sell_component.lbl.configure(text="All players sold")

def snipe(
    alt_positions, 
    alt_chem_styles,
    name,
    # pos_mod_price, 
    quality, 
    chem_style, 
    league, 
    position, 
    nation,
    club, 
    max_price,
    # consumable_type,
    # chem_type
    sell_player
    ):
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
        # pos_mod_price=pos_mod_price, 
        target_max_price=max_price
    )

    retry_cmd(goto_transfers, 0, 0, ProgramState.selenium_instance.getWebDriver())
    tradepile_size = retry_cmd(get_tradepile_size, 1, 0, ProgramState.selenium_instance.getWebDriver())
    retry_cmd(goto_transfer_search, 0, 0, ProgramState.selenium_instance.getWebDriver())

    # if consumable_type:
    #     retry_cmd(goto_consumables, 0, 0, ProgramState.selenium_instance.getWebDriver())

    retry_cmd(find_click_reset_filter_btn, 0, 0, ProgramState.selenium_instance.getWebDriver())


    search_filter.update(
        ProgramState.selenium_instance.getWebDriver(),
        name=("Name", name),
        quality=("Qualidade", quality),
        chem_style=("Estilos Entrosam.", chem_style), 
        league=("Liga", league),
        position=("Posição", position),
        nation=("Nacionalidade", nation),
        club=("Clube", club),
        max_price=("Máx.:", max_price)
        # consumable_type=("Treino de Jogador", consumable_type),
        # chem_type=("Estilos Entrosam.", chem_type)
    )

    while tradepile_size < max_tradepile_size:
        retry_cmd(confirm_search, 0, 0, ProgramState.selenium_instance.getWebDriver())

        if sell_player == 1:
            result = buy_card(ProgramState.selenium_instance.getWebDriver(), sell=False)
        else:
            result = buy_card(ProgramState.selenium_instance.getWebDriver(), sell=True)

        if result:
            cards_got += 1
            total_spent += result[0]
            total_earns += result[1]*0.95
            if result[1]*0.95-result[0] > 0:
                tradepile_size += 1

            if current_screen([SnipeScreen, FullRoutineScreen]): get_frame().snipe_form_component.lbl_total_players.configure(text=f"{str(cards_got)}")
            if current_screen([SnipeScreen, FullRoutineScreen]): get_frame().snipe_form_component.lbl_total_profit.configure(text=f"{str(int(total_earns-total_spent))}")
        
        retry_cmd(back_transfer_search, 0, 0, ProgramState.selenium_instance.getWebDriver())
        controller.manage_filter(ProgramState.selenium_instance.getWebDriver(), counter, search_filter)
        counter += 1