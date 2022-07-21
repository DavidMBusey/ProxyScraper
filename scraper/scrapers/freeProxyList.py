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


#################################################################################################
# These are all the owned by the same people.                                                   #
# Format is constant, with the exception of the Socks-Proxy                                     #
#################################################################################################
# SSLProxies.org
# HTTPS
import logging

import requests
from bs4 import BeautifulSoup

proxies = []
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')



def scrape_proxies():
    ssl_proxies_scraper()
    free_proxy_list_anonymous_scraper()
    free_proxy_list_scraper()
    free_proxy_list_uk_scraper()
    us_proxy_scraper()
    socks_proxy_scraper()


def ssl_proxies_scraper():
    proxy_site = 'https://www.sslproxies.org/'
    scrape(proxy_site)


# Free-proxy-list.net anonymous scraper
# Type: HTTP/HTTPS
# Anonymity: Anonymous and Elite Proxy
def free_proxy_list_anonymous_scraper():
    proxy_site = 'https://free-proxy-list.net/anonymous-proxy.html'
    scrape(proxy_site)


# Free-proxy-list.net Default scraper
# Type: HTTP/HTTPS
# Anonymity: ALL
def free_proxy_list_scraper():
    proxy_site = 'https://free-proxy-list.net/'
    scrape(proxy_site)


# Free-proxy-list.net UK scraper
# Type: HTTP/HTTPS
# Anonymity: ALL
def free_proxy_list_uk_scraper():
    proxy_site = 'https://free-proxy-list.net/uk-proxy.html'
    scrape(proxy_site)


# US-Proxy.org US scraper
# Type: HTTP/HTTPS
# Anonymity: ALL
def us_proxy_scraper():
    proxy_site = 'http://us-proxy.org'
    scrape(proxy_site)


# Socks-Proxy.net
# Type: Socks4
# Anonymity: Anonymous
def socks_proxy_scraper():
    proxy_site = 'https://www.socks-proxy.net/'
    scrape(proxy_site)
    ### SMALL VAR ISSUE:
    # 4 = VERSION = SOCKS4
    # 5 = Anonymity = Anonymous


def scrape(proxy_site):
    logging.info("Starting to scrape from: " + proxy_site)
    r = requests.get(proxy_site)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('tbody')
    # table = soup.find("table", attrs={"class": "table table-striped table-bordered"})
    for row in table.find_all("tr"):
        try:
            ip = row.find_all("td")[0].text or ""
            port = row.find_all("td")[1].text or ""
            code = row.find_all("td")[2].text or ""
            country = row.find_all("td")[3].text or ""
            anonymity = row.find_all("td")[4].text or ""
            google = row.find_all("td")[5].text or ""
            https = row.find_all("td")[6].text or ""
            last_checked = row.find_all("td")[7].text or ""
            logging.debug("ip:" + ip +
                          " port :" + port +
                          " code :" + code +
                          " country:" + country +
                          " Anonymity:" + anonymity +
                          " google:" + google +
                          " Https:" + https +
                          " Last Checked:" + last_checked
                          )
            proxy = ':'.join([ip, port])
            proxies.append(proxy)
        except Exception as e:  # Default: table has one blank row.
            continue

