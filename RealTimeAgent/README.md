# 🤖 Real-Time AI Agent (Weather`: • Crypto • Stock)

A **chat-based Real-Time AI Agent** built using **Python & Flask** that provides live:
- 🌦 Weather updates for any city
- 💰 Cryptocurrency prices
- 📈 Stock market prices

The application works like a **ChatGPT-style interface** and fetches real-time data using public APIs.  
Deployed on **AWS EC2**.

---

## 🚀 Features

- Chat-style web interface (similar to ChatGPT)
- Real-time weather for **any user-input city**
- Live cryptocurrency prices (Bitcoin, Ethereum, etc.)
- Live stock prices
- User-friendly UI with HTML, CSS & JavaScript
- Backend powered by Flask REST APIs

---

## 🛠 Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **APIs Used:**
  - OpenWeatherMap API (Weather)
  - CoinGecko API (Crypto)
  - Alpha Vantage API (Stocks)
- **Deployment:** AWS EC2
- **Version Control:** Git

---

## 📁 Project Structure

RealTimeAgent/
│
├── app.py # Flask app + routes
├── agent.py # RealTimeAgent class (logic)
├── config.py # API keys
├── templates/
│ └── index.html # HTML chat interface
├── static/
│ └── style.css # CSS design
├── requirements.txt
└── README.md


Update System & Install Python:-

sudo apt update
sudo apt install python3 python3-venv python3-pip -y

Clone the Repository:-

git clone https://github.com/your-username/RealTimeAgent.git
cd RealTimeAgent

Create and Activate Virtual Environment:-

python3 -m venv venv
source venv/bin/activate

Install Python Dependencies:-

pip install -r requirements.txt

Run the Flask Application:-

python app.py
