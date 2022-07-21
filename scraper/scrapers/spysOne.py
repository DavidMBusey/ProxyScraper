import concurrent.futures
import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import logging
from scraper.proxyValidator import check

PROXIES = []
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


#################################################################################################
# SPYS ONE                                                                                      #
#################################################################################################
# Spys.one scraper
# Type: ALL
# Anonymity: ALL
def spys_one_scraper():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44")
    browser = webdriver.Edge(options=options)
    browser.get('https://spys.one/free-proxy-list/US/')
    proxy_table = browser.find_elements(By.XPATH, "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr")
    for row in proxy_table:
        columns = row.find_elements(By.XPATH, 'td')
        try:
            proxy = columns[0].text
            # print("proxy " + proxy)
            proxy_type = columns[1].text
            # print("proxy_type " +proxy_type)
            anonymity = columns[2].text
            # print("anonymity " +anonymity)
            country_city_region = columns[3].text
            # print("country_city_region " +country_city_region)
            hostname = columns[4].text
            # print("proxy " +hostname)
            latency = columns[5].text
            # print("latency " + latency)
            speed = columns[6].text
            # print("speed " + speed)
            uptime = columns[7].text
            # print("uptime " + uptime)
            last_checked = columns[8].text
            # print("last_checked " + last_checked)
            logging.debug("Proxy:" + proxy +
                          " Type:" + proxy_type +
                          " Anonymity:" + anonymity +
                          " Country:" + country_city_region +
                          " Hostname:" + hostname +
                          " Latency:" + latency +
                          " Speed:" + speed +
                          " Uptime: " + uptime.replace("+", "").replace("-", "") +
                          " Last Checked:" + last_checked
                          )
            PROXIES.append(proxy)
            PROXIES.append("104.16.211.58:80")
        except Exception as e:  # Default: table throws exceptions due to headers+
            pass
    return ""


def check_proxies():
    check("104.16.211.58:80")
    # logging.info("Starting to verify proxies...")
    # for proxy in PROXIES:
        # check(proxy)
        # x = threading.Thread(target=scraper.proxyValidator.check, args=proxy)
        # x.start()
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     logging.info("Starting to verify proxies...")
    #     executor.map(scraper.proxyValidator.check, proxies)
    #     logging.info("Starting to verify proxies...")


# wait4me = spys_one_scraper()
check_proxies()
