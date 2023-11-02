from curl_cffi.requests import Session  # pip install curl-cffi=0.5.7
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import random

BASE_URL = 'https://www.barcodelookup.com/'

# Define the user-agent to impersonate
user_agent_list = [
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



chunk_size = 100

file_path = 'input/ean.xlsx'


def get_product_details(html):
    product = {}
    soup = BeautifulSoup(html, 'html.parser')
    prddetails_elem = soup.select_one('div.product-details')
    if not prddetails_elem:
        return None
    product['name'] = prddetails_elem.select_one('h4').text.replace(
        '\n', '') if prddetails_elem else None  # get product name from here
    product['asin'] = None
    product['mpn'] = None
    attributes_elem = soup.select_one('ul#product-attributes')
    for li in attributes_elem.find_all('li', class_='product-text'):
        text = li.text.strip()
        if "ASIN:" in text:
            asin = text.split("ASIN:")[1].strip()
            product['asin'] = asin
        elif "MPN:" in text:
            mpn = text.split("MPN:")[1].strip()
            product['mpn'] = mpn

    product['stores'] = []
    onlinestores_elem = soup.select_one('div.online-stores')
    # try to get prices by store from here using regX
    store_list = onlinestores_elem.select_one('div.store-list').find('ol')
    for li in store_list.find_all('li'):
        store_name = li.find('span', class_='store-name').text.strip()
        price = li.find('span', class_='store-link').text.strip()
        store = {
            'store': store_name,
            'price': price,
        }
        product['stores'].append(store)
        # from each elem in list get store_name, price & link
    print(product)
    return product


def process_chunk(chunk, impersonate):
    chunk_data = []
    with Session(impersonate=impersonate) as session:
        print(f'New session started with {impersonate}')
        for ean in chunk['ean']:
            product = {}
            product['id'] = ean
            url = f"{BASE_URL}{ean}"
            response = session.get(url)
            print(f'Connecting to {ean}')
            product = get_product_details(response.content)
            if not product:
                continue
            chunk_data.append(product)
            time.sleep(random.uniform(2, 5))
    return chunk_data


if __name__ == '__main__':
    try:
        df = pd.read_excel(file_path)
        chunksize = max(1, df.shape[0] // chunk_size)
        for i, chunk in enumerate(np.array_split(df, chunksize)):
            if i == 1:
                break
            print(f'Processing chunk {i}...')
            print(chunk.head())
            # impersonate = user_agent_list[i % len(user_agent_list)]
            impersonate = random.choice(user_agent_list)
            process_chunk(chunk, impersonate)
    except Exception as e:
        print("Error:", e)


# # http/socks proxies are supported
# proxies = {"https": "http://localhost:3128"}
# r = requests.get(BASE_URL, impersonate="chrome110", proxies=proxies)
# print(r.content)

# proxies = {"https": "socks://localhost:3128"}
# r = requests.get(BASE_URL, impersonate="chrome110", proxies=proxies)
# print(r.content)
