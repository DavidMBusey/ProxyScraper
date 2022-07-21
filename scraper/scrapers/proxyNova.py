import requests
from bs4 import BeautifulSoup
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import configparser
import json
import logging
import re
from scraper.scrapers import freeProxyList


proxies = []
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

#################################################################################################
# ProxyNova                                                                                     #
#################################################################################################
#  ProxyNova.com scraper
def proxy_nova_scraper():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    browser = webdriver.Edge(options=options)
    browser.get('https://www.proxynova.com/proxy-server-list/')
    # https://www.proxynova.com/proxy-server-list/anonymous-proxies/
    # https://www.proxynova.com/proxy-server-list/elite-proxies/
    # https://www.proxynova.com/proxy-server-list/country-
    proxy_table = browser.find_element(By.XPATH, "/html/body/div[4]/div/table/tbody[1]"). \
        find_elements(By.XPATH, '//*[@id="tbl_proxy_list"]/tbody[1]/tr')
    for row in proxy_table:
        row_data = row.text.split()
        try:
            ip = row_data.pop(0)
            port = row_data.pop(0)
            proxy = ':'.join([ip, port])
            logging.debug("[DEBUG] proxy_nova proxy: " + proxy)
            proxies.append(proxy)
        # Default: table has one blank row.
        except Exception as e:
            pass
