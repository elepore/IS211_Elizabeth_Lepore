
from bs4 import BeautifulSoup
import requests

def scrape_apple_stock():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    } # Due to previous scraping I was getting a 404 error so I've used headers. 

    url = "https://finance.yahoo.com/quote/AAPL/history?p=AAPL&guccounter=1"


    with requests.Session() as session:
        session.headers.update(headers)

        try:
            response = session.get(url, timeout=60)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            table = soup.find('table', {'data-test': 'historical-prices'})

            for row in table.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) >= 5:  
                    date = cols[0].get_text(strip=True)
                    close_price = cols[4].get_text(strip=True) 

                    print(f"Date: {date}, Close Price: {close_price}")

        except requests.RequestException as e:
            print(f"Error occurred with {e}")
            return None

if __name__ == "__main__":
    scrape_apple_stock()
