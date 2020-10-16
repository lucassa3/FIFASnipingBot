import threading
import time

from model.filter import Filter
from model.selenium_session import SeleniumSession
from model.filter_controller import FilterController
from controller.program_state import ProgramState
from view.sell_screen import SellScreen
from view.snipe_screen import SnipeScreen
from view.full_routine_screen import FullRoutineScreen
from view.farm_bronze_pack_screen import BronzePackFarmScreen
from model.utils import (
    login,
    retry_cmd,
    goto_transfers,
    goto_tradepile,
    remove_sold,
    wait_loading,
    sell_tradepile_players,
    goto_store,
    goto_bronze_packs,
    buy_base_bronze_pack,
    confirm_dialog,
    deal_with_bronze_items,
    get_tradepile_size,
    goto_transfer_search,
    find_click_reset_filter_btn,
    confirm_search,
    buy_card,
    back_transfer_search,
)


def call_login(credentials):
    login(ProgramState.selenium_instance.get_web_driver(), credentials)


def async_snipe(**kwargs):
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
    web_driver = ProgramState.selenium_instance.get_web_driver()
    log = ProgramState.screen_controller.log_text

    log([SellScreen], "Going to transfers")
    retry_cmd(goto_transfers, 1, 0, web_driver)

    log([SellScreen], "Going to tradepile")
    retry_cmd(goto_tradepile, 0, 0, web_driver)

    log([SellScreen], "Removing sold cards")
    retry_cmd(remove_sold, 1, 3, web_driver)
    wait_loading(web_driver, 2)

    log([SellScreen], "Selling cards")
    sell_tradepile_players(web_driver)

    log([SellScreen], "All cards listed")


def farm_bronze_packs_sync_routine():
    web_driver = ProgramState.selenium_instance.get_web_driver()
    log = ProgramState.screen_controller.log_text

    while True:
        log([BronzePackFarmScreen], "Going to store")
        retry_cmd(goto_store, 1, 0, web_driver)
        log([BronzePackFarmScreen], "Going to bronze packs")
        retry_cmd(goto_bronze_packs, 0, 0, web_driver)
        log([BronzePackFarmScreen], "Buying a bronze pack")
        retry_cmd(buy_base_bronze_pack, 0, 0, web_driver)
        retry_cmd(confirm_dialog, 0, 0, web_driver)
        time.sleep(8)
        log([BronzePackFarmScreen], "Dealing with the items")
        deal_with_bronze_items(web_driver)
        time.sleep(5)


def snipe(
    alt_chem_styles,
    name,
    quality,
    rarity,
    chem_style,
    league,
    position,
    nation,
    club,
    max_price,
    sell_player,
):
    counter = 0
    tradepile_size = 0
    max_tradepile_size = 100
    cards_got = 0
    total_spent = 0
    total_earns = 0

    web_driver = ProgramState.selenium_instance.get_web_driver()

    search_filter = Filter()

    controller = FilterController(
        alt_chem_styles=alt_chem_styles, target_max_price=max_price
    )

    retry_cmd(goto_transfers, 0, 0, web_driver)
    tradepile_size = retry_cmd(get_tradepile_size, 1, 0, web_driver)
    retry_cmd(goto_transfer_search, 0, 0, web_driver)

    retry_cmd(
        find_click_reset_filter_btn,
        0,
        0,
        web_driver,
    )

    search_filter.update(
        web_driver,
        name=("Name", name),
        quality=("Qualidade", quality),
        rarity=("Raridade", rarity),
        chem_style=("Estilos Entrosam.", chem_style),
        league=("Liga", league),
        position=("Posição", position),
        nation=("Nacionalidade", nation),
        club=("Clube", club),
        max_price=("Máx.:", max_price),
    )

    while tradepile_size < max_tradepile_size:
        retry_cmd(confirm_search, 0, 0, web_driver)

        if sell_player == 1:
            result = buy_card(web_driver, sell=False)
        else:
            result = buy_card(web_driver, sell=True)

        if counter > 0 and counter % 25 == 0:
            time.sleep(5)

        if result:
            cards_got += 1
            total_spent += result[0]
            total_earns += result[1] * 0.95
            if result[1] * 0.95 - result[0] > 0:
                tradepile_size += 1

            if current_screen([SnipeScreen, FullRoutineScreen]):
                get_frame().snipe_form_component.lbl_total_players.configure(
                    text=f"{str(cards_got)}"
                )
            if current_screen([SnipeScreen, FullRoutineScreen]):
                get_frame().snipe_form_component.lbl_total_profit.configure(
                    text=f"{str(int(total_earns-total_spent))}"
                )

        retry_cmd(back_transfer_search, 0, 0, web_driver)
        controller.manage_filter(web_driver, counter, search_filter)
        counter += 1