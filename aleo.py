import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup


COINBASE_MIN = 1
INCENTIVES_MIN = 0.01
SOLUTIONS_MIN = 2
SLEEP_TIME_SEC = 360

API_TOKEN = "2109:AA-LL_EEOO"
CHAT_ID = "-1703"
ADDRESSES = {
    "num1-serv1": "aleo...address1",
    "num2-serv2": "aleo...address2",
}

def send_tg_msg(value: str):
    try:
        requests.post(
            f"https://api.telegram.org/bot{API_TOKEN}/sendMessage",
            json={
                'chat_id': CHAT_ID,
                'text': value
            }
        )
    except Exception as e:
        print(e.args)


def get_match(soup: str):
    try:
        return float(re.match(r'\d+.\d+', soup)[0])
    except:
        return float(re.match(r'\d+', soup)[0])


def get_row_items(row: bs4.element.ResultSet):
    return get_match(soup=row[0].get_text()), get_match(soup=row[0].get_text())


def get_address_result(page: requests.Response):
    soup = BeautifulSoup(page.content, 'html.parser')
    address_table = soup.findAll('div', {'class': 'address-second-table'})

    solution_row = address_table[1].findAll('span', {'class': 'light-blue-number'})
    blocks, solutions = get_row_items(row=solution_row)

    credit_row = address_table[1].findAll('span', {'class': 'text-aleo-green'})
    incentives, coinbase = get_row_items(row=credit_row)
    return blocks, solutions, incentives, coinbase


def work():
    session = requests.session()
    for address in ADDRESSES.items():
        dt = datetime.now().strftime("%H:%M:%S")
        page = session.get(f"https://www.aleo.network/leaderboard/{address[1]}")
        if "No matching results" in page.text:
            print(f'[{dt}] | [{address[0]}] - [{address[1][-4:]}] | nothing...')
        else:
            blocks, solutions, incentives, coinbase = get_address_result(page=page)
            message = f'[{dt}] | [{address[0]}] - [{address[1][-4:]}] | ' \
                      f'incentives: {round(incentives, 2)}, ' \
                      f'coinbase: {round(coinbase, 2)}, ' \
                      f'blocks: {blocks}, ' \
                      f'solutions: {solutions}.'

            if coinbase > COINBASE_MIN and incentives > INCENTIVES_MIN and solutions > SOLUTIONS_MIN:
                print(message + 'DONE!')
                send_tg_msg(value=message)
            else:
                print(message)

    time.sleep(SLEEP_TIME_SEC)


if __name__ == '__main__':
    while True:
        work()

