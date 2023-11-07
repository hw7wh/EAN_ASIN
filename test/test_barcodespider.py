from requests_html import HTMLSession

session = HTMLSession()

response = session.get('https://www.barcodespider.com/8425402731871') #033984010529

print(response.content)