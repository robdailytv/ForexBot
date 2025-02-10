import requests
import time
import os
import subprocess
import logging

# Telegram Bot Info
TELEGRAM_BOT_TOKEN = "7566422168:AAH2DB3G9RHmdfFC2_BA2-kenfRN3MJK8Ys"
CHAT_ID = "694153691"

# Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ Auto-Update Function
def update_bot():
    logging.info("🔄 Checking for updates...")
    try:
        subprocess.run(["git", "pull"], check=True)
        logging.info("✅ Bot updated successfully!")
    except Exception as e:
        logging.error(f"⚠️ Update failed: {e}")

# ✅ Fetch GBP/JPY Data
def fetch_data():
    url = "https://api.twelvedata.com/time_series?symbol=GBP/JPY&interval=1min&apikey=YOUR_API_KEY"
    try:
        response = requests.get(url)
        data = response.json()
        return data["values"] if "values" in data else None
    except Exception as e:
        logging.error(f"❌ Error fetching data: {e}")
        return None

# ✅ Analyze Trends & Generate Signals
def analyze_trends(data):
    buy_signals, sell_signals = [], []
    for i in range(1, len(data)):
        prev_price = float(data[i-1]["close"])
        curr_price = float(data[i]["close"])
        
        if curr_price > prev_price * 1.002:  # Example Buy Condition (0.2% increase)
            buy_signals.append(data[i])
        elif curr_price < prev_price * 0.998:  # Example Sell Condition (0.2% decrease)
            sell_signals.append(data[i])
    
    return buy_signals, sell_signals

# ✅ Send Alerts to Telegram
def send_alerts(buy_signals, sell_signals):
    message = ""
    if buy_signals:
        message += f"📈 *BUY Signal* at {buy_signals[-1]['datetime']}\n"
    if sell_signals:
        message += f"📉 *SELL Signal* at {sell_signals[-1]['datetime']}\n"
    
    if message:
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", 
                     params={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

# ✅ Main Bot Loop (Runs Every Minute)
def run_bot():
    update_bot()  # Auto-Update Before Running
    while True:
        data = fetch_data()
        if data:
            buy_signals, sell_signals = analyze_trends(data)
            send_alerts(buy_signals, sell_signals)
        time.sleep(60)  # Run every minute

if __name__ == "__main__":
    run_bot()
