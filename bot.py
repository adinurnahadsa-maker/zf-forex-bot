    import os
import telebot
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import time

# Mengambil token dan chat_id dari Environment Variables (sangat aman)
TOKEN = os.environ.get('TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

bot = telebot.TeleBot(TOKEN)

def get_signal(symbol):
    # Mengambil data market
    df = yf.download(symbol, period='1d', interval='15m', progress=False)
    if df.empty:
        return "Gagal mengambil data."
    
    # Menghitung indikator sederhana (RSI)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    rsi_val = df['RSI'].iloc[-1]
    
    if rsi_val < 30:
        return f"🟢 BUY Signal untuk {symbol} (RSI: {rsi_val:.2f})"
    elif rsi_val > 70:
        return f"🔴 SELL Signal untuk {symbol} (RSI: {rsi_val:.2f})"
    else:
        return f"⚪ Wait/Sideways {symbol} (RSI: {rsi_val:.2f})"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "ZF-Core Engine Aktif! Gunakan /cek untuk melihat signal.")

@bot.message_handler(commands=['cek'])
def check_market(message):
    signal = get_signal("EURUSD=X")
    bot.reply_to(message, signal)

# Loop utama untuk menjaga bot tetap hidup
print("Bot sedang berjalan...")
bot.polling(none_stop=True)
