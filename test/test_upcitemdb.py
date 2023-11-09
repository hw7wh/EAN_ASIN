# RUN AS STANDALONE TO TEST HTTP CLIENT FOR 2nd public data source : curl_cffi is great
# NEED TO TEST ON 100 calls NEXT

from curl_cffi.requests import Session
from bs4 import BeautifulSoup
import time
import random

USER_AGENT_LIST = [
    'chrome99',
    'chrome100',
    'chrome101',
    'chrome104',
    'chrome107',
    'chrome110',
    'chrome99_android',
    'edge99',
    'edge101',
    'safari15_3',
    'safari15_5',
]

EAN_LISTS = [
    '7090810607592',
    '8414606648139',
    '8414606648146',
    '8425402731994',
    '8425402731871',
    '8425402731888',
    '4260168660126',
    '8545454545452',
    '733739017574',
    '8436540532275',
    '733739031709',
    '5400713802758',
    '8436540531780',
    '8436540532909',
    '8436540533715',
    '8436540534071',
    '733739047212',
    '8587324529063'
]

url = 'https://www.upcitemdb.com/upc/'

impersonate = 'chrome110'

if __name__ == '__main__':
    try:
        with Session(impersonate=impersonate) as session:
            for ean in EAN_LISTS:
                response = session.get(url + ean)
                print(f'Connecting to {ean}...')
                soup = BeautifulSoup(response.content, 'html.parser')
                table_elme = soup.select_one('table.detail-list')
                if table_elme:
                    print(table_elme.text)
                    print(
                        '---------------------------------------------------------------\n\n\n')
                time.sleep(random.uniform(1, 3))
    except Exception as e:
        print(f'Error : {e}')
