import requests
from bs4 import BeautifulSoup
from decimal import Decimal


def get_exchange_rate():
    # usd_rub_url = 'https://www.google.com/search?sxsrf=ALeKk01NWm6viYijAo3HXYOEQUyDEDtFEw%3A1584716087546&source=hp&ei=N9l0XtDXHs716QTcuaXoAg&q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+&gs_l=psy-ab.3.0.35i39i70i258j0i131l4j0j0i131l4.3044.4178..5294...1.0..0.83.544.7......0....1..gws-wiz.......35i39.5QL6Ev1Kfk4'
    usdt_rub_url = "https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+usdt+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALiCzsY8hQWb8NUHuhBGqlR2KPo-QWJ1VQ%3A1666704730016&ei=WuVXY5VP8cj0A7Hqg7AM&oq=%D0%BA%D1%83%D1%80%D1%81+usdt+&gs_lcp=Cgdnd3Mtd2l6EAMYADIKCAAQgAQQRhCCAjIFCAAQgAQyBQgAEIAEMgUIABCABDIICAAQgAQQywEyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoKCAAQRxDWBBCwAzoNCAAQ5AIQ1gQQsAMYAToICC4QgAQQ1AI6DgguEIAEEMcBENEDENQCOgsILhCABBDHARDRAzoFCC4QgAQ6BwguENQCEEM6BAguEEM6CQgAEIAEEAoQAToHCCMQsQIQJzoECAAQQzoHCAAQyQMQQzoHCAAQgAQQCjoHCCMQ6gIQJzoECCMQJzoJCCMQJxBGEP8BSgQITRgBSgQIQRgASgQIRhgBULEIWIkyYKdBaAhwAXgBgAGjBIgB5SOSAQoyLTEwLjAuNC4xmAEAoAEBsAEKyAENwAEB2gEGCAEQARgJ&sclient=gws-wiz"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    page = requests.get(url=usdt_rub_url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    convert = soup.findAll("span", {"class": "pclqee"})
    # convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
    exchange_rate = Decimal(convert[0].text.replace(',', '.'))
    return exchange_rate
