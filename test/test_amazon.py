# WORKS PERFECTLY --> TEST MORE ASIN !!!

from curl_cffi.requests import Session
from bs4 import BeautifulSoup
import time
import random

# FOR DEBUG ONLY - printing unicode chars
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# _________________________________________________________


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

ASIN_LISTS = [
    'B000Z92N6K',
    'B0BPY7HSC4',
    'B0001VW3WQ',
    'B000GJP21C',
    'B000URVCRS',
    'B000WMV8AM',
    'B000WMWYAA',
    'B0033R1P6A',
    'B0033R5HR8',
    'B0052N2B7A',
    'B00EV2V32W',
    'B00F416S7O',
    'B00F42GDZ0',
    'B01HSH0520']


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



if __name__ == '__main__':
    try:
        for amazon_url in URL_LIST:
            for asin in ASIN_LISTS:
                impersonate = random.choice(USER_AGENT_LIST)
                with Session(impersonate=impersonate) as session:
                    url = amazon_url + asin
                    response = session.get(url)
                    print(f'Connecting to {url}...')
                    if response.ok:  # TRUE if prod exists FALSE otherwise
                        soup = BeautifulSoup(response.content, 'html.parser')
                        # print(soup.prettify())
                        availability_elem = soup.select_one('div#availability')
                        price_elem = soup.select_one('div#corePrice_feature_div')
                        second_price_elem = soup.select_one('div#corePriceDisplay_desktop_feature_div')
                        print(availability_elem.text) if availability_elem else print('No availability elem ???')
                        print(price_elem.text) if price_elem else print('No price elem ???')
                        print(second_price_elem.text) if second_price_elem else print('No second price elem ???')
                        # scrape price
                    print(
                        '________________________________________________________________\n\n\n\n')
                    time.sleep(random.uniform(3, 5))
    except Exception as e:
        print(f'Error : {e}')
