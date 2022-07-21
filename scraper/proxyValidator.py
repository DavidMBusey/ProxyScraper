#################################################################################################
#   TESTING  PROXIES                                                                            #
#################################################################################################
import logging

import requests
import configparser

OUTPUT_DIR = "../output/"
OUTPUT_HTTP_FILE = OUTPUT_DIR + 'HTTP.txt'
OUTPUT_WORKING_FILE = OUTPUT_DIR + 'working.txt'
OUTPUT_SOCKS4_FILE = OUTPUT_DIR + 'socks4.txt'
OUTPUT_SOCKS5_FILE = OUTPUT_DIR + 'socks5.txt'
OUTPUT_EXCLUDED_FILE = OUTPUT_DIR + 'excluded.txt'
OUTPUT_MISCONFIURED_FILE = OUTPUT_DIR + 'misconfigured.txt'
CUSTOM_OUTPUT = OUTPUT_DIR + 'custom_output.txt'
verify_url = "https://httpbin.org/ip"


def get_advanced_proxy_info(proxy):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    ip = proxy.split(":", 1)[0]
    print("HEY YOU FOUND A TODO!")  # TODO ADD ENFORCEMENT FOR PROXIES
    try:
        # Gets country info.
        r = requests.get('https://whatismyipaddress.com/ip/' + ip, headers=headers,
                         proxies=dict(http=f'http://{proxy}'))
        r = requests.get('https://whatismyipaddress.com/ip/' + ip, headers=headers,
                         proxies=dict(http=f'socks4://{proxy}'))
        r = requests.get('https://whatismyipaddress.com/ip/' + ip, headers=headers,
                         proxies=dict(http=f'socks5://{proxy}'))
    except Exception as e:
        pass
    return ""


def check(proxy, **kwargs):
    print(proxy)
    proxy_settings = configparser.ConfigParser()
    proxy_settings_file = '../config/proxy_settings.cfg'
    proxy_settings.read(proxy_settings_file)
    #TODO WHEN I CALL ON THIS FROM SPYSONE, IT BREAKS!?
    p_type = ""
    anonymity = ""
    country = ""
    speed = ""
    latency = ""
    output_format = ""
    try:
        p_type = proxy_settings['PROXY_SETTINGS']['Proxy_Type'].lower()
        anonymity = proxy_settings['PROXY_SETTINGS']['Proxy_Anonymity'].lower()
        country = proxy_settings['PROXY_SETTINGS']['Proxy_Country'].lower()
        speed = proxy_settings['PROXY_SETTINGS']['Proxy_Country'].lower()
        latency = proxy_settings['PROXY_SETTINGS']['Proxy_Country'].lower()
        output_format = proxy_settings['EXPORT_SETTINGS']['Export_File_Format'].lower()
    except Exception as e:
        pass

    output = proxy
    # Using this site to verify
    ip = proxy.split(":", 1)[0]
    port = proxy.split(":", 1)[1]
    proxy_type = kwargs.get('type', p_type)
    proxy_anonymity = kwargs.get('anonymity', anonymity)
    proxy_country = kwargs.get('country', country)
    proxy_speed = kwargs.get('speed', speed)
    proxy_latency = kwargs.get('latency', latency)
    # Do we want to enforce/check for actual data?
    if kwargs.get('enforce', proxy_settings['EXPORT_SETTINGS']['Enforce_Export_Policy'].lower()) == "true":
            print("HEY YOU FOUND A TODO!")  # TODO ADD ENFORCEMENT FOR PROXIES
            TODORANDOMVAR = get_advanced_proxy_info(proxy)
    if proxy_settings['EXPORT_SETTINGS']['Enforce_Export_Policy'].lower() != "":
        output = output_format \
            .replace("ip", ip) \
            .replace("port", port) \
            .replace("type", proxy_type) \
            .replace("anonymity", proxy_anonymity) \
            .replace("speed", proxy_speed) \
            .replace("latency", proxy_latency)
    logging.warning(output)
    
    if "http" in proxy_type or "https" in proxy_type or "any" in proxy_type:
        try:
            resp = requests.get(verify_url, proxies=dict(http=f'http://{proxy}'), timeout=10)
            if resp.status_code == 200:
                with open(OUTPUT_WORKING_FILE, 'a') as f:
                    f.write(output + "n\r")
            else:
                with open(OUTPUT_MISCONFIURED_FILE, 'a') as f:
                    f.write(f"{proxy},http,{resp.elapsed.total_seconds()}\n")
        except requests.ConnectionError as err:
            pass
    if "socks5" in proxy_type or "any" in proxy_type:
        try:
            resp = requests.get(verify_url, proxies=dict(http=f'socks5://{proxy}'), timeout=10)
            if resp.status_code == 200:
                if resp.text == "ok\n":
                    with open(OUTPUT_WORKING_FILE, 'a') as f:
                        f.write(output)
                else:
                    with open(OUTPUT_EXCLUDED_FILE, 'a') as f:
                        f.write(f"{proxy},socks5,{resp.elapsed.total_seconds()}\n")
            else:
                with open(OUTPUT_MISCONFIURED_FILE, 'a') as f:
                    f.write(f"{proxy},socks5,{resp.elapsed.total_seconds()}\n")
        except requests.ConnectionError as err:
            pass
    if "socks4" in proxy_type or "any" in proxy_type:
        try:
            resp = requests.get(verify_url, proxies=dict(http=f'socks4://{proxy}'), timeout=10)
            if resp.status_code == 200:
                if resp.text == "ok\n":
                    with open(OUTPUT_WORKING_FILE, 'a') as f:
                        f.write(output)
                else:
                    with open(OUTPUT_EXCLUDED_FILE, 'a') as f:
                        f.write(f"{proxy},socks4,{resp.elapsed.total_seconds()}\n")
            else:
                with open(OUTPUT_MISCONFIURED_FILE, 'a') as f:
                    f.write(f"{proxy},socks4,{resp.elapsed.total_seconds()}\n")
        except requests.ConnectionError as err:
            pass


check("104.16.211.58:80")

############## OG CHECKER

# def check(proxy, **kwargs):
#     proxy_type = kwargs.get('type', 'all')
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
#     proxy_type = proxy_type.lower().replace(" ", "")
#     if "http" in proxy_type or "https" in proxy_type or "all" in proxy_type:
#         try:
#             http_proxies = {
#                 'http': proxy,
#                 'https': proxy,
#             }
#             r = requests.get('https://httpbin.org/ip', headers=headers, proxies=http_proxies)
#             print("Working Proxy: ", r.json(), r.status_code)
#         except requests.ConnectionError as err:
#             pass
#     if "socks5" in proxy_type or "all" in proxy_type:
#         try:
#             socks5_proxies = {
#                 'http': "socks5://" + proxy,
#                 'https': "socks5://" + proxy,
#             }
#             r = requests.get('https://httpbin.org/ip', headers=headers, proxies=socks5_proxies)
#             print("Working Proxy: ", r.json(), r.status_code)
#         except requests.ConnectionError as err:
#             pass
#     if "socks4" in proxy_type or "all" in proxy_type:
#         try:
#             socks4_proxies = {
#                 'http': "socks4://" + proxy,
#                 'https': "sock4://" + proxy,
#             }
#             r = requests.get('https://httpbin.org/ip', headers=headers, proxies=socks4_proxies)
#             print("Working Proxy: ", r.json(), r.status_code)
#         except requests.ConnectionError as err:
#             pass

