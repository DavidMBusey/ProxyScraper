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

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Load countries
countries_config = open('../config/countries.json')
countries = json.load(countries_config)

# Load Proxy Settings
proxy_settings = configparser.ConfigParser()
proxy_settings_file = '../config/proxy_settings.cfg'
proxy_settings.read(proxy_settings_file)
settings_anonymity = proxy_settings['PROXY_SETTINGS']['Proxy_Anonymity']
settings_ssl = proxy_settings['PROXY_SETTINGS']['Proxy_SSL']
settings_allowed_ports = proxy_settings['PROXY_SETTINGS']['Proxy_Ports']
settings_proxy_type = proxy_settings['PROXY_SETTINGS']['Proxy_Type']
settings_max_latency = proxy_settings['PROXY_SETTINGS']['Proxy_Max_Latency']
settings_max_speed = proxy_settings['PROXY_SETTINGS']['Proxy_Max_Speed']
settings_last_checked = proxy_settings['PROXY_SETTINGS']['Proxy_Last_Checked']
settings_minimum_uptime = proxy_settings['PROXY_SETTINGS']['Proxy_Min_Uptime']
settings_country = proxy_settings['PROXY_SETTINGS']['Proxy_Country']
logging.debug('%s', '{:>125}'.format("[DEBUG] Settings config: " + "\n\r") +
              '{:>100}'.format(" Proxy_Anonymity: " + settings_anonymity) +
              '{:>100}'.format(" Proxy_SSL: " + settings_ssl) + "\n\r" +
              '{:>100}'.format(" Proxy_Ports: " + settings_allowed_ports) +
              '{:>100}'.format(" Proxy_Type: " + settings_proxy_type) + "\n\r" +
              '{:>100}'.format(" Proxy_Max_Latency: " + settings_max_latency) +
              '{:>100}'.format(" Proxy_Max_Speed: " + settings_max_speed) + "\n\r" +
              '{:>100}'.format(" Proxy_Last_Checked: " + settings_last_checked) +
              '{:>100}'.format(" Proxy_Min_Uptime: " + settings_minimum_uptime) +
              '{:>100}'.format(" Proxy_Country: " + settings_country))

# Verify User Settings - OPTIONS SUPPORTED
anonymity_options = ['ANY', 'TRANSPARENT', 'ANONYMOUS', 'ELITE']
ssl_options = ['TRUE', 'FALSE']
proxy_allow_ports_options = ['ANY']
proxy_type_options = ['ANY', 'HTTP', 'HTTPS', 'SOCKS4', 'SOCKS5']
proxy_min_uptime_options = ['ANY']
# proxy_disallow_ports_options
latency_options = {
    'ANY': '',
    'LOW': '60',
    'MEDIUM': '180',
    'HIGH': '180'
}
speed_options = {
    'ANY': '',
    'LOW': '250',
    'MEDIUM': '800',
    'HIGH': '800'
}


#################################################################################################
# CONFIGURATION VALIDATION                                                                      #
#################################################################################################


def validate_user_settings():
    # Anonymity
    if settings_anonymity.upper() not in anonymity_options:
        logging.exception("[PROXY SETTINGS] The ANONYMITY set is not a valid value ", settings_anonymity)
    # SSL
    if settings_ssl.upper() not in ssl_options:
        logging.exception("[PROXY SETTINGS] The SSL set is not a valid value ", settings_ssl)
    # if settings_allowed_ports not in proxy_allow_ports_options:
    #     try:
    #         int(settings_allowed_ports)
    #     except Exception as e:
    #         settings_minimum_uptime.replace(" ", "").split(",")     # ADD A-Z CHARS
    #         # TODO check if it is valid.
    #         logging.exception("[PROXY SETTINGS] The max SPEED set is not a valid value ", settings_max_speed, e)
    # Proxy Types
    if settings_proxy_type.upper() not in proxy_type_options:
        logging.exception("[PROXY SETTINGS] The PROXY TYPE ", settings_proxy_type, " in the ", proxy_settings_file,
                          " is not valid.")
    # Max Latency
    if settings_max_latency not in latency_options.keys():
        try:
            int(settings_max_latency)
        except Exception as e:
            logging.exception("[PROXY SETTINGS] The MAX LATENCY set is not a valid value ", settings_max_latency, e)
    # Max Speed
    if settings_max_speed not in speed_options.keys():
        try:
            int(settings_max_speed)
        except Exception as e:
            logging.exception("[PROXY SETTINGS] The MAX SPEED ", settings_max_speed, " in the ", proxy_settings_file,
                              " is not valid.", e)
    # Min Uptime
    if settings_minimum_uptime not in proxy_min_uptime_options:
        try:
            int(settings_minimum_uptime)
        except Exception as e:
            logging.exception("[PROXY SETTINGS] The max MIN UPTIME set is not a valid value ", settings_max_speed, e)
    # Countries
    if settings_country.upper() not in countries['countries'] and settings_country.upper() not in countries[
        'countries']:
        if settings_country.upper() not in countries['countries'] and settings_country.upper() != "ANY":
            logging.exception("[PROXY SETTINGS] The COUNTRY ", settings_country, " in the ", proxy_settings_file,
                              " is not valid.")


validate_user_settings()
