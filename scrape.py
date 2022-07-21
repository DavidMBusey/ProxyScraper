import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import logging
from selenium.webdriver.common.proxy import Proxy, ProxyType

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
proxy_url = "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/"
ip_checker_url = "https://whatismyipaddress.com/ip/"
proxy_types = ["socks4", "socks5", "http"]
output_file_dir = "./output/"
output_file_name = output_file_dir + "proxies.txt"


def create_or_emtpy_file():
    with open(output_file_name, 'w') as file:
        file.write("")
        pass


def start():
    for proxy_type in proxy_types:
        logging.info("Starting " + proxy_type + " proxies...")
        proxy_site_request = requests.get(proxy_url + proxy_type + ".txt")
        soup = BeautifulSoup(proxy_site_request.content, 'html.parser')
        proxies = soup.findAll(text=True)[0]
        logging.info("Finished grabbing " + proxy_type + " proxies.")
        logging.info("Collecting IP Information for " + proxy_type + "...")
        for proxy in proxies.text.splitlines():
            ip = proxy.split(":", 1)[0]
            port = proxy.split(":", 1)[1]
            # We will use the proxy and get the proxy country.
            p_options = Proxy({
                'proxyType': ProxyType.MANUAL,
                'httpProxy': proxy,
                'sslProxy': proxy,
                'noProxy': ''})
            # Selenium Options
            options = Options()
            options.headless = True
            options.proxy = p_options
            # options.add_argument("--window-size=1920,1200")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44")
            browser = webdriver.Edge(options=options)
            browser.get(ip_checker_url + ip)
            country = browser.find_elements(By.CLASS_NAME, 'information')[6].text.split(":", 1)[1].replace(" ", "")
            with open(output_file_name, 'a') as f:
                f.write(f"{proxy_type} {ip} {port}  #{country}\n")
        logging.info("Finished collecting data for " + proxy_type)


# Start scrapping proxies
create_or_emtpy_file()
start()
