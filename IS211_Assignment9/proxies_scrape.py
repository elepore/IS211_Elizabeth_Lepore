
from bs4 import BeautifulSoup
import requests
import random 
import time 

# Scrapes free proxy websites for online public proxies and then returns a link. 
COUNTRIES = ["US", "AU", "CA", "DE", "MX", "NL", "GB"]
# Countries I want proxies from 
def get_proxies_from_page(url, headers):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    tr_tags = soup.find_all('tr')

    proxies = []
    for tr in tr_tags:
        td_tags = tr.find_all('td')
        if len(td_tags) > 7:
            ip = td_tags[0].text
            port = td_tags[1].text
            country_code = td_tags[2].text
            anonymity = td_tags[4].text
            https = td_tags[6].text

            if country_code in COUNTRIES and anonymity == 'elite proxy' and https == 'yes':
                proxies.append(f"{ip}:{port}")

    return proxies

def main():
    all_proxies = set()
    HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    URLS = ["https://free-proxy-list.net/", "https://sslproxies.org/", "https://hidemy.life/en/proxy-list-servers"]
    for url in URLS:
        extracted_proxies = get_proxies_from_page(url, HEADERS)
        all_proxies.update(extracted_proxies)

        delay = random.randint(1, 3)
        time.sleep(delay)

    return list(all_proxies)

proxy_list = main()
print(proxy_list)
