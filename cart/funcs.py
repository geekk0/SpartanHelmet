import requests
import re
from bs4 import BeautifulSoup
from decimal import Decimal


def get_exchange_rate(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    page = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    convert = soup.find("span", {"class": "pclqee"}).get_text()
    test_string = re.sub("\s+", " ", convert)
    string_value = test_string.replace(',', '.').replace(" ", "")
    exchange_rate = Decimal(string_value)
    return exchange_rate
