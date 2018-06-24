import unittest

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import base64
from urllib.parse import urlparse, parse_qs

from celery_task import refresh_ss
from common import b64decode, crawl_ssr


class MyTestCase(unittest.TestCase):
    def test_something(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get('https://free-ss.site/')
        table = driver.find_element_by_id('tb9d72')
        driver.quit()

    def test_ss(self):
        # ret = requests.get('https://ssrshare.xyz/freessr/').text
        # ss_content = base64.b64decode(ret).decode()
        # ss_list = ss_content.split()
        ss_0 = 'ssr://NDUuNzkuOTkuNTI6MTA0MTg6b3JpZ2luOmFlcy0yNTYtY2ZiOnBsYWluOk5USXdabUk1T1RCaE1UWTNPV0V6TldJMVptWTJOVGN3WldJLz9vYmZzcGFyYW09JnJlbWFya3M9NTc2TzVadTk1WXFnNVlpcDU2YVA1YkM4NUxxYTViZWU2TFM1NVlpcDZKS1omZ3JvdXA9VTFOU1UwaEJVa1V1UTA5Tg'
        params = ss_0.split('ssr://')[1]
        params = b64decode(params)
        params = params.split(':')
        print(params)
        ip = params[0]
        port = params[1]
        big_o = params[2]
        small_o = params[4]
        method = params[3]
        parse_res = urlparse(params[5])
        path = parse_res.path.split('/')[0]
        password = b64decode(path)

    def test_ssr(self):
        refresh_ss(False)


if __name__ == '__main__':
    unittest.main()
