from curl_cffi.requests import Session

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

URL = 'https://www.amazon.pl/dp/B0BPY7HSC4/'

impersonate = 'safari15_5'

if __name__ == '__main__':
    try:
        with Session(impersonate=impersonate) as session:
            url = f"{URL}"
            response = session.get(url)
            print(f'Connecting to {URL}...')
            print(response.content)
    except Exception as e:
        print(f'Error : {e}')
