# RUN AS STANDALONE TO TEST HTTP CLIENT FOR AMAZON : curl_cffi is great

from curl_cffi.requests import Session
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

ASIN_LISTS = ['B000Z92N6K', 'B0BPY7HSC4']

URL_LIST = [
    'https://www.amazon.co.uk/dp/',
    'https://www.amazon.pl/dp/',
    'https://www.amazon.nl/dp/',
    'https://www.amazon.it/dp/',
    'https://www.amazon.fr/dp/',
    'https://www.amazon.es/dp/',
    'https://www.amazon.de/dp/',
    'https://www.amazon.se/dp/',
    'https://www.amazon.com.be/dp/',
]


impersonate = 'safari15_5'

if __name__ == '__main__':
    try:
        with Session(impersonate=impersonate) as session:
            for amazon_url in URL_LIST:
                for asin in ASIN_LISTS:
                    url = amazon_url + asin
                    response = session.get(url)
                    print(f'Connecting to {url}...')
                    print(response.ok) # TRUE if prod exists FALSE otherwise
                    print('________________________________________________________________\n\n\n\n')
                    time.sleep(random.uniform(1,3))
    except Exception as e:
        print(f'Error : {e}')
