# WORKS PERFECTLY WORKS ON 14 --> WORKS ON 53 / 41 minutes (47seconds/asin)
# --> save asin if exit from every product to a list on every 50 ean -> test this script

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

NEW_ASIN = [
    'B0915ZWW42',
    'B01E7BI07M',
    'B01A1C6IPM',
    'B0877M1QBS',
    'B01HSPPDC4',
    'B00TDFAL3Y',
    'B0001SREQY',
    'B00F42EWKS',
    'B00014FBTU',
    'B000US24LK',
    'B00H2H37YA',
    'B0748NFJR5',
    'B0054RHE8U',
    'B00020IBC2',
    'B00014EXB2',
    'B0011FWJG6',
    'B0001VW4F2',
    'B00020IBF4',
    'B000WMV9B0',
    'B000WMZ4F2',
    'B000Z92LB2',
    'B000Z94F3O',
    'B001BCO4JE',
    'B002PH6IVG',
    'B002PN6B4Y',
    'B002VWT33A',
    'B004HIK2UO',
    'B004V8LYB6',
    'B0051OWT04',
    'B0051US4W0',
    'B0052MIHGA',
    'B007FJH17Y',
    'B007SH7LC8',
    'B008JLN69Y',
    'B008LFA7I6',
    'B00A2LKPAW',
    'B00AJRAQD0',
    'B00AYE4WDI',
    'B00CRENRLQ',
    'B00F415DZW',
    'B00F42ERTE',
    'B00FW7UUI8',
    'B00HYC40BC',
    'B00I0C9DZI',
    'B00S9XZTO2',
    'B00TO8P2CK',
    'B00TOC427W',
    'B00TOFCAYG',
    'B00TOGBBHM',
    'B00VHX3W2M',
    'B00VHX3XS0',
    'B00WYQ7SIU',
    'B0146XXW8I']


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
            for asin in NEW_ASIN:
                impersonate = random.choice(USER_AGENT_LIST)
                with Session(impersonate=impersonate) as session:
                    url = amazon_url + asin
                    response = session.get(url)
                    print(f'Connecting to {url}...')
                    if response.ok:  # TRUE if prod exists FALSE otherwise
                        soup = BeautifulSoup(response.content, 'html.parser')
                        # print(soup.prettify())
                        availability_elem = soup.select_one('div#availability') # availability_feature_div
                        price_elem = soup.select_one(
                            'div#corePrice_feature_div')
                        second_price_elem = soup.select_one(
                            'div#corePriceDisplay_desktop_feature_div')
                        print(availability_elem.text) if availability_elem else print(
                            'No availability elem ???')
                        print(price_elem.text) if price_elem else print(
                            'No price elem ???')
                        print(second_price_elem.text) if second_price_elem else print(
                            'No second price elem ???')


                        # NOT TESTED YET !!!
                        # technical_details_elem = soup.select_one(
                        #     'table#productDetails_techSpec_section_1')
                        # additional_info_elem = soup.select_one(
                        #     'table#productDetails_db_sections')
                        # bullet_points_elem = soup.select_one(
                        #     'div#detailBulletsWrapper_feature_div')
                        # title_elem = soup.select_one('span#productTitle')
                        # overview_elem = soup.select_one(
                        #     'div#productOverview_feature_div')
                        # print(overview_elem.text) if overview_elem else print(
                        #     'No overview elem ???')
                        # print(title_elem.text) if title_elem else print(
                        #     'No title elem ???')
                        # print(bullet_points_elem.text) if bullet_points_elem else print(
                        #     'No bullet points element ???')
                        # print(additional_info_elem.text) if additional_info_elem else print(
                        #     'No additional info element ???')
                        # print(technical_details_elem) if technical_details_elem else print(
                        #     'No technical details ???')
                        # scrape price
                    print(
                        '________________________________________________________________\n\n\n\n')
                    time.sleep(random.uniform(3, 5))
    except Exception as e:
        print(f'Error : {e}')
