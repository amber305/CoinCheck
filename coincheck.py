import time
import requests
import pandas as pd
import matplotlib.pyplot as plt
from config import DEFAULT_CRYPTO, DEFAULT_CURRENCY, REFRESH_INTERVAL, API_URL

class CoinCheck:
    def __init__(self, crypto=DEFAULT_CRYPTO, currency=DEFAULT_CURRENCY):
        self.crypto = crypto
        self.currency = currency
        self.history = []

    def get_price(self):
        params = {
            'ids': self.crypto,
            'vs_currencies': self.currency
        }
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get(self.crypto, {}).get(self.currency, None)
        else:
            print("Error fetching data!")
            return None

    def track_price(self):
        while True:
            price = self.get_price()
            if price:
                print(f"Current {self.crypto} Price: {price} {self.currency}")
                self.history.append(price)
                self.plot_price_trend()
            time.sleep(REFRESH_INTERVAL)

    def plot_price_trend(self):
        if len(self.history) > 1:
            df = pd.DataFrame(self.history, columns=['Price'])
            plt.plot(df.index, df['Price'], marker='o')
            plt.title(f"{self.crypto} Price Trend")
            plt.xlabel("Time (interval)")
            plt.ylabel(f"Price ({self.currency})")
            plt.grid(True)
            plt.show()

if __name__ == "__main__":
    crypto = input("Enter the cryptocurrency symbol (e.g., BTC, ETH): ").lower()
    currency = input("Enter the currency to track (e.g., USD, EUR): ").lower()

    tracker = CoinCheck(crypto, currency)
    tracker.track_price()
