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


def send_tg_msg(message: str):
    try:
        requests.post(
            f"https://api.telegram.org/bot{API_TOKEN}/sendMessage",
            json={
                'chat_id': CHAT_ID,
                'text': message
            }
        )
    except Exception as e:
        print(e.args)


while True:
    session = requests.session()
    for address in ADDRESSES.items():
        dt = datetime.now().strftime("%H:%M:%S")
        page = session.get(f"https://www.aleo.network/leaderboard/{address[1]}")
        if "No matching results" in page.text:
            print(f'[{dt}] [{address[0]}] - [{address[1][-4:]}] | nothing...')
        else:
            soup = BeautifulSoup(page.content, 'html.parser')
            address_row = soup.findAll('div', {'class': 'address-second-table'})

            solution_result = address_row[1].findAll('span', {'class': 'light-blue-number'})
            blocks = int(re.match(r'\d+', solution_result[0].get_text())[0])
            solutions = int(re.match(r'\d+', solution_result[1].get_text())[0])

            credit_result = address_row[1].findAll('span', {'class': 'text-aleo-green'})
            try:
                incentives = float(re.match(r'\d+.\d+', credit_result[0].get_text())[0])
            except:
                incentives = float(re.match(r'\d+', credit_result[0].get_text())[0])
            try:
                coinbase = float(re.match(r'\d+.\d+', credit_result[1].get_text())[0])
            except:
                coinbase = float(re.match(r'\d+', credit_result[1].get_text())[0])

            message = f'[{dt}] [{address[0]}]-[{address[1][-4:]}] | ' \
                      f'coinbase: {coinbase}, ' \
                      f'blocks: {blocks}, ' \
                      f'solutions: {solutions}.'
            print(message)
            if coinbase > COINBASE_MIN and incentives > INCENTIVES_MIN and solutions > SOLUTIONS_MIN:
                send_tg_msg(message)

    time.sleep(SLEEP_TIME_SEC)
