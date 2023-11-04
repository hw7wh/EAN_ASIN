from curl_cffi.requests import Session  # pip install curl-cffi=0.5.7
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pandas as pd
import numpy as np
from datetime import datetime
import time
import random
from dotenv import load_dotenv
import os

# FOR DEBUG ONLY
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# ______

load_dotenv()  # take environment variables from .env.

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME")

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


# MongoDB setup (.env file later)
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]  # replace with your database name
products_collection = db[COLLECTION_NAME]  # replace with your collection name


def insert_product(product_obj):
    try:
        # Check if jet exists
        existing_product = products_collection.find_one({"_id": product_obj["id"]})
        if not existing_product:
            # In MongoDB, the unique identifier is "_id". We're setting it to the same value as "id".
            product_obj["_id"] = product_obj["id"]
            # Insert the jet object
            products_collection.insert_one({
                **product_obj,
                'createdAt': datetime.now(),
                'updatedAt': datetime.now()
            })
            print(f"Added product with id {product_obj['id']}")
        else:
            updated = False  # Flag to check if update occurred
            for key in existing_product:
                if existing_product[key] is None and product_obj.get(key) is not None:
                    products_collection.update_one(
                        {'_id': product_obj["id"]},
                        {
                            '$set': {
                                **product_obj,
                                'updatedAt': datetime.now()
                            }
                        }
                    )
                    print(f"Updated product with id {product_obj['id']}")
                    updated = True
                    break  # Exit the loop after the first update
            if not updated:
                print(f"Product with id {product_obj['id']} already exists.")
    except Exception as error:
        print("Insertion error:", error)


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
    if attributes_elem:
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
        print(f'---------------------------\nNew session started with {impersonate}\n---------------------------')
        for ean in chunk['ean']:
            url = f"{BASE_URL}{ean}"
            response = session.get(url)
            print(f'Connecting to {ean}')
            product = get_product_details(response.content)
            if not product:
                continue
            product['id'] = ean
            insert_product(product)
            chunk_data.append(product)
            time.sleep(random.uniform(1, 3))
    return chunk_data


if __name__ == '__main__':
    try:
        df = pd.read_excel(file_path)
        chunksize = max(1, df.shape[0] // chunk_size)
        for i, chunk in enumerate(np.array_split(df, chunksize)):
            if i == 0 and i == 1:
                continue
            if i == 20:
                break
            chunk_data = []
            print(f'Processing chunk {i}...')
            print(chunk.head())
            # impersonate = user_agent_list[i % len(user_agent_list)]
            impersonate = random.choice(user_agent_list)
            chunk_data = process_chunk(chunk, impersonate)
    except Exception as e:
        print("Error:", e)


# # http/socks proxies are supported
# proxies = {"https": "http://localhost:3128"}
# r = requests.get(BASE_URL, impersonate="chrome110", proxies=proxies)
# print(r.content)

# proxies = {"https": "socks://localhost:3128"}
# r = requests.get(BASE_URL, impersonate="chrome110", proxies=proxies)
# print(r.content)
