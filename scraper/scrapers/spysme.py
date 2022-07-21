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
# SPYS ME                                                                                       #
#################################################################################################
# Spys.me scraper
# Type: HTTP/HTTPS/SOCKS(?) - possibly all
# Anonymity: ALL
def spys_me_scraper(proxy_type):
    proxy_site = ""
    proxy_type = proxy_type.lower()
    if "http" in proxy_type or "https" in proxy_type or proxy_type == "any":
        proxy_site = 'https://spys.me/proxy.txt'
    if "socks4" in proxy_type or "socks5" in proxy_type or proxy_type == "any":
        proxy_site = 'https://spys.me/socks.txt'
    r = requests.get(proxy_site)
    spys_me_proxies = r.text
    pattern = re.compile('\\d{1,3}(?:\\.\\d{1,3}){3}(?::\\d{1,5})?')
    matcher = re.findall(pattern, spys_me_proxies)
    # with open(pathTextFile, "a") as txt_file:
    #     for proxy in matcher:
    #         txt_file.write(proxy + "\n")
