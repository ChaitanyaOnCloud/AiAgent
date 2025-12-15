# app.py
from flask import Flask, render_template, request, jsonify
from agent import RealTimeAgent

app = Flask(__name__)
agent = RealTimeAgent()

user_state = {}  # Track conversation state per user

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_ip = request.remote_addr
    user_msg = request.json.get("message", "").strip()

    if user_ip in user_state:
        state = user_state[user_ip]

        if state == "weather":
            user_state.pop(user_ip)
            return jsonify({"reply": agent.get_weather(user_msg)})

        if state == "crypto":
            user_state.pop(user_ip)
            return jsonify({"reply": agent.get_crypto_price(user_msg.lower())})

        if state == "stock":
            user_state.pop(user_ip)
            return jsonify({"reply": agent.get_stock_price(user_msg.upper())})

    msg = user_msg.lower()
    if "weather" in msg:
        user_state[user_ip] = "weather"
        reply = "🌤 Which city weather do you want?"
    elif "crypto" in msg:
        user_state[user_ip] = "crypto"
        reply = "💰 Which cryptocurrency price do you want?"
    elif "stock" in msg:
        user_state[user_ip] = "stock"
        reply = "📈 Which stock symbol?"
    else:
        reply = "🤖 Ask me about weather, crypto, or stock."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

