# agent.py
import requests
from config import WEATHER_API_KEY, ALPHA_VANTAGE_KEY

class RealTimeAgent:
    def __init__(self):
        self.weather_api_key = WEATHER_API_KEY
        self.alpha_vantage_key = ALPHA_VANTAGE_KEY
        self.crypto_api_url = "https://api.coingecko.com/api/v3"

    def get_weather(self, city):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            data = r.json()
            return f"Weather in {city}: {data['weather'][0]['description']}, Temp: {data['main']['temp']}°C, Humidity: {data['main']['humidity']}%"
        except:
            return "❌ Could not fetch weather data. Check city name."

    def get_crypto_price(self, coin):
        url = f"{self.crypto_api_url}/simple/price?ids={coin}&vs_currencies=usd"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            price = r.json().get(coin, {}).get("usd")
            return f"{coin.upper()} price is {price} USD" if price else "❌ Crypto not found."
        except:
            return "❌ Failed to fetch crypto price."

    def get_stock_price(self, symbol):
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.alpha_vantage_key}"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            price = r.json().get("Global Quote", {}).get("05. price")
            return f"{symbol} stock price is {price} USD" if price else "❌ Invalid stock symbol."
        except:
            return "❌ Failed to fetch stock price."

