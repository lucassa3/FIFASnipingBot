from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import random
from utils import *

current_filters = { 
                    "Qualidade" : None,
                    "Estilos Entrosam." : None,
                    "Liga" : None,
                    "Posição" : None,
                    "Nacionalidade" : None,
                    "Clube" : None,
                    "Mín.:" : None,
                    "Máx.:" : None
                    }

inc_flag = False
tradepile_capacity = 70
tradepile_cur_size = 0

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=profile/")
d = webdriver.Chrome("chromedriver.exe", chrome_options=options)

d.set_page_load_timeout("10")
d.get("https://www.easports.com/br/fifa/ultimate-team/web-app/#")

####CONFIGS#########
quality="Ouro"
position=""
nation=""
league="Premier"
chem_style=""
max_price=400
min_price=350

swap_basic_chem = 5
swap_pos_def = 10
inc_swap_pos = True
####################
price_range = ((max_price - 150)/50) - 1

login(d, "credentials.txt")
retry_cmd(goto_transfers, 1, 0, d)


retry_cmd(goto_tradepile, 0, 0, d)
retry_cmd(remove_sold, 1, 3, d)
wait_loading(d, 2)
sell_tradepile_players(d)

print(tradepile_cur_size)
retry_cmd(goto_transfers, 0, 0, d)
tradepile_cur_size = retry_cmd(get_tradepile_size, 1, 0, d)
retry_cmd(goto_transfer_search, 0, 0, d)

select_search_filters(d, quality=quality, position=position, nation=nation, 
                      league=league, chem_style=chem_style, max_price=max_price, 
                      min_price=min_price)
counter = 0
cards_got = 0
total_spent = 0
total_earns = 0

while tradepile_cur_size < tradepile_capacity-1:
    result = buy_card(d)

    if result:
        tradepile_cur_size += 1
        cards_got += 1
        total_spent += result[0]
        total_earns += result[1]*0.95

        print(f"cartas obtidas: {cards_got}")
        print(f"vendendo por: {result[1]}")
        print(f"lucro total: {total_earns-total_spent}")

    retry_cmd(back_transfer_search, 0, 0, d)
    update_filter(d, price_range, counter=counter, swap_basic_chem=swap_basic_chem, swap_pos_def=swap_pos_def, inc_swap_pos=True)
    counter += 1
    print(tradepile_cur_size)
    if counter != 0 and counter % 60 == 0:
        print("Estou dormindo por 15 segundos")
        time.sleep(15)

time.sleep(0.5)
logout(d)