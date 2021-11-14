import time as t
import random
from selenium.webdriver.common.keys import Keys
from state.program_state import State
from utils import retry as r


def find_click_login_btn(d):
    btn = d.find_elements_by_class_name("call-to-action")
    if len(btn) > 0:
        if "disabled" not in btn[0].get_attribute("class"):
            r.retry(btn[0].click, 0.1, 2)
            return "clicked_btn"
        else:
            return False
    return False


def check_if_loading(d):
    loading = d.find_elements_by_class_name("loaderIcon")
    if len(loading) > 0:
        if loading[0].get_attribute("style") == "":
            return "is_loading"
        else:
            return False
    return False


def find_login_form(d):
    elem = d.find_elements_by_id("email")
    if len(elem) > 0:
        return "found_login"
    else:
        return False


def login(d, credentials):
    # check whether its already logged in or needs to click the btn
    state = None
    while not state:
        clicked_btn = find_click_login_btn(d)
        if clicked_btn:
            state = clicked_btn

        is_loading = check_if_loading(d)
        if is_loading:
            state = is_loading

        t.sleep(1)

    if state == "clicked_btn":  # it means i needed to click
        state = None
        while not state:
            is_in_form = find_login_form(d)
            if is_in_form:
                state = is_in_form
                email = d.find_element_by_id("email")
                password = d.find_element_by_id("password")
                with open(credentials) as f:
                    cr = f.readlines()
                    if email.get_attribute("value") == "":
                        email.send_keys(cr[0])
                    password.send_keys(cr[1])
                t.sleep(2)
                d.find_element_by_id("logInBtn").click()

            is_loading = check_if_loading(d)
            if is_loading:
                state = is_loading

            t.sleep(1)


def logout(d):
    wait_loading(d, 1)
    d.find_element_by_class_name("icon-settings").click()
    t.sleep(1)
    d.find_element_by_xpath(
        "//*[contains(text(), 'Desconectar')]"
    ).find_element_by_xpath("..").click()
    t.sleep(1)
    d.find_elements_by_xpath("//*[contains(text(), 'Desconectar')]")[1].click()


def goto_transfers(d):
    d.find_element_by_class_name("icon-transfer").click()


def goto_store(d):
    d.find_element_by_class_name("icon-store").click()


def goto_packs(d):
    d.find_element_by_class_name("packs-tile").click()


def get_tradepile_size(d):
    size = (
        d.find_element_by_class_name("ut-tile-transfer-list")
        .find_element_by_class_name("total-transfers")
        .find_element_by_class_name("value")
        .text
    )
    return int(size)


def goto_transfer_search(d):
    d.find_elements_by_class_name("col-1-1")[1].click()


def goto_tradepile(d):
    d.find_element_by_class_name("ut-tile-transfer-list").click()


def goto_bronze_packs(d):
    d.find_element_by_class_name("menu-container").find_element_by_xpath(
        ".//*[contains(text(), 'PACOTES CLÁSSICOS')]"
    ).click()


def find_click_list_btn(d):
    d.find_element_by_class_name("ui-layout-right").find_element_by_class_name(
        "ut-quick-list-panel-view"
    ).find_element_by_class_name("accordian").click()


def find_click_cmp_btn(d):
    d.find_element_by_class_name("ui-layout-right").find_element_by_xpath(
        ".//*[contains(text(), 'Comparar')]"
    ).find_element_by_xpath("..").click()


def find_click_back_btn(d):
    d.find_element_by_class_name("ui-layout-right").find_element_by_xpath(
        ".//*[contains(text(), 'Resultados da Busca')]"
    ).find_element_by_xpath("..").find_element_by_class_name(
        "ut-navigation-button-control"
    ).click()


def sell_item(d):
    r.retry(find_click_cmp_btn, 0.1, 0, d)

    sell_price = find_lowest_price(d)

    r.retry(find_click_back_btn, 0.1, 0, d)
    t.sleep(0.5)

    r.retry(find_click_list_btn, 0.1, 0, d)
    wait_loading(d)
    t.sleep(0.2)

    # escreve preco min: 9000000 (default)
    init_price_box = (
        d.find_element_by_class_name("ui-layout-right")
        .find_element_by_xpath(".//*[contains(text(), 'Inicial:')]")
        .find_element_by_xpath("..")
        .find_element_by_xpath("..")
        .find_element_by_class_name("numericInput")
    )
    t.sleep(0.15)
    r.retry(init_price_box.send_keys, 0.02, 0, Keys.CONTROL + "a")
    r.retry(init_price_box.send_keys, 0.02, 0, Keys.DELETE)
    t.sleep(0.2)
    r.retry(init_price_box.send_keys, 0.02, 0, "9000000")

    # escreve preco venda: min_price
    imm_price_box = (
        d.find_element_by_class_name("ui-layout-right")
        .find_element_by_xpath(".//*[contains(text(), 'Imediato:')]")
        .find_element_by_xpath("..")
        .find_element_by_xpath("..")
        .find_element_by_class_name("numericInput")
    )
    t.sleep(0.15)
    r.retry(imm_price_box.send_keys, 0.02, 0, Keys.CONTROL + "a")
    r.retry(imm_price_box.send_keys, 0.02, 0, Keys.DELETE)
    t.sleep(0.2)
    r.retry(imm_price_box.send_keys, 0.02, 0, str(sell_price))

    list_btn = d.find_element_by_class_name("ui-layout-right").find_element_by_xpath(
        ".//*[contains(text(), 'Listar para') and not(contains(text(), 'novamente'))]"
    )
    r.retry(list_btn.click, 0, 0)

    return sell_price


def remove_sold(d):
    d.find_element_by_xpath(
        "//*[contains(text(), 'Retirar vendidos')]"
    ).find_element_by_xpath("..").find_element_by_class_name("call-to-action").click()


def get_expired_cards(d):
    expired_cards = (
        d.find_element_by_xpath("//*[contains(text(), 'Itens não vend.')]")
        .find_element_by_xpath("..")
        .find_element_by_xpath("..")
        .find_element_by_class_name("itemList")
        .find_elements_by_class_name("listFUTItem")
    )

    return expired_cards


def get_available_cards(d):
    available_cards = (
        d.find_element_by_xpath("//*[contains(text(), 'Itens disponíveis')]")
        .find_element_by_xpath("..")
        .find_element_by_xpath("..")
        .find_element_by_class_name("itemList")
        .find_elements_by_class_name("listFUTItem")
    )

    return available_cards


def sell_tradepile_players(d):
    expired_cards = r.retry(get_expired_cards, 0.5, 0, d)[0]
    wait_loading(d)
    while len(expired_cards) > 0:
        card = expired_cards[0]
        r.retry(card.click, 0.1, 0)
        sell_item(d)

        next_expired_cards_len = len(expired_cards)
        while next_expired_cards_len == len(expired_cards):
            next_expired_cards = r.retry(get_expired_cards, 0.5, 0, d)[0]
            next_expired_cards_len = len(next_expired_cards)
        expired_cards = next_expired_cards

    t.sleep(1)
    available_cards = r.retry(get_available_cards, 0, 0, d)[0]
    while len(available_cards) > 0:
        card = available_cards[0]
        r.retry(card.click, 0.1, 0)
        sell_item(d)

        next_available_cards_len = len(available_cards)
        while next_available_cards_len == len(available_cards):
            next_available_cards = r.retry(get_available_cards, 0.5, 0, d)[0]
            next_available_cards_len = len(next_available_cards)
        available_cards = next_available_cards


def find_click_filter(d, filter_name=""):
    d.find_element_by_class_name("ut-pinned-list").find_element_by_xpath(
        f".//*[contains(text(), '{filter_name}')]"
    ).find_element_by_xpath("..").find_element_by_xpath("..").click()


def find_textbox_filter(d, filter_name=""):
    fil = (
        d.find_element_by_class_name("ut-pinned-list")
        .find_elements_by_xpath(f".//*[contains(text(), '{filter_name}')]")[1]
        .find_element_by_xpath("..")
        .find_element_by_xpath("..")
        .find_element_by_class_name("numericInput")
    )
    return fil


def find_playername_filter(d):
    fil = d.find_element_by_xpath("//input[@placeholder='Digite o Nome do Jogador']")
    return fil


def select_playername_filter(d, name):
    fil = r.retry(find_playername_filter, 0.02, 0, d)[0]
    fil.send_keys(name)
    t.sleep(0.7)
    d.find_element_by_xpath(f"//*[contains(text(), '{name}')]").click()


def get_max_price_textbox(d):
    fil = r.retry(find_textbox_filter, 0.02, 0, d, "Máx.:")[0].get_attribute("value")
    return int(fil.replace(".", "")) if fil != "" else 0


def get_min_price_textbox(d):
    fil = r.retry(find_textbox_filter, 0.02, 0, d, "Mín.:")[0].get_attribute("value")
    return int(fil.replace(".", "")) if fil != "" else 0


def cancel_filter(d, filter_name=""):
    d.find_element_by_xpath(
        f"//*[contains(text(), '{filter_name}')]"
    ).find_element_by_xpath("..").find_element_by_class_name("flat").click()


def select_filter(d, filter_name="", value=""):
    r.retry(find_click_filter, 0.02, 0, d, filter_name)
    r.retry(d.find_element_by_xpath(f"//*[contains(text(), '{value}')]").click, 0.02, 0)


def select_textbox_filter(d, filter_name="", value=""):
    fil = r.retry(find_textbox_filter, 0.02, 0, d, filter_name)[0]
    r.retry(fil.send_keys, 0.02, 0, str(value))


def find_click_inc_min_price(d):
    d.find_elements_by_xpath("//*[contains(text(), 'Mín.:')]")[1].find_element_by_xpath(
        ".."
    ).find_element_by_xpath("..").find_element_by_class_name("increment-value").click()


def find_click_dec_min_price(d):
    d.find_elements_by_xpath("//*[contains(text(), 'Mín.:')]")[1].find_element_by_xpath(
        ".."
    ).find_element_by_xpath("..").find_element_by_class_name("decrement-value").click()


def find_click_inc_max_price(d):
    d.find_elements_by_xpath("//*[contains(text(), 'Máx.:')]")[1].find_element_by_xpath(
        ".."
    ).find_element_by_xpath("..").find_element_by_class_name("increment-value").click()


def find_click_dec_max_price(d):
    d.find_elements_by_xpath("//*[contains(text(), 'Máx.:')]")[1].find_element_by_xpath(
        ".."
    ).find_element_by_xpath("..").find_element_by_class_name("decrement-value").click()


def confirm_search(d):
    d.find_element_by_class_name("call-to-action").click()


def back_transfer_search(d):
    d.find_element_by_class_name("ut-navigation-bar-view").find_element_by_class_name(
        "ut-navigation-button-control"
    ).click()


def find_click_reset_filter_btn(d):
    d.find_element_by_xpath("//*[contains(text(), 'Redefinir')]").click()


def wait_loading(d, wait_extra=0):
    ready = False
    while not ready:
        loading = d.find_element_by_class_name("loaderIcon").get_attribute("style")
        if loading != "":
            ready = True
        t.sleep(0.05)
    t.sleep(wait_extra)


def get_card_prices(d):
    price_list = []
    card_list = (
        d.find_element_by_class_name("ui-layout-right")
        .find_element_by_class_name("paginated-item-list")
        .find_elements_by_xpath(".//*[contains(text(), 'Comprar')]")
    )

    for card in card_list:
        price = (
            card.find_element_by_xpath("..")
            .find_element_by_class_name("currency-coins")
            .text
        )

        price = int(str(price).replace(".", ""))
        price_list.append(price)

    return price_list


def find_click_next_btn(d):
    d.find_element_by_class_name("ui-layout-right").find_element_by_class_name(
        "paginated-item-list"
    ).find_element_by_class_name("next").click()


def calc_interval(value):
    if value <= 1000:
        return 50
    elif value > 1000 and value <= 10000:
        return 100
    else:
        return 250


def find_lowest_price(d, num_pages=3, good_price=600):
    min_price = 9000000
    for i in range(num_pages):
        wait_loading(d)
        t.sleep(2)
        price_list = r.retry(get_card_prices, 0.2, 0, d)[0]

        for price in price_list:
            if price < min_price:
                min_price = price

        if i != num_pages - 1:
            if not (r.retry(find_click_next_btn, 0.2, 4, d)[2]):
                break

    if min_price <= good_price:
        return min_price
    else:
        return min_price - calc_interval(min_price)


def check_status_buy(d, idx_sel_card):
    status = None
    # todo: cant stop thread while executing this
    while status is None:
        card_status = (
            d.find_element_by_class_name("paginated-item-list")
            .find_elements_by_class_name("rowContent")[idx_sel_card]
            .find_element_by_xpath("..")
            .get_attribute("class")
        )

        if "won" in card_status:
            status = "won"

        if r.retry(negative_notification, 0.1, 2, d)[2]:
            status = "expired"

    return status


def find_buy_btn(d):
    d.find_element_by_class_name("ui-layout-right").find_element_by_class_name(
        "buyButton"
    )


def find_click_buy_btn(d):
    d.find_element_by_class_name("ui-layout-right").find_element_by_class_name(
        "buyButton"
    ).click()


def confirm_dialog(d):
    d.find_element_by_class_name("view-modal-container").find_element_by_xpath(
        ".//*[contains(text(), 'OK')]"
    ).click()


def select_buy_card(d):
    card_list = d.find_element_by_class_name(
        "paginated-item-list"
    ).find_elements_by_class_name("rowContent")

    card_rand_idx = random.randint(0, len(card_list) - 1)
    card_list[card_rand_idx].click()

    return card_rand_idx


def find_no_results(d):
    d.find_element_by_class_name("ut-no-results-view")


def negative_notification(d):
    d.find_element_by_id("NotificationLayer").find_element_by_class_name("negative")


def input_name(d, player_name):
    player_name_box = d.find_element_by_class_name(
        "ut-player-search-control"
    ).find_element_by_xpath(".//*[@placeholder='Digite o Nome do Jogador']")

    r.retry(player_name_box.send_keys, 0.02, 0, Keys.CONTROL + "a")
    r.retry(player_name_box.send_keys, 0.02, 0, Keys.DELETE)

    r.retry(player_name_box.send_keys, 0.02, 0, player_name)

    click_name_btn = r.retry(find_player_name_btn, 0.02, 0, d)[0]

    r.retry(click_name_btn.click, 0.02, 0)


def find_player_name_btn(d):
    return (
        d.find_element_by_class_name("ut-player-search-control")
        .find_element_by_class_name("inline-list")
        .find_elements_by_class_name("btn-text")[0]
        .find_element_by_xpath("..")
    )


def send_player_to_club(d):
    d.find_element_by_class_name("ui-layout-right").find_element_by_xpath(
        ".//*[contains(text(), 'Enviar ao Meu Clube')]"
    ).find_element_by_xpath("..").click()


def buy_base_bronze_pack(d):
    d.find_element_by_class_name("ut-store-pack-details-view").find_element_by_xpath(
        ".//*[contains(text(), '750')]"
    ).find_element_by_xpath("..").click()


def find_item_list(d, cur_list):
    item_list = d.find_element_by_class_name("itemList").find_elements_by_class_name(
        "listFUTItem"
    )

    if len(item_list) <= 0:
        raise ValueError("did not expect this list size!")
    elif cur_list and (cur_list[0].id == item_list[0].id):
        raise ValueError("its the same list!")

    return item_list


def is_player(card):
    return (
        True
        if len(
            card.find_elements_by_xpath(
                ".//*[contains(text(), 'RIT') or contains(text(), 'POS')]"
            )
        )
        != 0
        else False
    )


def deal_with_bronze_items(d):
    items = r.retry(find_item_list, 0.2, 0, d, [])[0]
    wait_loading(d)

    i = 0
    while (len(items) > 0) and (i < len(items)):
        card = items[i]
        r.retry(card.click, 0.1, 0)
        if maybe_sell_item(d, card):
            t.sleep(2)
            items = r.retry(find_item_list, 0.2, 0, d, items)[0]
        else:
            t.sleep(0.5)
            i += 1

    t.sleep(0.5)
    r.retry(sell_duplicates_if_present, 0.1, 4, d)
    r.retry(store_remaining_cards_if_present, 0.1, 4, d)


def sell_duplicates_if_present(d):
    d.find_elements_by_xpath("//*[contains(text(), 'duplicata')]")[
        0
    ].find_element_by_xpath("..").click()
    t.sleep(1)
    confirm_dialog(d)


def store_remaining_cards_if_present(d):
    d.find_element_by_xpath("//*[contains(text(), 'Guardar tudo')]").click()


def maybe_sell_item(d, card):
    coin_card, _, exists = r.retry(
        d.find_element_by_xpath, 0.2, 0.7, "//*[contains(text(), 'Resgatar ')]"
    )
    if exists:
        t.sleep(1.5)
        coin_card.find_element_by_xpath("..").click()
        t.sleep(1.5)
        return False

    if not is_player(card):
        return False

    r.retry(find_click_cmp_btn, 0.1, 0, d)

    sell_price = find_price_or_quit(d)

    if sell_price == 0:
        return False

    r.retry(find_click_back_btn, 0.1, 0, d)
    t.sleep(0.5)

    r.retry(find_click_list_btn, 0.1, 0, d)
    wait_loading(d)
    t.sleep(0.2)

    # escreve preco min: 9000000 (default)
    init_price_box = (
        d.find_element_by_class_name("ui-layout-right")
        .find_element_by_xpath(".//*[contains(text(), 'Inicial:')]")
        .find_element_by_xpath("..")
        .find_element_by_xpath("..")
        .find_element_by_class_name("numericInput")
    )
    t.sleep(0.15)
    r.retry(init_price_box.send_keys, 0.02, 0, Keys.CONTROL + "a")
    r.retry(init_price_box.send_keys, 0.02, 0, Keys.DELETE)
    t.sleep(0.2)
    r.retry(init_price_box.send_keys, 0.02, 0, "9000000")

    # escreve preco venda: min_price
    imm_price_box = (
        d.find_element_by_class_name("ui-layout-right")
        .find_element_by_xpath(".//*[contains(text(), 'Imediato:')]")
        .find_element_by_xpath("..")
        .find_element_by_xpath("..")
        .find_element_by_class_name("numericInput")
    )
    t.sleep(0.15)
    r.retry(imm_price_box.send_keys, 0.02, 0, Keys.CONTROL + "a")
    r.retry(imm_price_box.send_keys, 0.02, 0, Keys.DELETE)
    t.sleep(0.2)
    r.retry(imm_price_box.send_keys, 0.02, 0, str(sell_price))

    list_btn = d.find_element_by_class_name("ui-layout-right").find_element_by_xpath(
        ".//*[contains(text(), 'Listar para') and not(contains(text(), 'novamente'))]"
    )
    r.retry(list_btn.click, 0, 0)

    return sell_price


def find_price_or_quit(d, num_pages=3, good_price=450):
    min_price = 9000000
    for i in range(num_pages):
        wait_loading(d)
        price_list = []
        while len(price_list) == 0:
            price_list = r.retry(get_card_prices, 0.2, 0, d)[0]

        for price in price_list:
            if price < min_price:
                min_price = price

            if price < 400:
                return 0

        if i != num_pages - 1:
            if not (r.retry(find_click_next_btn, 0.2, 4, d)[2]):
                break

        t.sleep(1)

    if min_price <= good_price:
        return min_price
    else:
        return min_price - calc_interval(min_price)


def already_in_club(d):
    return (
        True
        if len(
            d.find_element_by_class_name("ui-layout-right").find_elements_by_xpath(
                ".//*[contains(text(), 'Trocar duplicata do clube')]"
            )
        )
        > 0
        else False
    )


def buy_card(d, sell=True):
    _, fname, _ = r.retry_many([find_buy_btn, find_no_results], 0, 0, [[d], [d]])

    if fname == "find_buy_btn":
        idx = r.retry(select_buy_card, 0, 0, d)[0]
        r.retry(find_click_buy_btn, 0, 0, d)
        r.retry(confirm_dialog, 0, 10, d)
        t.sleep(1.6)
        status = check_status_buy(d, idx)

        if status == "expired":
            t.sleep(0.5)
            return None
        else:
            if r.retry(negative_notification, 0.2, 1, d)[2]:
                t.sleep(0.5)
                return None
            bought_price = int(
                d.find_element_by_class_name("subContent").text.replace(".", "")
            )
            t.sleep(0.5)
            if sell:
                sold_price = sell_item(d)
                t.sleep(0.5)
                return (bought_price, sold_price)
            else:
                if not already_in_club(d):
                    send_player_to_club(d)
                    t.sleep(0.5)
                    return (bought_price, 0)
                else:
                    sold_price = sell_item(d)
                    t.sleep(0.5)
                    return (bought_price, sold_price)

    elif fname == "find_no_results":
        wait_loading(d, 0)
        return


def increase_min_imm(value, desired_min, desired_max, increase):
    """
    True if min immediate value needs to be increased... else False
    """
    if value == desired_min:
        increase = True
    elif value == desired_max - calc_interval(value):
        increase = False
