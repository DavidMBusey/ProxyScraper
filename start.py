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

# TODO support other browsers for seleneium and docker this shit up
# browser = webdriver.Chrome()
# browser = webdriver.Firefox()
# browser = webdriver.Safari()


#################################################################################################
# START OF SCRAPE CODE                                                                          #
#################################################################################################
# OUR PROXY LIST

def start_scraper():
    # geonode_scraper()
    # open_proxy_space_scraper(settings_proxy_type)
    # proxy_scrape_scraper()
    # proxy_nova_scraper()
    # spys_me_scraper(settings_proxy_type.upper())
    # spys_one_scraper()

    ##################################
    # freeProxyListScraper.scrape_proxies()
    return


# Start scrapping proxies
start_scraper()