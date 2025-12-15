from flask import Flask, render_template_string, request, jsonify
import requests

# -------------------- Flask App --------------------
app = Flask(__name__)

# -------------------- RealTimeAgent Logic --------------------
class RealTimeAgent:
    def __init__(self, weather_api_key, alpha_vantage_key, crypto_api_url="https://api.coingecko.com/api/v3"):
        self.weather_api_key = weather_api_key
        self.alpha_vantage_key = alpha_vantage_key
        self.crypto_api_url = crypto_api_url

    # Weather API
    def get_weather(self, city):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            return f"Weather in {city}: {weather}, Temp: {temp}°C, Humidity: {humidity}%"
        except:
            return "Could not fetch weather data. Make sure city name is correct."

    # Crypto API
    def get_crypto_price(self, crypto_name="bitcoin", currency="usd"):
        url = f"{self.crypto_api_url}/simple/price?ids={crypto_name}&vs_currencies={currency}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            price = data.get(crypto_name, {}).get(currency)
            if price:
                return f"The current price of {crypto_name.capitalize()} is {price} {currency.upper()}"
            else:
                return "Crypto data not found."
        except:
            return "Failed to fetch crypto price."

    # Stock API
    def get_stock_price(self, symbol):
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            quote = data.get("Global Quote", {})
            price = quote.get("05. price")
            if price:
                return f"The current price of {symbol.upper()} is {price} USD"
            else:
                return "Stock data not available or invalid symbol."
        except:
            return "Failed to fetch stock price."

# -------------------- API Keys --------------------
WEATHER_API_KEY = "deadb30e689bfcf4ded388dc91c976cd"
ALPHA_VANTAGE_KEY = "d4vtui1r01qs25f2duv0d4vtui1r01qs25f2duvg"

agent = RealTimeAgent(WEATHER_API_KEY, ALPHA_VANTAGE_KEY)

# -------------------- User State --------------------
user_state = {}  # key = user IP, value = waiting state ("awaiting_city"/"awaiting_crypto"/"awaiting_stock")

# -------------------- HTML + CSS + JS --------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>RealTimeAgent Chat</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f7fa; display:flex; justify-content:center; padding-top:30px; }
        #chat-container { width: 100%; max-width: 600px; background: #fff; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); display:flex; flex-direction:column; }
        #messages { padding:20px; flex:1; overflow-y:auto; max-height:500px; }
        .message { margin:10px 0; display:flex; }
        .user { justify-content:flex-end; }
        .user .bubble { background:#007BFF; color:#fff; border-radius:15px 15px 0 15px; padding:10px 15px; max-width:70%; }
        .bot { justify-content:flex-start; }
        .bot .bubble { background:#e4e6eb; color:#000; border-radius:15px 15px 15px 0; padding:10px 15px; max-width:70%; }
        #input-form { display:flex; border-top:1px solid #ddd; }
        #input-form input { flex:1; padding:15px; border:none; border-radius:0 0 0 10px; font-size:16px; }
        #input-form button { padding:15px; border:none; background:#007BFF; color:#fff; font-size:16px; cursor:pointer; border-radius:0 0 10px 0; }
        #input-form button:hover { background:#0056b3; }
    </style>
</head>
<body>
    <div id="chat-container">
        <div id="messages"></div>
        <form id="input-form">
            <input type="text" id="user-input" placeholder="Ask about weather, crypto, stock..." autocomplete="off" required>
            <button type="submit">Send</button>
        </form>
    </div>

    <script>
        const form = document.getElementById("input-form");
        const input = document.getElementById("user-input");
        const messages = document.getElementById("messages");

        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const userText = input.value.trim();
            if(!userText) return;

            // Show user message
            const userDiv = document.createElement("div");
            userDiv.className = "message user";
            userDiv.innerHTML = `<div class="bubble">${userText}</div>`;
            messages.appendChild(userDiv);

            input.value = "";
            messages.scrollTop = messages.scrollHeight;

            // Send to server
            const res = await fetch("/get_response", {
                method:"POST",
                headers:{"Content-Type":"application/json"},
                body: JSON.stringify({message:userText})
            });
            const data = await res.json();

            // Show bot response
            const botDiv = document.createElement("div");
            botDiv.className = "message bot";
            botDiv.innerHTML = `<div class="bubble">${data.reply}</div>`;
            messages.appendChild(botDiv);
            messages.scrollTop = messages.scrollHeight;
        });
    </script>
</body>
</html>
"""

# -------------------- Flask Routes --------------------
@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message", "").strip()
    user_ip = request.remote_addr
    reply = "I did not understand that. Please ask weather, crypto, or stock."

    # Check if user is waiting for city/crypto/stock
    if user_ip in user_state:
        state = user_state[user_ip]
        if state == "awaiting_city":
            city = user_input
            reply = agent.get_weather(city)
            del user_state[user_ip]
            return jsonify({"reply": reply})
        elif state == "awaiting_crypto":
            coin = user_input
            reply = agent.get_crypto_price(coin.lower(), "usd")
            del user_state[user_ip]
            return jsonify({"reply": reply})
        elif state == "awaiting_stock":
            symbol = user_input.upper()
            reply = agent.get_stock_price(symbol)
            del user_state[user_ip]
            return jsonify({"reply": reply})

    # Detect main command
    words_lower = [w.lower() for w in user_input.split()]
    if "weather" in words_lower:
        user_state[user_ip] = "awaiting_city"
        reply = "Sure! Which city do you want the weather for?"
    elif "crypto" in words_lower:
        user_state[user_ip] = "awaiting_crypto"
        reply = "Sure! Which cryptocurrency do you want the price for?"
    elif "stock" in words_lower:
        user_state[user_ip] = "awaiting_stock"
        reply = "Sure! Which stock symbol do you want the price for?"

    return jsonify({"reply": reply})

# -------------------- Run App --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

