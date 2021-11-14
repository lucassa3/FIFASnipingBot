import threading
import time

from model.filter import Filter
from model.filter_controller import FilterController
from state.program_state import State
from view.sell_screen import SellScreen
from view.snipe_screen import SnipeScreen
from view.full_routine_screen import FullRoutineScreen
from view.farm_bronze_pack_screen import BronzePackFarmScreen
from model.actions import (
    goto_packs,
    login,
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

from utils import retry as r


def call_login(credentials):
    login(State.selenium_instance.get_web_driver(), credentials)


def full_routine(**kwargs):
    sell_cards()
    snipe(**kwargs)


def sell_cards():
    web_driver = State.selenium_instance.get_web_driver()
    log = State.gui_instance.log_text

    log([SellScreen], "Going to transfers")
    r.retry(goto_transfers, 1, 0, web_driver)

    log([SellScreen], "Going to tradepile")
    r.retry(goto_tradepile, 0, 0, web_driver)

    log([SellScreen], "Removing sold cards")
    r.retry(remove_sold, 1, 3, web_driver)
    wait_loading(web_driver, 2)

    log([SellScreen], "Selling cards")
    sell_tradepile_players(web_driver)

    log([SellScreen], "All cards listed")


def farm_bronze_packs():
    web_driver = State.selenium_instance.get_web_driver()
    log = State.gui_instance.log_text

    while True:
        log([BronzePackFarmScreen], "Going to store")
        r.retry(goto_store, 1, 0, web_driver)

        log([BronzePackFarmScreen], "Going to packs")
        r.retry(goto_packs, 1, 0, web_driver)
        
        log([BronzePackFarmScreen], "Going to bronze packs")
        r.retry(goto_bronze_packs, 0, 0, web_driver)

        log([BronzePackFarmScreen], "Buying a bronze pack")
        r.retry(buy_base_bronze_pack, 0, 0, web_driver)
        r.retry(confirm_dialog, 0, 0, web_driver)
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

    web_driver = State.selenium_instance.get_web_driver()
    log_total_cards = State.gui_instance.update_total_cards
    log_total_profit = State.gui_instance.update_total_profit

    search_filter = Filter()

    controller = FilterController(
        alt_chem_styles=alt_chem_styles, target_max_price=max_price
    )

    r.retry(goto_transfers, 0, 0, web_driver)
    tradepile_size = r.retry(get_tradepile_size, 1, 0, web_driver)[0]
    r.retry(goto_transfer_search, 0, 0, web_driver)

    r.retry(
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
        r.retry(confirm_search, 0, 0, web_driver)

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

            log_total_cards([SnipeScreen, FullRoutineScreen], f"{str(cards_got)}")
            log_total_profit(
                [SnipeScreen, FullRoutineScreen], f"{str(int(total_earns-total_spent))}"
            )

        r.retry(back_transfer_search, 0, 0, web_driver)
        controller.manage_filter(web_driver, counter, search_filter)
        counter += 1