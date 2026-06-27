import os
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import telebot
from requests_cache import CachedSession

# --- KONFIGURASI ---
# Token diambil dari pengaturan 'Variables' di Railway
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
SYMBOLS = ['EURUSD=X', 'GBPUSD=X', 'AUDUSD=X', 'USDJPY=X']

bot = telebot.TeleBot(TOKEN)
session = CachedSession('cache_file', expire_after=300)

def get_data(symbol):
    data = yf.download(symbol, period='1d', interval='1h', session=session)
    if data.empty:
        return None
    data['RSI'] = ta.rsi(data['Close'], length=14)
    return data

def main():
    bot.send_message(CHAT_ID, "Bot sedang berjalan...")
    for symbol in SYMBOLS:
        df = get_data(symbol)
        if df is not None:
            last_rsi = df['RSI'].iloc[-1]
            msg = f"Radar Sinyal: {symbol}\nRSI: {last_rsi:.2f}"
            bot.send_message(CHAT_ID, msg)
        else:
            bot.send_message(CHAT_ID, f"Data {symbol} tidak tersedia.")

if __name__ == '__main__':
    main()
