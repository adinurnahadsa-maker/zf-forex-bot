import os
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import telebot
import time

# --- KONFIGURASI ---
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
SYMBOLS = ['EURUSD=X', 'GBPUSD=X', 'AUDUSD=X', 'USDJPY=X']

bot = telebot.TeleBot(TOKEN)

def get_data(symbol):
    # Mengambil data 5 hari terakhir untuk memastikan data tersedia
    try:
        data = yf.download(symbol, period='5d', interval='1h', progress=False)
        if data.empty or len(data) < 14:
            return None
        data['RSI'] = ta.rsi(data['Close'], length=14)
        return data
    except Exception as e:
        return None

def main():
    bot.send_message(CHAT_ID, "✅ Bot Radar Sinyal Dimulai!")
    while True:
        for symbol in SYMBOLS:
            df = get_data(symbol)
            if df is not None:
                last_rsi = df['RSI'].iloc[-1]
                msg = f"📊 Sinyal {symbol}\nRSI: {last_rsi:.2f}"
                bot.send_message(CHAT_ID, msg)
            # Menunggu 1 jam sebelum scan ulang agar tidak kena limit
            time.sleep(3600) 

if __name__ == '__main__':
    main()
