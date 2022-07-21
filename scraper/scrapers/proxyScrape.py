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
# ProxyScrape                                                                                   #
#################################################################################################
# Proxyscrape.com scraper
# Uses BeautifulSoup
def proxy_scrape_scraper():
    r = requests.get(
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all')
    soup = BeautifulSoup(r.content, 'html.parser')
    proxylist = soup.text.split()
    for proxy in proxylist:
        proxies.append(proxy)
    return